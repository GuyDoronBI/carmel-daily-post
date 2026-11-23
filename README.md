# carmel-daily-post

מנועים קבועים לפוסט השיווקי היומי של כרמל הדרכה: גרפיקה לפוסט וסרטון קצר (דקה עד דקה וחצי) על חידוש של מייקרוסופט.

## מבנה
- `engine/` – מנוע הסרטון: `video_engine.py` (סרטון ריבועי 1080, מוזיקה וכתוביות, בלי קריינות), `apps.py` + `_base.py` (מסכי תוכנה משוחזרים: Excel, Copilot, Power BI ותבנית כללית ל-Planner/Visio/Azure), מיתוג (`brand.json`, `logo.svg`) וגופן Heebo.
- `post/` – מנוע הגרפיקה לפוסט: `render.py` + `template.html` + `logo.png`.
- `examples/` – דוגמה שנבדקה (Accounting skills, 23.11.2026): `states_day.py`, `spec.json`, `data.json`.

## שימוש יומי
1. מעתיקים את `examples/` לתיקיית עבודה ומשנים: `states_day.py` (המסכים), `spec.json` (תסריט), `data.json` (גרפיקה).
2. `python3 states_day.py`
3. `python3 <repo>/engine/video_engine.py spec.json` → `video.mp4` (בדיקה מהירה: `--still 50`)
4. `python3 <repo>/post/render.py data.json post.png`

דרישות: python3 עם numpy ו-Pillow, google-chrome, ffmpeg.
