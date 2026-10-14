"""Build the BanglaKnight site.

Page bodies live in src/<slug>.html. This script wraps each one in the shared
header, menu and footer, fills in the dates, and writes the finished pages:
src/home.html -> index.html, src/data.html -> data/index.html, and so on.

Run after any edit:  python3 build.py
Change a date:       edit DATES below, then run the script (it fills the home-page card).
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (ISO date used for the countdown, label shown, milestone)
DATES = [
    ("2026-10-20", "Oct 20, 2026", "Training and development data release"),
    ("2026-10-20", "Oct 20, 2026", "CodaBench registration opens"),
    ("2027-01-15", "Jan 15, 2027", "Test data release / evaluation begins"),
    ("2027-01-24", "Jan 24, 2027", "Registration deadline"),
    ("2027-01-31", "Jan 31, 2027", "System submission deadline"),
    ("2027-02-03", "Feb 3, 2027", "Official results released"),
    ("2027-02-15", "Feb 15, 2027", "Shared-task paper submission deadline"),
    ("2027-03-26", "Mar 26, 2027", "Notification of acceptance"),
    ("2027-04-16", "Apr 16, 2027", "Camera-ready paper due"),
    ("2027-06-01", "Jun 1–5, 2027", "Workshop at NAACL 2027, San Francisco"),
]

# slug, menu label, page title, one-line description, header photo, icon
PAGES = [
    ("home", "Home", "BanglaKnight", "Shared Task 1 at BLP 2027: classify Bangla prompts into four risk levels.", "sf-golden-gate.jpg", None),
    ("data", "Data", "Data", "What you get, the three written forms, and the starter kit.", "sf-skyline.jpg", "data"),
    ("leaderboard", "Leaderboard", "Leaderboard", "Metrics and official results.", "sf-painted-ladies.jpg", "trophy"),
    ("participate", "Participate", "Participate", "From registration on CodaBench to your final submission.", "sf-golden-gate.jpg", "flag"),
    ("paper", "Paper Submission", "Paper Submission", "How to write and submit your system description paper.", "sf-painted-ladies.jpg", "paper"),
    ("organizers", "Organizers", "Organizers", "Who runs the task and how to reach us.", "sf-skyline.jpg", None),
]

# Old addresses that now point elsewhere: path -> target
REDIRECTS = {"task": "/#task", "dates": "/"}

# Line icons (24x24, drawn with the current text color)
ICONS = {
    "data": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "trophy": '<path d="M8 21h8"/><path d="M12 16v5"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3"/><path d="M7 5H4v2a3 3 0 0 0 3 3"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h13l-2.5 4.5L18 13H5"/>',
    "paper": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h6"/>',
}


def icon(name, cls="ico"):
    if not name:
        return ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')



def url(slug):
    return "/" if slug == "home" else f"/{slug}/"


def dates_card():
    items = "\n".join(
        f'      <li data-date="{iso}"><span class="dc-date">{label}</span>'
        f'<span class="dc-title">{escape(title)}</span></li>'
        for iso, label, title in DATES
    )
    return f"""<aside class="dates-card" aria-label="Important dates">
  <div class="dc-head"><h2>Important Dates</h2><span class="dc-tag">AoE</span></div>
  <ol class="dc-list">
{items}
  </ol>
  <p class="dc-countdown" hidden></p>
  <p class="dc-note">Dates may change. Deadlines are 11:59 PM AoE.</p>
</aside>"""


def nav(active):
    current = ' class="active" aria-current="page"'
    links = "\n".join(
        f'      <a href="{url(s)}"{current if s == active else ""}>{icon(ico)}{label}</a>'
        for s, label, _t, _d, _p, ico in PAGES if s != "home"
    )
    return f"""<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="/" aria-label="BanglaKnight home">
      <img src="/assets/img/logo.svg" alt="" width="38" height="38">
      <span class="brand-text"><span class="brand-name">Bangla<span>Knight</span></span><span class="brand-sub">BLP-2027 Task 1</span></span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <nav id="nav-links" class="nav-links">
{links}
      <a class="nav-cta" href="https://blp-workshop.github.io/" target="_blank" rel="noopener">BLP 2027 ↗</a>
    </nav>
  </div>
