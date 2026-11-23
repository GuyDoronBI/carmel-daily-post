"""Example daily screens (Accounting skills, 23.11.2026). Copy and adapt each day."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "engine"))
from apps import *
FILE = "התאמת בנק – אוקטובר.xlsx"
HDR = ["תאריך", "אסמכתא", "תיאור", "ספרים", "בנק"]
ROWS = [HDR,
 ["02/10/2026", "1041", "קבלה – לקוח אלפא", "18,400", "18,400"],
 ["05/10/2026", "1042", "תשלום ספק – סופטקום", "-5,300", "-5,300"],
 ["08/10/2026", "1043", "קבלה – לקוח בטא", "12,750", "12,750"],
 ["12/10/2026", "1044", "תשלום שכירות", "-9,800", "-9,800"],
 ["15/10/2026", "1045", "קבלה – לקוח גמא", "7,200", "7,020"],
 ["19/10/2026", "1046", "תשלום ספק – שליח מהיר", "-3,410", "-3,410"],
 ["24/10/2026", "1047", "המחאה 5521", "-2,600", ""],
 ["31/10/2026", "—", "עמלות בנק", "", "-85"],
 ["31/10/2026", "", "יתרת סגירה", "17,240", "19,575"],
]
CW = [140, 110, 260, 120, 120]
cls = {(5, 3): "dt", (5, 4): "dt", (7, 3): "sp", (7, 4): "sp", (8, 3): "tx", (8, 4): "tx"}
for c in range(5): cls[(9, c)] = "tot"
G0 = grid(ROWS, 5, 15, colw=CW, classes={(9, c): "tot" for c in range(5)})
G1 = grid(ROWS, 5, 15, colw=CW, classes=cls)
P = "תתאים בין הספרים לדף הבנק של אוקטובר ותציע פקודות יומן להפרשים"
ME = me(P)
FOUND = '''<div class="msg"><h4>מצאתי 3 הפרשים:</h4>
<div class="iss"><span class="cb">1</span>קבלה 1045 – הפרש סכום<b>180 ₪</b></div>
<div class="iss"><span class="cb">2</span>המחאה 5521 – טרם נפרעה<b>2,600 ₪</b></div>
<div class="iss"><span class="cb">3</span>עמלות בנק – לא נרשמו<b>85 ₪</b></div></div>'''
JE = '''<div class="msg"><h4>פקודת יומן מוצעת (טיוטה)</h4>
<div class="iss">ח׳ הוצאות עמלות בנק<b>85</b></div>
<div class="iss">ז׳ בנק<b>85</b></div>
<div class="step"><span class="ok">✓</span>חובה = זכות</div>
<div class="btn glow">הוסף לגיליון לבדיקה</div></div>'''
AUDIT = '<div class="msg"><span class="ok">✓</span> נוסף גיליון "פקודות יומן".<br>נשמר תיעוד: מה שונה ולמה.<br>ההחלטה הסופית – שלכם.</div>'
JG = grid([["תאריך", "חשבון", "חובה", "זכות", "הערה"],
           ["31/10/2026", "הוצאות עמלות בנק", "85", "", "לפי דף הבנק"],
           ["31/10/2026", "בנק", "", "85", ""],
           ["", "סה\"כ", "85", "85", "מאוזן ✓"]], 5, 15, colw=[140, 220, 110, 110, 170],
          classes={(1, 1): "fixed", (1, 2): "fixed", (2, 3): "fixed", (3, 2): "tot", (3, 3): "tot", (3, 4): "tot", (3, 1): "tot"})
SH = ("ספרים מול בנק", "פקודות יומן")
S = {}
S["s0"] = excel(FILE, G0, fbar=("D11", "=SUM(D2:D10)"), sheets=SH)
S["s1"] = excel(FILE, G0, pane=(msg("היי! במה אפשר לעזור עם החוברת הזאת?"), typing(P, len(P))), fbar=("A1", "תאריך"), hot="Copilot", sheets=SH)
S["s2"] = excel(FILE, G1, pane=(ME + FOUND, typing("", 0)), fbar=("E6", "7,020"), sheets=SH)
S["s3"] = excel(FILE, G1, pane=(ME + JE, typing("", 0)), fbar=("E9", "-85"), sheets=SH)
S["s4"] = excel(FILE, JG, pane=(ME + AUDIT, typing("", 0)), fbar=("C4", "=SUM(C2:C3)"), sheets=SH, sheet_on=1)
render_states(S, Path(__file__).resolve().parent / "states")
