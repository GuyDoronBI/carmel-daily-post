"""Post graphic (1080x1080 PNG). Usage: python3 render.py data.json out.png
data.json: {"kicker","headline","subtitle","caveat","cards":[{"product","title","line"} x3]}"""
import sys, json, subprocess, base64
from pathlib import Path
HERE = Path(__file__).parent
d = json.load(open(sys.argv[1], encoding="utf-8")); out = Path(sys.argv[2]).resolve()
colors = {"Excel": "#16A34A", "Power BI": "#CA8A04", "Copilot": "#7C3AED", "Azure": "#2563EB", "Planner": "#059669",
          "Visio": "#1D4ED8", "Office 365": "#DC2626", "Microsoft 365": "#DC2626"}
cards = ""
for i, c in enumerate(d["cards"], 1):
    cards += f'<div class="card"><div class="num">{i}</div><div class="txt"><span class="badge" style="background:{colors.get(c["product"], "#475569")}">{c["product"]}</span><div class="t">{c["title"]}</div><div class="d">{c["line"]}</div></div></div>'
h = (HERE / "template.html").read_text(encoding="utf-8")
for k in ["KICKER", "HEADLINE", "SUBTITLE", "CAVEAT"]: h = h.replace("{{" + k + "}}", d[k.lower()])
h = h.replace("{{CARDS}}", cards).replace("{{LOGO}}", base64.b64encode((HERE / "logo.png").read_bytes()).decode())
tmp = out.with_suffix(".html"); tmp.write_text(h, encoding="utf-8")
subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1080,1080",
                "--screenshot=" + str(out), tmp.as_uri()], check=True, capture_output=True)
tmp.unlink(); print("post", out)
