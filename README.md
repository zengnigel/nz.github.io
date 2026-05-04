# zengnigel.github.io

Personal website — pure HTML/CSS/JS, no frameworks.

Live at: https://zengnigel.github.io

**What this README is for:** it is the on-repo note for *you* (or anyone with a clone) on how the site is structured, how blog posts are produced, and what to commit. GitHub’s web UI does not run the Python builder for you unless you add CI yourself—today this repo expects you to run `build.py` locally and push the generated files.

---

## Structure

```
.
├── index.html          # English homepage
├── index-zh.html       # Chinese homepage
├── style.css           # Styles (light + dark mode)
├── script.js           # Theme toggle, scroll animation, blog lists (EN / 中文)
├── assets/             # Images (avatar, post figures, etc.)
├── _posts/             # Markdown **sources** (you edit these)
├── posts/              # **Generated** HTML + JSON (do not hand-edit)
│   ├── index.json      # English blog list (for script.js)
│   ├── index-zh.json   # Chinese blog list
│   └── *.html          # Per-post pages (`slug.html` and `slug-zh.html`)
└── tools/
    └── build.py        # Converts `_posts/*.md` → `posts/*.html` + both indexes
```

---

## Blog workflow

### English-only post

1. Add `_posts/YYYY-MM-DD-your-slug.md` with YAML front matter (`title`, `date`, `tags`, …).
2. Run **`python tools/build.py`** from the repo root (needs `pip install markdown`).
3. Commit **`_posts/`** plus everything **`build.py` changed under `posts/`** (new/changed `.html` and `index.json` / `index-zh.json`).
4. Push to **`main`**.

### English + Chinese (paired posts)

1. Add the English file: `_posts/YYYY-MM-DD-slug.md`.
2. Add the Chinese file with the **same date and slug**: `_posts/YYYY-MM-DD-slug.zh.md` (note the **`.zh.md`** suffix).
3. Run **`python tools/build.py`**.
4. Commit `_posts/` and all generated files under `posts/`.

**Outputs:**

| Source | Generated page | Listed on |
|--------|----------------|-----------|
| `…-slug.md` | `posts/slug.html` | English home (`index.html`) via `posts/index.json` |
| `…-slug.zh.md` | `posts/slug-zh.html` | Chinese home (`index-zh.html`) via `posts/index-zh.json` |

The homepage **`script.js`** loads `posts/index.json` on the English site and `posts/index-zh.json` when the URL is `index-zh.html` or a Chinese post (`*-zh.html`).

**Language switcher on each article:** if both `slug.md` and `slug.zh.md` exist, `build.py` injects a line under the tags: on English posts, “Also available in **中文**”; on Chinese posts, “其他語言：**English**”. If you only have one language, no switcher appears.

---

## Deploy (GitHub Pages)

This site is **static files only**. **GitHub Pages does not execute `build.py` on push** in the current setup—you generate HTML locally (or in your own CI), then push.

After you push **`main`**, Pages serves whatever is in the repo (root of the site). So:

- If you change **only** `_posts/*.md` but forget to run **`build.py`** and commit **`posts/`**, visitors will **not** see the update.
- After running **`build.py`**, always **`git add posts/`** (and `_posts/` if new) so the live site matches your sources.

---

## Features

- Light/dark mode toggle (saved to `localStorage`)
- Scroll reveal animations (`IntersectionObserver`)
- Bilingual home pages + bilingual blog lists + per-post language switcher when a translation exists
- Dynamic blog lists from `posts/index.json` / `posts/index-zh.json`