</header>"""


def page_header(slug, title, desc, photo, ico):
    return f"""<section class="page-head" style="--photo: url('/assets/img/{photo}')">
  <div class="wrap">
    <p class="crumbs"><a href="/">BanglaKnight</a> <span aria-hidden="true">/</span> {escape(title)}</p>
    <h1>{icon(ico, "ico ico-h1")}{escape(title)}</h1>
    <p class="page-desc">{escape(desc)}</p>
  </div>
</section>"""


def pager(i):
    inner = [p for p in PAGES if p[0] != "home"]
    slugs = [p[0] for p in inner]
    slug = PAGES[i][0]
    if slug not in slugs:
        return ""
    j = slugs.index(slug)
    prev_html = f'<a class="pg-prev" href="{url(inner[j-1][0])}"><span>Previous</span>{inner[j-1][1]}</a>' if j > 0 else "<span></span>"
    next_html = f'<a class="pg-next" href="{url(inner[j+1][0])}"><span>Next</span>{inner[j+1][1]}</a>' if j < len(inner) - 1 else "<span></span>"
    return f'<nav class="pager wrap" aria-label="Page navigation">{prev_html}{next_html}</nav>'


FOOTER = """<footer class="footer">
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-brand">
        <img src="/assets/img/logo.svg" alt="" width="40" height="40">
        <p><strong>BanglaKnight</strong> is Shared Task 1 of the <a href="https://blp-workshop.github.io/" target="_blank" rel="noopener">Third Workshop on Bangla Language Processing (BLP 2027)</a>, co-located with NAACL 2027 in San Francisco.</p>
      </div>
      <p class="footer-also">Also at BLP 2027: <a href="https://multilingual-qa.github.io/" target="_blank" rel="noopener">Task 2: Multilingual Cultural Question Answering ↗</a></p>
    </div>
    <p class="credits">Photos from Wikimedia Commons:
      <a href="https://commons.wikimedia.org/wiki/File:Golden_Gate_Bridge_as_seen_from_Battery_East.jpg" target="_blank" rel="noopener">Golden Gate Bridge</a> by Frank Schulenburg (CC BY-SA 4.0);
      <a href="https://commons.wikimedia.org/wiki/File:Painted_Ladies_San_Francisco_January_2013_panorama_2.jpg" target="_blank" rel="noopener">Painted Ladies</a> by King of Hearts (CC BY-SA 3.0);
      <a href="https://commons.wikimedia.org/wiki/File:San_Francisco_skyline_from_Coit_Tower.jpg" target="_blank" rel="noopener">San Francisco skyline</a> by Supercarwaar (CC BY-SA 4.0). Resized and tinted.</p>
  </div>
</footer>"""


def render(i):
    slug, label, title, desc, photo, ico = PAGES[i]
    body = (ROOT / "src" / f"{slug}.html").read_text(encoding="utf-8")
    body = body.replace("{{DATES_CARD}}", dates_card())
    full_title = "BanglaKnight · BLP-2027 Task 1: Adversarial Prompt Classification" if slug == "home" else f"{title} · BanglaKnight (BLP-2027 Task 1)"
    head_html = "" if slug == "home" else page_header(slug, title, desc, photo, ico)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(full_title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#E0474F">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+Da+2:wght@500;600;700;800&family=Hind+Siliguri:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="page-{slug}">

{nav(slug)}

<main>
{head_html}
{body}
{pager(i)}
</main>

{FOOTER}

<script src="/assets/js/app.js"></script>
</body>
</html>
"""


def main():
    for i, (slug, *_rest) in enumerate(PAGES):
        out = ROOT / ("index.html" if slug == "home" else f"{slug}/index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(i), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    for path, target in REDIRECTS.items():
        out = ROOT / path / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}">'
            f'<title>Moved</title></head><body><p>This page moved: <a href="{target}">{target}</a></p></body></html>\n',
            encoding="utf-8")
        print("redirect", path, "->", target)


if __name__ == "__main__":
    main()
