"""Recreated Microsoft app screens (fictitious data) rendered to PNG with headless Chrome.
Use from a daily states script:
    import sys; sys.path.insert(0, ENGINE_DIR); from apps import *
    S = {}
    S["s0"] = excel("קובץ.xlsx", grid(ROWS, 5, 16, colw=[150]*5), pane=(msg_html, typing("", 0)))
    render_states(S, "states")
Every state is a 1280x1050 page rendered at 1.5x -> 1920x1575 PNG.
Helpers: grid, excel, typing, copilot_app, powerbi, generic_app, msg, me, steps, btn.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
exec(open(HERE / "_base.py", encoding="utf-8").read())  # CSS, COLS, grid, excel, typing

FONT_FACE = "".join(
    f"@font-face{{font-family:'Heebo';font-weight:{w};src:url('{(HERE / 'fonts' / f'heebo-{sub}-{w}-normal.woff2').as_uri()}') format('woff2')}}"
    for w in (400, 500, 700, 800, 900) for sub in ("hebrew", "latin"))

CSS += """
/* Copilot app / Cowork */
.cpa{display:flex;flex-direction:column;height:1050px;background:#F7F7FB}
.cpa .top{height:56px;background:#fff;border-bottom:1px solid #E6E6F0;display:flex;align-items:center;gap:12px;padding:0 22px;font-size:20px;font-weight:800}
.cpmain{flex:1;display:flex;min-height:0}
.cpnav{width:250px;background:#fff;border-left:1px solid #E6E6F0;padding:16px 12px;font-size:17px}
.cpnav .it{padding:9px 12px;border-radius:8px;display:flex;gap:10px;align-items:center;color:#333}
.cpnav .it.on{background:#EEF0FF;color:#3B2DB8;font-weight:700}
.cpnav .it.hot{outline:3px solid #FFB000;background:#FFF4D6}
.cpnav .sec{color:#888;font-size:14px;font-weight:700;margin:16px 8px 6px}
.chat{flex:1;display:flex;flex-direction:column;min-width:0}
.chat .body{flex:1;padding:26px 60px;display:flex;flex-direction:column;gap:16px;overflow:hidden}
.chat .msg{font-size:19px}
.chat .inp{margin:0 60px 26px}
.art{background:#fff;border:1px solid #E3E3F0;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(40,40,90,.08)}
.art .ah{background:#1D6F42;color:#fff;font-weight:700;padding:8px 14px;font-size:16px}
/* Power BI */
.pbi{display:flex;flex-direction:column;height:1050px;background:#F3F2F1}
.pbi .tbar{background:#F2C811;color:#222}
.pbimain{flex:1;display:flex;min-height:0}
.canvas{flex:1;padding:22px;display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:min-content;gap:16px;overflow:hidden}
.viz{background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.12);padding:14px 16px;font-size:16px}
.viz h4{font-size:16px;color:#444;margin-bottom:8px;font-weight:700}
.viz .big{font-size:40px;font-weight:800;color:#222}
.viz.w2{grid-column:span 2}.viz.w3{grid-column:span 3}
.bars{display:flex;align-items:flex-end;gap:12px;height:180px;padding-top:10px}
.bars div{flex:1;background:#118DFF;border-radius:4px 4px 0 0;position:relative}
.bars div span{position:absolute;bottom:-24px;left:0;right:0;text-align:center;font-size:13px;color:#555}
.fields{width:250px;background:#fff;border-right:1px solid #DDD;padding:14px;font-size:16px}
.fields .f{padding:6px 4px;display:flex;gap:8px}
/* generic app */
.ga{display:flex;flex-direction:column;height:1050px;background:#F6F7FB}
.gamain{flex:1;display:flex;min-height:0}
"""

PAGE = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{ff}{css}</style></head><body>{body}</body></html>'


def msg(html): return f'<div class="msg">{html}</div>'
def me(html): return f'<div class="msg me">{html}</div>'
def btn(text, glow=False): return f'<div class="btn{" glow" if glow else ""}">{text}</div>'
def steps(title, items, note=""):
    s = "".join(f'<div class="step"><span class="ok">✓</span>{x}</div>' for x in items)
    return f'<div class="msg"><h4>{title}</h4>{s}{f"<div style=margin-top:8px;color:#555;font-size:16px>{note}</div>" if note else ""}</div>'


def _pane(pane):
    if not pane: return ""
    return f'<div class="pane"><div class="ph"><div class="logo"></div>Copilot</div><div class="body">{pane[0]}</div><div class="inp">{pane[1]}</div></div>'


def copilot_app(chat_html, input_html, title="Microsoft 365 Copilot", nav=None, nav_on="Chat", hot=None):
    nav = nav or ["Chat", "Cowork", "Agents &amp; Plugins", "Automations", "Projects", "Workspaces"]
    items = "".join(f'<div class="it{" on" if n == nav_on else ""}{" hot" if n == hot else ""}">{n}</div>' for n in nav)
    return f'''<div class="cpa"><div class="top"><div class="logo"></div>{title}</div>
<div class="cpmain"><div class="cpnav">{items}</div><div class="chat"><div class="body">{chat_html}</div><div class="inp">{input_html}</div></div></div></div>'''


def powerbi(file, visuals_html, fields=None, pane=None, tab="דף הבית"):
    tabs = "".join(f'<span class="{"on" if t == tab else ""}">{t}</span>' for t in ["קובץ", "דף הבית", "הוספה", "מידול", "תצוגה", "עזרה"])
    f = f'<div class="fields"><b>נתונים</b>{"".join(f"<div class=f>☐ {x}</div>" for x in fields)}</div>' if fields else ""
    return f'''<div class="pbi"><div class="tbar"><span class="l">Power BI</span>{file}</div><div class="tabs">{tabs}</div>
<div class="pbimain"><div class="canvas">{visuals_html}</div>{f}{_pane(pane)}</div></div>'''


def generic_app(app, color, title, nav, nav_on, content_html, pane=None, hot=None):
    """Planner / Teams / Outlook / Visio / Azure portal / SharePoint etc. nav: list of item names."""
    items = "".join(f'<div class="it{" on" if n == nav_on else ""}{" hot" if n == hot else ""}">{n}</div>' for n in nav)
    return f'''<div class="ga"><div class="tbar" style="background:{color}"><span class="l">{app}</span>{title}</div>
<div class="gamain"><div class="nav">{items}</div><div class="content">{content_html}</div>{_pane(pane)}</div></div>'''


def render_states(states, outdir="states", chrome="google-chrome"):
    out = Path(outdir).resolve(); out.mkdir(parents=True, exist_ok=True)
    html = out / "_html"; html.mkdir(exist_ok=True)
    for name, body in states.items():
        f = html / f"{name}.html"
        f.write_text(PAGE.format(ff=FONT_FACE, css=CSS, body=body), encoding="utf-8")
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1280,1050",
                        "--force-device-scale-factor=1.5", "--allow-file-access-from-files", "--virtual-time-budget=3000",
                        f"--screenshot={out / (name + '.png')}", f.as_uri()], check=True, capture_output=True)
    print("states:", len(states))
