# zengnigel.github.io

Personal website — pure HTML/CSS/JS, no frameworks.

Live at: https://zengnigel.github.io

## Structure

```
.
├── index.html          # English homepage
├── index-zh.html       # Chinese homepage
├── style.css           # Styles (light + dark mode)
├── script.js           # Theme toggle, scroll animation, blog list
├── assets/             # Images (avatar, etc.)
├── _posts/             # Markdown source for blog posts
├── posts/              # Generated HTML posts (from build.py)
│   ├── index.json      # Post list (auto-generated)
│   └── *.html          # Individual post pages
└── tools/
    └── build.py        # Convert _posts/*.md → posts/*.html
```

## Blog workflow

1. Add a new post to `_posts/` with format `YYYY-MM-DD-slug.md`
2. Run `python tools/build.py`
3. Commit and push

## Features

- Light/dark mode toggle (saved to localStorage)
- Scroll reveal animations (IntersectionObserver)
- Bilingual (English / Chinese)
- Dynamic blog list from `posts/index.json`

## Deploy

Push to `main` — GitHub Pages deploys automatically (static files, no build step).
