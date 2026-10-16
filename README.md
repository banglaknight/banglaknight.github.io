# BanglaKnight: BLP-2027 Shared Task 1

Website for **BanglaKnight**, Shared Task 1 (Adversarial Prompt Classification) at the
[Third Workshop on Bangla Language Processing (BLP 2027)](https://blp-workshop.github.io/), co-located with NAACL 2027.

Live site: https://banglaknight.github.io/

## How to edit

Each page's content is in `src/`. The shared menu, page header, footer and dates are added by `build.py`.

1. Edit the page in `src/` (for example `src/data.html`), or the dates in `DATES` at the top of `build.py` (shown in the home-page card and the rolling updates bar). Extra items for the updates bar are in `NEWS`; dates that have passed drop out of the bar on their own.
2. Run `python3 build.py`. It rewrites `index.html` and the `*/index.html` pages, plus redirects from the old `/task/` and `/dates/` addresses.
3. Commit and push. GitHub Pages updates in a minute or two.

Don't edit the generated `index.html` files by hand; the next build overwrites them.

| Page | Source | URL |
|---|---|---|
| Home (includes the task) | `src/home.html` | `/` |
| Data | `src/data.html` | `/data/` |
| Leaderboard | `src/leaderboard.html` | `/leaderboard/` |
| Participate | `src/participate.html` | `/participate/` |
| Paper Submission | `src/paper.html` | `/paper/` |
| Organizers | `src/organizers.html` | `/organizers/` |

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Links start with `/`, so open the site through the server, not as a file.
