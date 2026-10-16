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

# (ISO date used for the countdown, label shown, milestone, phase)
DATES = [
    ("2026-10-20", "Oct 20, 2026", "Training and development data release", "dev"),
    ("2026-10-20", "Oct 20, 2026", "CodaBench registration opens", "dev"),
    ("2027-01-15", "Jan 15, 2027", "Test data release / evaluation begins", "eval"),
    ("2027-01-24", "Jan 24, 2027", "Registration deadline", "eval"),
    ("2027-01-31", "Jan 31, 2027", "System submission deadline", "eval"),
    ("2027-02-03", "Feb 3, 2027", "Official results released", "after"),
    ("2027-02-15", "Feb 15, 2027", "Shared-task paper submission deadline", "after"),
    ("2027-03-26", "Mar 26, 2027", "Notification of acceptance", "after"),
    ("2027-04-16", "Apr 16, 2027", "Camera-ready paper due", "after"),
    ("2027-06-01", "Jun 1–5, 2027", "Workshop at NAACL 2027, San Francisco", "after"),
]

# Group headings in the dates card
PHASE_NAMES = {
    "dev": ("Development phase", "Oct 20 – Jan 15"),
    "eval": ("Evaluation phase", "Jan 15 – Jan 31"),
    "after": ("Results and papers", ""),
}

# Extra items for the rolling updates bar, after the dates: (bold label, HTML text)
NEWS = [
    ("BLP 2027", 'Co-located with NAACL 2027 · June 1–5, 2027 · San Francisco, California'),
    ("New", 'The <a href="/participate/">Participate</a> page explains both CodaBench phases'),
    ("New", 'System papers: up to 4 pages. See <a href="/paper/">Paper Submission</a>'),
]

# The two competition phases, shown on Home, Participate and Leaderboard ({{PHASES}})
PHASES_BLOCK = """<div class="phases">
  <article class="phase phase-dev">
    <p class="phase-tag">Phase 1</p>
    <h3>{{i:sword}}Development phase</h3>
    <p class="phase-when">Oct 20, 2026 – Jan 15, 2027</p>
    <dl>
      <dt>{{i:data}}Data</dt><dd>Training and dev sets, plus the starter kit</dd>
      <dt>{{i:user}}You</dt><dd>Build and tune your system</dd>
      <dt>{{i:upload}}CodaBench</dt><dd>Submit predictions on the dev set to see your score and check your file format. Practice only: it does not count toward the final ranking.</dd>
    </dl>
  </article>
  <article class="phase phase-eval">
    <p class="phase-tag">Phase 2 · Final</p>
    <h3>{{i:shield}}Evaluation phase</h3>
    <p class="phase-when">Jan 15 – Jan 31, 2027</p>
    <dl>
      <dt>{{i:data}}Data</dt><dd>A new test set, released Jan 15, without labels</dd>
      <dt>{{i:user}}You</dt><dd>Run your final system on it</dd>
      <dt>{{i:upload}}CodaBench</dt><dd>Submit your test predictions by Jan 31. These decide the official ranking, published Feb 3.</dd>
    </dl>
  </article>
</div>"""


# slug, menu label, page title, one-line description, header photo, icon
PAGES = [
    ("home", "Home", "BanglaKnight", "Shared Task 1 at BLP 2027: classify Bangla prompts into four risk levels.", "sf-golden-gate.jpg", None),
    ("data", "Data", "Data", "What you get, the three written forms, and the starter kit.", "sf-skyline.jpg", "data"),
    ("leaderboard", "Leaderboard", "Leaderboard", "Metrics, development-phase scores, and official results.", "sf-painted-ladies.jpg", "trophy"),
    ("participate", "Participate", "Participate", "Two phases on CodaBench: practice on the dev set, then submit on the test set.", "sf-golden-gate.jpg", "swords"),
    ("paper", "Paper Submission", "Paper Submission", "How to write and submit your system description paper.", "sf-painted-ladies.jpg", "paper"),
    ("organizers", "Organizers", "Organizers", "Who runs the task and how to reach us.", "sf-skyline.jpg", "people"),
]

# Old addresses that now point elsewhere: path -> target
REDIRECTS = {"task": "/#task", "dates": "/"}

