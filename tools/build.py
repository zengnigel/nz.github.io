#!/usr/bin/env python3
"""
build.py — Convert _posts/*.md to posts/*.html

Usage:
    python tools/build.py

Requires:
    pip install markdown

Output:
    posts/<slug>.html       (English post)
    posts/<slug>-zh.html    (Chinese post, from _posts/*.zh.md)
    posts/index.json        (English blog list)
    posts/index-zh.json     (Chinese blog list)
"""

import re
import json
import markdown
from pathlib import Path


# ── Paths ──────────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).parent.parent
POSTS_MD    = REPO_ROOT / "_posts"
POSTS_HTML  = REPO_ROOT / "posts"
POSTS_INDEX    = POSTS_HTML / "index.json"
POSTS_INDEX_ZH = POSTS_HTML / "index-zh.json"


# ── Frontmatter parser ─────────────────────────────────────────────────────

def parse_frontmatter(text):
    """Extract YAML-style frontmatter (---) and return (meta dict, body str)."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    fm_block = text[3:end].strip()
    body     = text[end + 4:].strip()

    meta = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"').strip("'")

    # Parse tags / categories lists e.g. [ESP32, IR, AC]
    for key in ("tags", "categories"):
        if key in meta:
            raw = meta[key].strip("[]")
            meta[key] = [t.strip() for t in raw.split(",") if t.strip()]

    return meta, body


# ── Slug helper ────────────────────────────────────────────────────────────

def filename_to_slug(filename):
    """2025-07-02-smart-ac-controller-progress.md → smart-ac-controller-progress"""
    name = Path(filename).stem                    # strip .md
    match = re.match(r"^\d{4}-\d{2}-\d{2}-(.*)", name)
    return match.group(1) if match else name


def filename_to_date(filename):
    """2025-07-02-smart-ac-controller-progress.md → 2025-07-02"""
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", Path(filename).name)
    return match.group(1) if match else ""


def zh_filename_to_slug(filename):
    """2026-05-02-goodbye-jekyll.zh.md → goodbye-jekyll"""
    stem = Path(filename).stem
    if not stem.endswith(".zh"):
        return None
    base = stem[:-3]
    match = re.match(r"^\d{4}-\d{2}-\d{2}-(.*)", base)
    return match.group(1) if match else base


# ── HTML template ──────────────────────────────────────────────────────────

def render_html(meta, body_html, zh=False, lang_switch=None):
    """lang_switch: (href_filename, link_label) e.g. ('goodbye-jekyll-zh.html', '中文') or None."""
    title   = meta.get("title", "Post")
    date    = meta.get("date", "")[:10]          # keep YYYY-MM-DD only
    tags    = meta.get("tags", [])
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)

    if zh:
        lang = "zh"
        back_href = "../index-zh.html"
        back_text = "← 返回首頁"
        nav_primary = '<a href="../index-zh.html" class="nav-link active">首頁</a>'
        nav_secondary = '<a href="../index.html" class="nav-link">English</a>'
        aria_theme = "切換深色模式"
        footer_text = "© 2025 Nigel Zeng。純 HTML/CSS/JS 製作。"
    else:
        lang = "en"
        back_href = "../index.html"
        back_text = "← Back to Home"
        nav_primary = '<a href="../index.html" class="nav-link">Home</a>'
        nav_secondary = '<a href="../index-zh.html" class="nav-link">中文</a>'
        aria_theme = "Toggle dark mode"
        footer_text = "© 2025 Nigel Zeng. Built with pure HTML/CSS/JS."

    if lang_switch:
        switch_href, switch_label = lang_switch
        if zh:
            lang_switch_html = (
                f'      <p class="lang-switch" role="note">'
                f'<span class="lang-switch-text">其他語言：</span>'
                f'<a class="lang-switch-link" href="{switch_href}">{switch_label}</a>'
                f"</p>"
            )
        else:
            lang_switch_html = (
                f'      <p class="lang-switch" role="note">'
                f'<span class="lang-switch-text">Also available in </span>'
                f'<a class="lang-switch-link" href="{switch_href}">{switch_label}</a>'
                f"</p>"
            )
    else:
        lang_switch_html = ""

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%232563eb%22 width=%22100%22 height=%22100%22 rx=%2215%22/><text x=%2250%22 y=%2270%22 font-size=%2260%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22sans-serif%22 font-weight=%22bold%22>N</text></svg>">
  <style>
    .post-header {{ padding: 3rem 0 1.5rem; }}
    .post-date   {{ color: var(--text-muted); font-size: .875rem; margin-bottom: .75rem; }}
    .post-title  {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem; }}
    .post-tags   {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 2rem; }}
    .post-body   {{ padding-bottom: 4rem; }}
    .post-body h2 {{ font-size: 1.25rem; font-weight: 600; margin: 2rem 0 .75rem; }}
    .post-body h3 {{ font-size: 1.1rem; font-weight: 600; margin: 1.5rem 0 .5rem; }}
    .post-body p  {{ margin-bottom: 1rem; color: var(--text-secondary); line-height: 1.8; }}
    .post-body ul, .post-body ol {{ margin: 0 0 1rem 1.5rem; color: var(--text-secondary); line-height: 1.8; }}
    .post-body img {{ max-width: 100%; border-radius: 8px; margin: 1rem 0; }}
    .post-body em  {{ font-style: italic; color: var(--text-muted); font-size: .875rem; }}
    .post-body code {{ background: var(--tag-bg); padding: .2rem .4rem; border-radius: 4px; font-size: .875em; }}
    .post-body pre  {{ background: var(--tag-bg); padding: 1rem; border-radius: 8px; overflow-x: auto; margin-bottom: 1rem; }}
    .post-body pre code {{ background: none; padding: 0; }}
    .back-link  {{ display: inline-block; margin: 1.5rem 0; color: var(--text-secondary); font-size: .875rem; }}
    .back-link:hover {{ color: var(--accent); }}
    .lang-switch {{ margin: -0.5rem 0 1.75rem; font-size: .875rem; color: var(--text-muted); }}
    .lang-switch-link {{ color: var(--accent); font-weight: 600; text-decoration: none; }}
    .lang-switch-link:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="nav">
        {nav_primary}
        {nav_secondary}
        <button id="theme-toggle" class="theme-toggle" aria-label="{aria_theme}">
          <svg class="icon-sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"></circle>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
          </svg>
          <svg class="icon-moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </nav>
    </div>
  </header>

  <main class="main">
    <div class="container">
      <a href="{back_href}" class="back-link">{back_text}</a>

      <div class="post-header">
        <p class="post-date">{date}</p>
        <h1 class="post-title">{title}</h1>
        <div class="post-tags">{tags_html}</div>
        {lang_switch_html}
      </div>

      <article class="post-body">
        {body_html}
      </article>
    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <p>{footer_text}</p>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>"""


