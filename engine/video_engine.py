"""Daily Microsoft-news video, in the style of "חידושי מייקרוסופט 20.11" (square 1080, music + captions, no narration).
Usage: python3 video_engine.py spec.json [--still SECONDS]
spec.json (all text Hebrew, HTML allowed: <b> = yellow, <em> = green, <bdi> for English inside Hebrew):
{
  "out": "video.mp4",
  "states_dir": "states",                      # PNGs made with apps.render_states
  "hook": [[["big","..."],["mid","..."]], [["mid","..."],["big","..."]]],   # 2 opening text scenes, 2 lines each
  "intro": {"kicker": "החידוש של השבוע ב-Copilot", "name": "Accounting skills", "sub": "..."},
  "demo": [{"state": "s0", "cap": "pill html", "cam": [cx, cy, zoom], "beats": 8}, ...],   # 4-7 steps
  "example": {"q": "ומה זה אומר<br><em>לאנשי כספים?</em>", "cards": [["📥","title","line"], x3]},
  "warn": {"cards": [["⚠️","title","line"], 1-3 cards], "tip": "נסו קודם על <b>קובץ תרגול</b>"},
  "takeaway": ["mid html line 1", "mid html line 2"]
}
cam: cx, cy = 0..1 point of the screen to center on, zoom 1.0 = whole screen (1.3-1.7 = zoom in).
"""
import json, math, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from apps import FONT_FACE

FPS = 30; BPM = 120; B = 60 / BPM; W = H = 1080
args = sys.argv[1:]
STILL = None
if "--still" in args:
    i = args.index("--still"); STILL = float(args[i + 1]); del args[i:i + 2]
SPEC_PATH = Path(args[0]).resolve(); SPEC = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
BASE = SPEC_PATH.parent
BRAND = json.loads((HERE / "brand.json").read_text(encoding="utf-8")); C = BRAND["colors"]
STATES = (BASE / SPEC.get("states_dir", "states"))
WORK = BASE / "work"; SPR_DIR = WORK / "sprites"; HTML_DIR = WORK / "html"
SPR_DIR.mkdir(parents=True, exist_ok=True); HTML_DIR.mkdir(parents=True, exist_ok=True)


def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


CSS = f"""{FONT_FACE}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;width:1800px;height:1100px;overflow:hidden}}
body{{font-family:'Heebo',Arial,sans-serif;direction:rtl;display:flex;align-items:center;justify-content:center}}
.big{{font-size:140px;font-weight:900;color:#fff;line-height:1.08;text-align:center;text-shadow:0 8px 30px rgba(0,0,0,.45)}}
.mid{{font-size:96px;font-weight:900;color:#fff;line-height:1.15;text-align:center;text-shadow:0 6px 24px rgba(0,0,0,.45)}}
.big em,.mid em,.pill em,.sub em{{font-style:normal;color:{C['accent']}}}
.big b,.mid b,.pill b,.sub b{{color:{C['highlight']}}}
.pill{{font-size:62px;font-weight:800;color:#fff;background:{C['pill_bg']};border-radius:26px;padding:20px 42px;border-right:16px solid {C['accent']};box-shadow:0 14px 40px rgba(0,0,0,.35);white-space:nowrap}}
.card{{width:1000px;background:#fff;border-radius:36px;padding:38px 50px;display:flex;gap:36px;align-items:center;box-shadow:0 20px 60px rgba(0,0,0,.4)}}
.card .ic{{font-size:110px;line-height:1}}
.card h3{{font-size:66px;font-weight:900;color:{C['card_title']};line-height:1.1}}
.card p{{font-size:42px;font-weight:500;color:{C['card_text']};margin-top:10px;line-height:1.3}}
.card.sm{{padding:28px 44px}} .card.sm h3{{font-size:58px}} .card.sm .ic{{font-size:90px}} .card.sm p{{font-size:40px}}
.sub{{font-size:60px;font-weight:700;color:#E8F5E0;text-align:center;line-height:1.3}}
.contact{{font-size:48px;font-weight:700;color:#fff;text-align:center;line-height:1.5}}
.contact div{{direction:ltr;unicode-bidi:isolate}}
.plate{{background:#fff;border-radius:40px;padding:36px 56px;box-shadow:0 14px 40px rgba(0,0,0,.35)}}
.plate img{{width:520px;display:block}}
bdi{{unicode-bidi:isolate;direction:ltr}}
"""