# Line icons (24x24, drawn with the current text color). In page sources, {{i:name}} becomes the icon.
ICONS = {
    "data": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "trophy": '<path d="M8 21h8"/><path d="M12 16v5"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3"/><path d="M7 5H4v2a3 3 0 0 0 3 3"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h13l-2.5 4.5L18 13H5"/>',
    "paper": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.6-3.4 3-5.4 6-5.4s5.4 2 6 5.4"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.7c2.4.2 4 1.9 4.5 4.8"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    "upload": '<path d="M12 15V4"/><path d="M7.5 8.5 12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "download": '<path d="M12 4v11"/><path d="M7.5 10.5 12 15l4.5-4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "inbox": '<path d="M3 13h5l1.5 2.5h5L16 13h5"/><path d="M5.5 5h13L21 13v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"/>',
    "tag": '<path d="M3 12V4h8l9.5 9.5-8 8z"/><circle cx="7.5" cy="8.5" r="1.4"/>',
    "book": '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5z"/><path d="M4 19.5A1.5 1.5 0 0 0 5.5 21H20v-3"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/>',
    "shield-check": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    "shield-alert": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="M12 8.5v4M12 15.6v.1"/>',
    "shield-x": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m9.6 9.6 4.8 4.8M14.4 9.6l-4.8 4.8"/>',
    "sword": '<path d="M14.5 17.5 3 6V3h3l11.5 11.5"/><path d="m13 19 6-6"/><path d="m16 16 4 4"/><path d="m19 21 2-2"/>',
    "swords": '<path d="M14.5 17.5 3 6V3h3l11.5 11.5"/><path d="m13 19 6-6"/><path d="m16 16 4 4"/><path d="m19 21 2-2"/><path d="M14.5 6.5 18 3h3v3l-3.5 3.5"/><path d="m5 14 4 4"/><path d="m7 17-3 3"/><path d="m3 19 2 2"/>',
    "castle": '<path d="M3 21h18"/><path d="M5 21V5h3v3h3V5h2v3h3V5h3v16"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/>',
    "helmet": '<path d="M5 20v-8a7 7 0 0 1 14 0v8z"/><path d="M7.5 12.5h9"/><path d="M12 5v15"/>',
    "message": '<path d="M4 5h16v11H9l-5 4z"/><path d="M9 9l4 4M13 9l-4 4"/>',
    "alert": '<path d="M12 3.5 2.5 20h19z"/><path d="M12 10v4.5M12 17.3v.1"/>',
    "octagon": '<path d="M8.2 3h7.6L21 8.2v7.6L15.8 21H8.2L3 15.8V8.2z"/><path d="M12 8v4.5M12 15.8v.1"/>',
    "gauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 4-5"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "tool": '<path d="M15 4a5 5 0 0 0-4.8 6.4L4 16.6V20h3.4l6.2-6.2A5 5 0 0 0 20 9l-3 1-2-2 1-3z"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.7 5.4 3.7 8.5s-1.2 5.9-3.7 8.5c-2.5-2.6-3.7-5.4-3.7-8.5s1.2-5.9 3.7-8.5z"/>',
    "package": '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    "code": '<path d="m8.5 7-5 5 5 5M15.5 7l5 5-5 5"/>',
    "file-code": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/>',
    "file-check": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14.5 2 2 4-4"/>',
    "table": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M3.5 14.5h17M9.5 9.5v10"/>',
    "user": '<circle cx="12" cy="8" r="3.8"/><path d="M4.5 20.5c.8-4 3.8-6.2 7.5-6.2s6.7 2.2 7.5 6.2"/>',
    "user-plus": '<circle cx="10" cy="8" r="3.5"/><path d="M3.5 20c.7-3.6 3.3-5.6 6.5-5.6s5.8 2 6.5 5.6"/><path d="M19 8v6M16 11h6"/>',
    "play": '<circle cx="12" cy="12" r="8.5"/><path d="m10 8.5 5.5 3.5-5.5 3.5z"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2.5v3.5M15 2.5v3.5M9 18v3.5M15 18v3.5M2.5 9h3.5M2.5 15h3.5M18 9h3.5M18 15h3.5"/>',
    "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.2 2.4 2.4 4.6-4.8"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "present": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "eye-off": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/><path d="M4 4l16 16"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 7h14"/><path d="m5 7-2.5 6a2.8 2.8 0 0 0 5 0zM19 7l-2.5 6a2.8 2.8 0 0 0 5 0z"/>',
    "type": '<path d="M4 7V5h16v2M12 5v14M9 19h6"/>',
    "question": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.5v.7M12 16.8v.1"/>',
    "shuffle": '<path d="M3 7h3.5c4.5 0 6.5 10 11 10H21M3 17h3.5c1.6 0 2.8-1.2 3.8-2.8M13.7 9.8c1-1.6 2.2-2.8 3.8-2.8H21"/><path d="m18 4 3 3-3 3M18 14l3 3-3 3"/>',
    "route": '<circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="5" r="2.2"/><path d="M8.2 19H16a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h7.8"/>',
    "chart": '<path d="M4 4v16h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
}