# ── Main ───────────────────────────────────────────────────────────────────

def build():
    POSTS_HTML.mkdir(exist_ok=True)

    md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list"])

    posts = []
    posts_zh = []

    for md_file in sorted(POSTS_MD.glob("*.md")):
        if md_file.name == ".placeholder":
            continue
        if md_file.name.endswith(".zh.md"):
            continue

        text             = md_file.read_text(encoding="utf-8")
        meta, body       = parse_frontmatter(text)
        md.reset()
        body_html        = md.convert(body)

        slug             = filename_to_slug(md_file.name)
        date             = meta.get("date", filename_to_date(md_file.name))[:10]
        title            = meta.get("title", slug)

        zh_sibling = md_file.with_name(f"{md_file.stem}.zh.md")
        lang_switch = (f"{slug}-zh.html", "中文") if zh_sibling.is_file() else None

        html             = render_html(meta, body_html, zh=False, lang_switch=lang_switch)
        out_path         = POSTS_HTML / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK  {md_file.name}  ->  posts/{slug}.html")

        posts.append({
            "slug":  slug,
            "title": title,
            "date":  date,
            "tags":  meta.get("tags", []),
            "url":   f"posts/{slug}.html",
        })

    for md_file in sorted(POSTS_MD.glob("*.zh.md")):
        text             = md_file.read_text(encoding="utf-8")
        meta, body       = parse_frontmatter(text)
        md.reset()
        body_html        = md.convert(body)

        slug             = zh_filename_to_slug(md_file.name)
        if not slug:
            print(f"  SKIP  {md_file.name}  (could not parse slug)")
            continue

        date             = meta.get("date", filename_to_date(md_file.name))[:10]
        title            = meta.get("title", slug)

        stem_full = Path(md_file).stem
        base_stem = stem_full[:-3] if stem_full.endswith(".zh") else stem_full
        en_sibling = md_file.parent / f"{base_stem}.md"
        lang_switch = (f"{slug}.html", "English") if en_sibling.is_file() else None

        html             = render_html(meta, body_html, zh=True, lang_switch=lang_switch)
        out_path         = POSTS_HTML / f"{slug}-zh.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK  {md_file.name}  ->  posts/{slug}-zh.html")

        posts_zh.append({
            "slug":  slug,
            "title": title,
            "date":  date,
            "tags":  meta.get("tags", []),
            "url":   f"posts/{slug}-zh.html",
        })

    # Write index.json (sorted newest first)
    posts.sort(key=lambda p: p["date"], reverse=True)
    POSTS_INDEX.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  posts/index.json  ({len(posts)} post(s))")

    posts_zh.sort(key=lambda p: p["date"], reverse=True)
    POSTS_INDEX_ZH.write_text(json.dumps(posts_zh, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  posts/index-zh.json  ({len(posts_zh)} post(s))")


if __name__ == "__main__":
    build()