def card(ic, h, p, sm=False):
    return f'<div class="card{" sm" if sm else ""}"><div class="ic">{ic}</div><div><h3>{h}</h3><p>{p}</p></div></div>'


# ---------------------------------------------------------------- timeline (beats)
S = SPEC; SP = {}; SCENES = []; RISERS = []; CALM = []
b = 0
for k, scene in enumerate(S["hook"][:2]):
    items = []
    ys = [400, 660] if len(scene) == 2 else [540]
    for j, (cls, html) in enumerate(scene):
        n = f"h{k}{j}"; SP[n] = f'<div class="{cls}">{html}</div>'; items.append((n, b + 2 * j, b + 8, 540, ys[j]))
    SCENES.append((b, b + 8, "text", items)); b += 8
CALM.append((0, 8))
RISERS.append(b - 8)
it = S["intro"]
SP["ik"] = f'<div class="pill">{it["kicker"]}</div>'; SP["in"] = f'<div class="big">{it["name"]}</div>'; SP["is"] = f'<div class="sub">{it["sub"]}</div>'
SCENES.append((b, b + 8, "text", [("ik", b, b + 8, 540, 260), ("in", b + 1, b + 8, 540, 540), ("is", b + 2, b + 8, 540, 780)])); b += 8
RISERS.append(b - 8)
d0 = b; states = []; cams = []; caps = []
for j, st in enumerate(S["demo"]):
    n = st.get("beats", 8); cx, cy, z = st.get("cam", [0.5, 0.5, 1.0])
    states.append((b, st["state"]))
    cams += [(b, cx, cy, z), (b + n - 1.5, cx, cy, z * 1.04)]
    if st.get("cap"): SP[f"k{j}"] = f'<div class="pill">{st["cap"]}</div>'; caps.append((f"k{j}", b, b + n))
    b += n
SCENES.append((d0, b, "screen", dict(states=states, cam=cams, caps=caps)))
RISERS.append(b - 8)
ex = S["example"]
SP["ex0"] = f'<div class="mid">{ex["q"]}</div>'
SCENES.append((b, b + 6, "text", [("ex0", b, b + 6, 540, 540)])); b += 6
items = []
for j, (ic, h, p) in enumerate(ex["cards"][:3]):
    SP[f"e{j}"] = card(ic, h, p); items.append((f"e{j}", b + 1 + 5 * j, b + 18, 540, [280, 540, 800][j], "right"))
SCENES.append((b, b + 18, "text", items)); b += 18
wa = S["warn"]; SP["w0"] = '<div class="mid">⚠️ חשוב לדעת</div>'
items = [("w0", b, b + 22, 540, 130)]
wc = wa["cards"][:3]; ys = {1: [450], 2: [380, 660], 3: [345, 575, 805]}[len(wc)]
for j, (ic, h, p) in enumerate(wc):
    SP[f"w{j + 1}"] = card(ic, h, p, True); items.append((f"w{j + 1}", b + 3 + 4 * j, b + 22, 540, ys[j], "right"))
SP["wt"] = f'<div class="pill">{wa["tip"]}</div>'; items.append(("wt", b + 15, b + 22, 540, 990))
SCENES.append((b, b + 22, "text", items)); b += 22
RISERS.append(b - 8)
t1, t2 = S["takeaway"][:2]
SP["m1"] = f'<div class="mid">{t1}</div>'; SP["m2"] = f'<div class="mid">{t2}</div>'
SCENES.append((b, b + 16, "text", [("m1", b, b + 16, 540, 390), ("m2", b + 4, b + 16, 540, 660)])); CALM.append((b, b + 16)); b += 16
ec = BRAND["end_card"]
SP["logo"] = f'<div class="plate"><img src="{(HERE / BRAND["logo"]).as_uri()}"></div>'
SP["title"] = f'<div class="big" style="font-size:120px">{BRAND["name"]}</div>'
SP["o1"] = '<div class="sub">סדנאות מעשיות ב-Copilot,<br>Excel ו-Power BI</div>'
SP["o3"] = '<div class="contact">' + "".join(f"<div>{x}</div>" for x in ec["contact_lines"]) + "</div>"
END0 = b; SCENES.append((b, b + 24, "end", None)); b += 24
TOTAL_BEATS = b; DUR = TOTAL_BEATS * B