ICON_RE = __import__("re").compile(r"\{\{i:([a-z-]+)\}\}")


def icons_in(html):
    """Replace {{i:name}} placeholders with inline icons."""
    return ICON_RE.sub(lambda m: icon(m.group(1)), html)


def icon(name, cls="ico"):
    if not name:
        return ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')



def url(slug):
    return "/" if slug == "home" else f"/{slug}/"


def dates_card():
    groups = []
    for phase in dict.fromkeys(p for *_, p in DATES):
        name, span = PHASE_NAMES[phase]
        items = "\n".join(
            f'        <li data-date="{iso}"><span class="dc-date">{label}</span>'
            f'<span class="dc-title">{escape(title)}</span></li>'
            for iso, label, title, p in DATES if p == phase
        )
        span_html = f'<span class="dc-span">{span}</span>' if span else ""
        groups.append(f"""    <section class="dc-group dc-group-{phase}">
      <h3 class="dc-phase-head"><span class="dc-pill">{name}</span>{span_html}</h3>
      <ol class="dc-list">
{items}
      </ol>
    </section>""")
    body = "\n".join(groups)
    return f"""<aside class="dates-card" aria-label="Important dates">
  <div class="dc-head"><h2>{icon("calendar")}Important Dates</h2><span class="dc-tag">AoE</span></div>
{body}
  <p class="dc-countdown" hidden></p>
  <p class="dc-note">Dates may change. Deadlines are 11:59 PM AoE.</p>
</aside>"""


def ticker():
    """Rolling updates bar: the dates still ahead, then NEWS. app.js loops it."""
    seen, items = set(), []
    for iso, label, title, _p in DATES:
        if label in seen:   # two milestones on one day share one item
            items[-1] = items[-1].replace("</span>", f"; {escape(title[0].lower() + title[1:] if not title.startswith('CodaBench') else title)}</span>")
            continue
        seen.add(label)
        items.append(f'<span class="tk" data-date="{iso}"><b>{label}</b>{escape(title)}</span>')
    items += [f'<span class="tk"><b>{k}</b>{v}</span>' for k, v in NEWS]
    body = "\n          ".join(items)
    return f"""<div class="ticker" role="region" aria-label="Updates and important dates">
  <div class="wrap ticker-in">
    <span class="ticker-label"><span class="dot" aria-hidden="true"></span>Updates</span>
    <div class="ticker-view">
      <div class="ticker-track">
        <div class="tk-set">
          {body}
        </div>
      </div>
    </div>
  </div>
</div>"""


def nav(active):
    current = ' class="active" aria-current="page"'
    links = "\n".join(
        f'      <a href="{url(s)}"{current if s == active else ""}>{icon(ico)}{label}</a>'
        for s, label, _t, _d, _p, ico in PAGES if s != "home"
    )
    return f"""<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="/" aria-label="BanglaKnight home">
      <img src="/assets/img/logo.svg?v=3" alt="" width="38" height="38">
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
        <img src="/assets/img/logo.svg?v=3" alt="" width="40" height="40">
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
    body = body.replace("{{DATES_CARD}}", dates_card()).replace("{{TICKER}}", ticker()).replace("{{PHASES}}", PHASES_BLOCK)
    full_title = "BanglaKnight · BLP-2027 Task 1: Adversarial Prompt Classification" if slug == "home" else f"{title} · BanglaKnight (BLP-2027 Task 1)"
    head_html = "" if slug == "home" else page_header(slug, title, desc, photo, ico) + "\n" + ticker()
    return icons_in(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(full_title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg?v=3">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+Da+2:wght@500;600;700;800&family=Hind+Siliguri:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css?v=9">
</head>
<body class="page-{slug}">

{nav(slug)}

<main>
{head_html}
{body}
{pager(i)}
</main>

{FOOTER}

<script src="/assets/js/app.js?v=2"></script>
</body>
</html>
""")


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
