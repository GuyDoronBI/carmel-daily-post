CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:1050px;overflow:hidden;background:#fff}
body{font-family:'Heebo','Segoe UI',Arial,sans-serif;direction:rtl;color:#222;font-size:20px}
.app{display:flex;flex-direction:column;height:1050px}
.tbar{height:46px;background:#1D6F42;color:#fff;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:500;position:relative}
.tbar .l{position:absolute;right:18px;font-weight:800;font-size:22px}
.tabs{height:44px;background:#F3F3F3;display:flex;gap:30px;align-items:flex-end;padding:0 22px;font-size:18px;color:#444}
.tabs span{padding-bottom:9px}
.tabs .on{color:#1D6F42;font-weight:700;border-bottom:4px solid #1D6F42}
.ribbon{height:78px;background:#F8F8F8;border-bottom:1px solid #DDD;display:flex;gap:16px;align-items:center;padding:0 22px}
.rb{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:15px;color:#444;min-width:64px}
.rb i{font-style:normal;font-size:28px;line-height:1}
.rb.cp{background:#EEF0FF;border-radius:10px;padding:6px 10px;color:#3B2DB8;font-weight:700}
.rb.hot{outline:4px solid #FFB000;border-radius:10px;background:#FFF4D6}
.sep{width:1px;height:52px;background:#DDD}
.fbar{height:42px;display:flex;align-items:center;border-bottom:1px solid #DDD;font-size:18px}
.fbar .nb{width:110px;text-align:center;border-left:1px solid #DDD;height:100%;display:flex;align-items:center;justify-content:center}
.fbar .fx{width:46px;text-align:center;color:#888;font-style:italic;border-left:1px solid #DDD}
.fbar .v{padding:0 14px;direction:ltr;text-align:right;flex:1}
.main{flex:1;display:flex;min-height:0}
.gridwrap{flex:1;overflow:hidden;background:#fff}
table.g{border-collapse:collapse;font-size:19px}
table.g td,table.g th{border:1px solid #E1E1E1;height:41px;padding:0 10px;white-space:nowrap}
table.g th{background:#F3F3F3;color:#555;font-weight:500;font-size:16px}
table.g th.rn{width:46px}
table.g td.h{background:#1D6F42;color:#fff;font-weight:700}
table.g td.n{text-align:left;direction:ltr}
table.g td.sp{background:#FFF1B8;outline:3px solid #E0A800;outline-offset:-3px}
table.g td.dt{background:#FFE0C7;outline:3px solid #E8833A;outline-offset:-3px}
table.g td.tx{background:#E3EEFF;outline:3px solid #1F70C1;outline-offset:-3px}
table.g tr.dup td{background:#FFD9DB}
table.g tr.dup td.rn2{outline:none}
table.g td.fixed{background:#E2F5D8}
table.g td.neg{color:#C62828;font-weight:700}
table.g td.pos{color:#2E7D32;font-weight:700}
table.g td.tot{font-weight:800;background:#EEF5EA}
.pane{width:450px;border-right:1px solid #D6D6E8;background:#FAFAFF;display:flex;flex-direction:column}
.pane .ph{height:58px;display:flex;align-items:center;gap:12px;padding:0 18px;font-size:22px;font-weight:800;border-bottom:1px solid #E3E3F0}
.logo{width:34px;height:34px;border-radius:10px;background:conic-gradient(from 200deg,#2B7FFF,#8B3DFF,#FF4FA3,#FFB13D,#2B7FFF)}
.pane .body{flex:1;padding:18px;display:flex;flex-direction:column;gap:14px;overflow:hidden}
.msg{background:#fff;border:1px solid #E3E3F0;border-radius:14px;padding:14px 16px;font-size:18px;line-height:1.45;box-shadow:0 2px 6px rgba(40,40,90,.06)}
.msg.me{background:#E9E6FF;border:none;align-self:flex-start;max-width:92%}
.msg h4{font-size:19px;margin-bottom:8px}
.iss{display:flex;align-items:center;gap:10px;padding:7px 0;border-top:1px solid #EEE;font-size:17.5px}
.iss:first-of-type{border-top:none}
.cb{width:22px;height:22px;border-radius:5px;background:#5B4BDB;color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center;flex:none}
.iss b{margin-right:auto;color:#666;font-weight:500;font-size:16px}
.btn{display:inline-block;background:#5B4BDB;color:#fff;border-radius:10px;padding:9px 20px;font-weight:700;font-size:18px;margin-top:10px}
.btn.glow{box-shadow:0 0 0 5px #FFB000}
.step{display:flex;gap:10px;align-items:center;padding:5px 0;font-size:17.5px}
.ok{color:#2E7D32;font-weight:800}
.inp{margin:14px 18px 18px;border:2px solid #8C80F0;border-radius:14px;background:#fff;min-height:64px;padding:16px;font-size:19px;display:flex;align-items:center;gap:8px}
.inp .ph2{color:#999}
.inp .at{color:#5B4BDB;font-weight:800;direction:ltr}
.caret{display:inline-block;width:2px;height:24px;background:#333}
.chip{display:inline-block;background:#EEF0FF;color:#3B2DB8;border-radius:8px;padding:2px 10px;font-weight:700;direction:ltr}
.status{height:32px;background:#F3F3F3;border-top:1px solid #DDD;display:flex;align-items:center;gap:26px;padding:0 18px;font-size:15px;color:#555}
.sheets{display:flex;gap:4px}
.sheets span{padding:3px 14px}
.sheets .on{background:#fff;color:#1D6F42;font-weight:700;border-bottom:3px solid #1D6F42}
/* power query */
.pq{display:flex;flex-direction:column;height:1050px}
.pq .tbar{background:#1D6F42}
.pqmain{flex:1;display:flex;min-height:0}
.qlist{width:230px;background:#F5F5F5;border-left:1px solid #DDD;padding:14px;font-size:17px}
.qlist .q{background:#DCEBDD;border-radius:6px;padding:8px 10px;font-weight:700;margin-top:10px}
.prev{flex:1;padding:0;overflow:hidden}
.steps{width:330px;background:#FAFAFA;border-right:1px solid #DDD;padding:16px;font-size:18px}
.steps h5{font-size:17px;color:#666;margin:6px 0 10px;font-weight:600}
.steps .s{padding:8px 10px;border-radius:6px;display:flex;gap:10px;align-items:center}
.steps .s.on{background:#D6E8FF;font-weight:700}
.steps .s i{font-style:normal;color:#888}
.mbar{height:44px;border-bottom:1px solid #DDD;display:flex;align-items:center;padding:0 14px;font-family:Consolas,monospace;font-size:16px;direction:ltr;color:#333;background:#fff}
/* planner */
.pl{display:flex;flex-direction:column;height:1050px;background:#F6F7FB}
.pl .tbar{background:#2E6B4F}
.plmain{flex:1;display:flex;min-height:0}
.nav{width:280px;background:#fff;border-left:1px solid #E2E4EC;padding:18px 14px;font-size:18px}
.nav .sec{color:#777;font-size:15px;font-weight:700;margin:18px 6px 8px}
.nav .it{padding:9px 12px;border-radius:8px;display:flex;gap:10px;align-items:center}
.nav .it.on{background:#E6F2EC;color:#1E6B47;font-weight:700}
.nav .it.hot{outline:3px solid #FFB000;background:#FFF4D6}
.content{flex:1;padding:22px 26px;overflow:hidden}
.content h2{font-size:28px;margin-bottom:6px}
.vtabs{display:flex;gap:26px;border-bottom:2px solid #E2E4EC;margin:12px 0 18px;font-size:18px;color:#555}
.vtabs span{padding:8px 2px}
.vtabs .on{color:#1E6B47;font-weight:800;border-bottom:4px solid #1E6B47;margin-bottom:-2px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.pc{background:#fff;border-radius:14px;padding:16px 18px;box-shadow:0 2px 8px rgba(30,40,80,.08);font-size:17px}
.pc h3{font-size:20px;margin-bottom:6px}
.pc .k{display:inline-block;border-radius:8px;padding:2px 10px;font-size:14px;font-weight:700;margin-bottom:10px}
.k1{background:#E7F0FF;color:#1F5FBF}.k2{background:#E6F2EC;color:#1E6B47}.k3{background:#F4E9FF;color:#7A3DBF}
.bar{height:10px;border-radius:5px;background:#E9ECF3;margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%;background:#36A16B}
.cap{background:#fff;border-radius:14px;padding:10px 20px;box-shadow:0 2px 8px rgba(30,40,80,.08)}
.crow{display:flex;align-items:center;gap:16px;padding:13px 0;border-top:1px solid #EEF0F5;font-size:19px}
.crow:first-child{border-top:none}
.av{width:44px;height:44px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;flex:none}
.crow .nm{width:120px;font-weight:700}
.cbar{flex:1;height:30px;background:#EEF0F5;border-radius:8px;position:relative;overflow:hidden}
.cbar i{position:absolute;top:0;bottom:0;right:0;border-radius:8px}
.cbar .lim{position:absolute;top:-4px;bottom:-4px;width:3px;background:#333}
.crow .num{width:280px;white-space:nowrap;text-align:left;font-weight:700}
.crow.over{background:#FFF0F0;border-radius:10px;padding-right:8px;padding-left:8px;outline:3px solid #E53935}
table.pg{border-collapse:collapse;width:100%;background:#fff;border-radius:12px;overflow:hidden;font-size:18px;box-shadow:0 2px 8px rgba(30,40,80,.08)}
table.pg th{background:#F0F2F7;color:#555;font-weight:700;padding:11px 12px;text-align:right;font-size:16px}
table.pg td{padding:11px 12px;border-top:1px solid #EEF0F5;white-space:nowrap}
table.pg td.red{background:#FFDADA;color:#B71C1C;font-weight:700}
table.pg td.yel{background:#FFF1B8;color:#7A5A00;font-weight:700}
table.pg td.grn{background:#DDF3E4;color:#1B5E20;font-weight:700}
table.pg tr.sel td{outline:none;background-color:#EEF4FF}
.hist{width:360px;background:#fff;border-right:1px solid #E2E4EC;padding:20px;font-size:17px}
.hist h3{font-size:21px;margin-bottom:4px}
.hist .sub{color:#777;font-size:15px;margin-bottom:14px}
.ev{display:flex;gap:12px;padding:10px 0;border-top:1px solid #F0F0F0}
.ev .dot{width:12px;height:12px;border-radius:50%;background:#36A16B;margin-top:7px;flex:none}
.ev small{display:block;color:#888;font-size:14px}
.hl{outline:4px solid #FFB000 !important;outline-offset:-2px}
"""

COLS = "ABCDEFGH"


def grid(rows, ncols=6, nrows=None, start=1, colw=None, classes=None, rowcls=None):
    """rows: list of lists of cell text. classes[(r,c)] -> css class. Column A is on the right (RTL)."""
    classes = classes or {}; rowcls = rowcls or {}
    nrows = nrows or len(rows) + 6
    colw = colw or [150] * ncols
    h = '<table class="g"><tr><th class="rn"></th>' + "".join(f'<th style="width:{colw[i]}px">{COLS[i]}</th>' for i in range(ncols)) + "</tr>"
    for r in range(nrows):
        rr = rows[r] if r < len(rows) else [""] * ncols
        h += f'<tr class="{rowcls.get(r, "")}"><th class="rn">{start + r}</th>'
        for c in range(ncols):
            v = rr[c] if c < len(rr) else ""
            cl = classes.get((r, c), "")
            if r == 0 and v: cl += " h"
            if isinstance(v, str) and v.strip().replace(",", "").replace(".", "").replace("-", "").replace("%", "").replace("₪", "").strip().isdigit() and r > 0:
                cl += " n"
            h += f'<td class="{cl}">{v.replace(" ", "&nbsp;") if isinstance(v, str) else v}</td>'
        h += "</tr>"
    return h + "</table>"


def excel(file, body_grid, pane=None, fbar=("A1", ""), tab="בית", hot=None, sheets=("גיליון1",), sheet_on=0, ribbon=None):
    tabs = "".join(f'<span class="{"on" if t == tab else ""}">{t}</span>' for t in ["קובץ", "בית", "הוספה", "נוסחאות", "נתונים", "סקירה", "תצוגה"])
    ribbon = ribbon or [("📋", "הדבק"), ("B", "מודגש"), ("🎨", "מילוי"), "|", ("∑", "סכום"), ("⇅", "מיון וסינון"), ("🔍", "חיפוש"), "|", ("✨", "Copilot", "cp")]
    rb = ""
    for x in ribbon:
        if x == "|": rb += '<div class="sep"></div>'; continue
        cls = "rb" + (" " + x[2] if len(x) > 2 else "") + (" hot" if hot == x[1] else "")
        rb += f'<div class="{cls}"><i>{x[0]}</i>{x[1]}</div>'
    sh = "".join(f'<span class="{"on" if i == sheet_on else ""}">{s}</span>' for i, s in enumerate(sheets))
    pane_html = ""
    if pane:
        pane_html = f'<div class="pane"><div class="ph"><div class="logo"></div>Copilot</div><div class="body">{pane[0]}</div><div class="inp">{pane[1]}</div></div>'
    return f'''<div class="app"><div class="tbar"><span class="l">X</span>{file}</div><div class="tabs">{tabs}</div>
<div class="ribbon">{rb}</div>
<div class="fbar"><div class="nb">{fbar[0]}</div><div class="fx">fx</div><div class="v">{fbar[1]}</div></div>
<div class="main"><div class="gridwrap">{body_grid}</div>{pane_html}</div>
<div class="status"><div class="sheets">{sh}</div><span style="margin-right:auto">מוכן</span></div></div>'''



def typing(text, n):
    return f'<span>{text[:n]}</span><span class="caret"></span>' if n else '<span class="ph2">שאלו את Copilot או הקלידו @ לכישורים</span><span class="caret"></span>'