def render_sprites():
    for name, body in SP.items():
        out = SPR_DIR / f"{name}.png"; f = HTML_DIR / f"{name}.html"
        f.write_text(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")
        subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1800,1100",
                        "--virtual-time-budget=3000", "--force-device-scale-factor=1", "--default-background-color=00000000",
                        "--allow-file-access-from-files", f"--screenshot={out}", f.as_uri()], check=True, capture_output=True)
        im = Image.open(out).convert("RGBA")
        bb = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bb is None: raise SystemExit(f"empty sprite {name}")
        if bb[0] < 5 or bb[2] > 1795: print(f"WARNING: sprite {name} touches the edge – text too long, shorten it")
        im.crop((max(0, bb[0] - 40), max(0, bb[1] - 40), min(1800, bb[2] + 40), min(1100, bb[3] + 40))).save(out)


SPRC = {}
def spr(n):
    if n not in SPRC: SPRC[n] = Image.open(SPR_DIR / f"{n}.png").convert("RGBA")
    return SPRC[n]
IMGC = {}
def img(n):
    if n not in IMGC: IMGC[n] = Image.open(STATES / f"{n}.png").convert("RGB")
    return IMGC[n]


def music(path, seconds):
    sr = 44100; n = int(seconds * sr); out = np.zeros(n)
    rng = np.random.default_rng(31)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def put(sig, start):
        s = int(start * sr)
        if s >= n: return
        e = min(n, s + len(sig)); out[s:e] += sig[:e - s]
    t = lambda d: np.arange(int(d * sr)) / sr
    tk = t(0.35); kick = np.sin(2 * np.pi * np.cumsum(50 + 130 * np.exp(-tk * 32)) / sr) * np.exp(-tk * 7) * 0.9
    tc = t(0.22); nz = rng.standard_normal(len(tc)); clap = (nz - np.convolve(nz, np.ones(6) / 6, "same")) * np.exp(-tc * 22) * 0.33
    th = t(0.06); nh = rng.standard_normal(len(th)); hat = (nh - np.convolve(nh, np.ones(3) / 3, "same")) * np.exp(-th * 70) * 0.16
    prog = [50, 46, 53, 48]
    chords = {50: [50, 53, 57], 46: [46, 50, 53], 53: [53, 57, 60], 48: [48, 52, 55]}
    beats = TOTAL_BEATS + 4; duck = np.ones(n)
    for bb in range(beats):
        tb = bb * B; end = bb >= TOTAL_BEATS - 2
        calm = any(a <= bb < z for a, z in CALM)
        if not end:
            put(kick * (0.75 if calm else 1), tb)
            s = int(tb * sr); e = min(n, s + int(0.25 * sr))
            if s < n: duck[s:e] = np.minimum(duck[s:e], 0.35 + 0.65 * np.linspace(0, 1, e - s))
        if bb % 2 == 1 and not end: put(clap, tb)
        if not end:
            put(hat, tb + B / 2)
            if not calm: put(hat * 0.4, tb + B / 4); put(hat * 0.4, tb + 3 * B / 4)
        root = prog[(bb // 8) % 4]
        if bb >= 16 and not end:
            tbs = t(0.22); f = hz(root - 12); saw = 2 * ((tbs * f) % 1) - 1
            put(np.convolve(saw, np.ones(18) / 18, "same") * np.exp(-tbs * 7) * 0.5, tb + B / 2)
        if bb >= 16 and not end and not calm:
            notes = [m + 12 for m in chords[root]] + [chords[root][2] + 24]
            for k in range(4):
                tl = t(0.11); f = hz(notes[(bb * 4 + k) % 4])
                put((0.6 * np.sign(np.sin(2 * np.pi * f * tl)) + 0.4 * np.sin(2 * np.pi * 2 * f * tl)) * np.exp(-tl * 22) * 0.075, tb + k * B / 4)
    tt = np.arange(n) / sr; pad = np.zeros(n)
    for c in range(beats // 8 + 1):
        root = prog[c % 4]; s0 = int(c * 8 * B * sr); s1 = min(n, int((c + 1) * 8 * B * sr))
        if s0 >= n: break
        seg = tt[s0:s1] - tt[s0]
        pad[s0:s1] = sum(2 * ((seg * hz(m) * (1 + d)) % 1) - 1 for m in chords[root] for d in (0, 0.004)) * 0.025
    out += np.convolve(pad, np.ones(12) / 12, "same") * duck
    for rb in RISERS:
        if rb < 0: continue
        rs = int(rb * B * sr); re_ = min(n, int((rb + 8) * B * sr))
        noise = rng.standard_normal(re_ - rs) * np.linspace(0, 0.12, re_ - rs) ** 1.5
        out[rs:re_] += noise - np.convolve(noise, np.ones(4) / 4, "same")
    f = int(2 * sr); out[-f:] *= np.linspace(1, 0, f)
    out = np.tanh(out * 1.6); out /= np.abs(out).max() / 0.9
    st = np.stack([out, np.roll(out, 220) * 0.92 + out * 0.08], 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype("<i2").tobytes())


def ease_back(x):
    c1, c3 = 1.70158, 2.70158; x = min(1, max(0, x)); return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def bt(x): return x * B
def punch(now, amt=0.03): return 1 + amt * math.exp(-((now % B) / B) * 7)


def put_sprite(canvas, name, cx, cy, t_in, t_out, now, max_w=980, slide=None, max_h=None):
    if now < t_in or now >= t_out: return
    im = spr(name); base = min(1.0, max_w / im.width)
    if max_h: base = min(base, max_h / im.height)
    a = ease_back((now - t_in) / 0.28); o = 1.0
    if t_out - now < 0.12: o = (t_out - now) / 0.12
    s = base * max(0.05, a) * (0.85 + 0.15 * o)
    w, hh = max(1, int(im.width * s)), max(1, int(im.height * s))
    sp = im.resize((w, hh), Image.BILINEAR)
    if o < 1: sp.putalpha(sp.getchannel("A").point(lambda v: int(v * o)))
    dx = int((1 - min(1, (now - t_in) / 0.25)) ** 2 * 800) if slide == "right" else 0
    canvas.alpha_composite(sp, (int(cx - w / 2 + dx), int(cy - hh / 2)))


class Background:
    def __init__(self):
        y, x = np.mgrid[0:H * 2, 0:W * 2]; g = np.zeros((H * 2, W * 2, 3))
        for cx, cy, col, r in [(700, 700, hexrgb(C["bg_mid"]), 900), (1500, H * 2 - 500, hexrgb(C["bg_deep"]), 900)]:
            d = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r ** 2)); g += d[..., None] * np.array(col) * 0.85
        g += np.array(hexrgb(C["bg_dark"])) * 0.55; g += (((x + y) // 40 % 2 == 0) * 5)[..., None]
        self.img = Image.fromarray(np.clip(g, 0, 255).astype("uint8")); self.acc = Image.new("RGB", (W, H), hexrgb(C["accent"]))
    def at(self, now):
        ox = int(W * 0.3 + 250 * math.sin(now * 0.6)); oy = int(H * 0.3 + 250 * math.cos(now * 0.45))
        im = self.img.crop((ox, oy, ox + W, oy + H)); pulse = math.exp(-((now % B) / B) * 6) * 0.18
        if pulse > 0.01: im = Image.blend(im, self.acc, pulse * 0.25)
        return im.convert("RGBA")


def lerp_keys(keys, now):
    if now <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *bb) in zip(keys, keys[1:]):
        if now <= t1:
            k = ease((now - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(x + (y - x) * k for x, y in zip(a, bb))
    return keys[-1][1:]


def view(src, cx, cy, zoom, w, h):
    sw, sh = src.size; vw = sw / zoom; vh = vw * h / w
    if vh > sh: vh = sh; vw = vh * w / h
    x0 = min(max(0, cx * sw - vw / 2), sw - vw); y0 = min(max(0, cy * sh - vh / 2), sh - vh)
    return src.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((w, h), Image.LANCZOS if vw > w else Image.BICUBIC)


CARD = (40, 36, 1040, 856); CAP_Y = 962


def screen_card(canvas, im):
    x0, y0, x1, y1 = CARD
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 10, y0 + 16, x1 + 10, y1 + 16), 30, fill=(0, 0, 0, 90)); canvas.alpha_composite(sh)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 30, fill=255)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); lay.paste(im, (0, 0), mask); canvas.alpha_composite(lay, (x0, y0))


def frame(BG, now):
    si = max(i for i, s in enumerate(SCENES) if now >= bt(s[0])); s0, s1, kind, data = SCENES[si]
    canvas = BG.at(now)
    if kind == "text":
        for sp in data:
            name, a, b_, cx, cy = sp[:5]; slide = sp[5] if len(sp) > 5 else None
            mh = 260 if name in ("w1", "w2", "w3") else (330 if name in ("e0", "e1", "e2") else None)
            put_sprite(canvas, name, cx, cy, bt(a), bt(b_), now, max_w=980, slide=slide, max_h=mh)
    elif kind == "screen":
        x0, y0, x1, y1 = CARD; w, h = x1 - x0, y1 - y0
        cx, cy, z = lerp_keys([(bt(k[0]), *k[1:]) for k in data["cam"]], now); z *= punch(now, 0.012)
        st = data["states"]; cur = max(i for i, q in enumerate(st) if now >= bt(q[0]))
        im = view(img(st[cur][1]), cx, cy, z, w, h); since = now - bt(st[cur][0])
        if cur > 0 and since < 0.25: im = Image.blend(view(img(st[cur - 1][1]), cx, cy, z, w, h), im, ease(since / 0.25))
        screen_card(canvas, im)
        for name, a, b_ in data["caps"]: put_sprite(canvas, name, 540, CAP_Y, bt(a), bt(b_), now, max_w=1020)
    elif kind == "end":
        e, z = END0, TOTAL_BEATS
        put_sprite(canvas, "logo", 540, 250, bt(e), bt(z), now, max_w=560)
        put_sprite(canvas, "title", 540, 500, bt(e + .5), bt(z), now, max_w=900)
        put_sprite(canvas, "o1", 540, 690, bt(e + 2), bt(z), now, max_w=980)
        put_sprite(canvas, "o3", 540, 900, bt(e + 4), bt(z), now, max_w=900)
    since = now - bt(s0)
    if since < 0.15 and si > 0:
        canvas = Image.blend(canvas, Image.new("RGBA", canvas.size, (255, 255, 255, 255)), 0.5 * (1 - since / 0.15))
    return canvas


def build():
    BG = Background()
    if STILL is not None:
        out = BASE / f"still_{STILL:06.2f}.png"; frame(BG, STILL).convert("RGB").save(out); print("still", out); return
    wav = WORK / "music.wav"; music(wav, DUR + 0.5)
    out = BASE / SPEC.get("out", "video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "2M", "-bufsize", "4M", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
        enc.stdin.write(frame(BG, fi / FPS).convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
    print(f"done {out}  {DUR:.1f}s  {out.stat().st_size / 1e6:.1f}MB")


if __name__ == "__main__":
    print(f"timeline: {TOTAL_BEATS} beats = {DUR:.1f}s")
    if not (40 <= DUR <= 120): print("WARNING: duration outside 40-120 s – adjust demo beats")
    if STILL is None or not all((SPR_DIR / f"{n}.png").exists() for n in SP): render_sprites()
    build()
