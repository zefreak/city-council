#!/usr/bin/env python3
"""Build the GitHub Pages site from the rolling agenda-watch page.

    python3 data/build_site.py

No arguments, no network, stdlib only. Reads briefs/agenda-watch.html and
writes docs/index.html plus docs/archive.html. GitHub Pages serves /docs on
main, so `git push` is the publish step -- which is the whole point: the
headless `claude -p` run has no Artifact tool, but it can commit and push.

WHY agenda-watch.html STAYS A FRAGMENT. It has no <!doctype>, <html>, <head>
or <body> -- it starts at <title>. That is the shape the Artifact tool wants
(it supplies the skeleton itself), and it is the file the brief-writing agent
edits. Keeping the boilerplate out of the file being edited means the agent
cannot break the page skeleton, and it leaves the claude.ai artifact usable as
a fallback if Pages ever goes away. This script adds the skeleton back.

WHAT IT ADDS. The doctype and head, a three-state theme toggle, and an archive
page listing the markdown briefs. Nothing else -- the design, palette and
content are entirely the fragment's.
"""

import html
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAGMENT = os.path.join(ROOT, "briefs", "agenda-watch.html")
BRIEFS = os.path.join(ROOT, "briefs")
DOCS = os.path.join(ROOT, "docs")
REPO = "https://github.com/zefreak/city-council"

# The fragment's own tokens already define all three theme states: bare :root
# is light, :root:not([data-theme="light"]) under prefers-color-scheme:dark is
# the system default, and :root[data-theme="dark"] is the explicit choice. So
# the toggle only has to set or clear one attribute -- no colours live here.
TOGGLE_CSS = """
  .theme-toggle{
    position:fixed; top:14px; right:14px; z-index:50;
    display:flex; align-items:center; gap:.45em;
    padding:.42em .8em;
    font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
    font-size:12px; letter-spacing:.04em;
    color:var(--ink-soft); background:var(--raised);
    border:1px solid var(--rule); border-radius:999px;
    box-shadow:var(--shadow); cursor:pointer;
    transition:color .15s ease, border-color .15s ease;
  }
  .theme-toggle:hover{ color:var(--accent); border-color:var(--accent); }
  .theme-toggle:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
  .theme-toggle .glyph{ font-size:14px; line-height:1; }
  @media (prefers-reduced-motion:reduce){ .theme-toggle{transition:none} }
  @media print{ .theme-toggle{display:none} }
  /* Narrow screens: the masthead needs the width more than the label does. */
  @media (max-width:560px){ .theme-toggle .label{display:none} }
"""

# Runs in <head>, before the body paints. Inline and synchronous on purpose:
# reading localStorage after first paint gives a flash of the wrong theme.
THEME_BOOT = """
  (function(){
    try{
      var t = localStorage.getItem("agenda-watch-theme");
      if (t === "light" || t === "dark") {
        document.documentElement.setAttribute("data-theme", t);
      }
    }catch(e){}
  })();
"""

# Three states, not two, because "follow the OS" is a real preference and the
# CSS already distinguishes it: no attribute at all means system.
THEME_TOGGLE_JS = """
  (function(){
    var KEY = "agenda-watch-theme";
    var ORDER = ["system","light","dark"];
    var FACE = {
      system:{glyph:"\\u25D0", label:"System"},
      light: {glyph:"\\u2600", label:"Light"},
      dark:  {glyph:"\\u263E", label:"Dark"}
    };
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var glyph = btn.querySelector(".glyph");
    var label = btn.querySelector(".label");

    function read(){
      var t = document.documentElement.getAttribute("data-theme");
      return (t === "light" || t === "dark") ? t : "system";
    }
    function paint(state){
      glyph.textContent = FACE[state].glyph;
      label.textContent = FACE[state].label;
      btn.setAttribute("aria-label", "Theme: " + FACE[state].label + ". Click to change.");
      btn.setAttribute("title", "Theme: " + FACE[state].label);
    }
    function apply(state){
      if (state === "system") {
        document.documentElement.removeAttribute("data-theme");
      } else {
        document.documentElement.setAttribute("data-theme", state);
      }
      try{
        if (state === "system") { localStorage.removeItem(KEY); }
        else { localStorage.setItem(KEY, state); }
      }catch(e){}
      paint(state);
    }

    paint(read());
    btn.addEventListener("click", function(){
      apply(ORDER[(ORDER.indexOf(read()) + 1) % ORDER.length]);
    });
  })();
"""

TOGGLE_HTML = (
    '<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Change theme">'
    '<span class="glyph" aria-hidden="true">◐</span>'
    '<span class="label">System</span>'
    "</button>"
)


def split_fragment(src):
    """Return (title, head_links, rest) from the artifact fragment."""
    title = "Council Agenda Watch"
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if m:
        title = m.group(1).strip()
        src = src[: m.start()] + src[m.end():]

    # Font <link> and the <style> block belong in <head>; everything after the
    # closing </style> is body content.
    links = re.findall(r"<link\b[^>]*>", src)
    for tag in links:
        src = src.replace(tag, "", 1)

    m = re.search(r"<style\b.*?</style>", src, re.S)
    if not m:
        raise SystemExit("build_site: no <style> block found in the fragment")
    style = m.group(0)
    body = (src[: m.start()] + src[m.end():]).strip()
    return title, links, style, body


def page(title, links, style, body, extra_css, description):
    """Wrap content in the full document the artifact host used to supply."""
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<meta name="description" content="{html.escape(description, quote=True)}">\n'
        # Keeps the browser chrome from painting light UI over a dark page.
        '<meta name="color-scheme" content="light dark">\n'
        f"<title>{html.escape(title)}</title>\n"
        + "\n".join(links)
        + "\n"
        + style.replace("</style>", extra_css + "\n</style>")
        + "\n<script>"
        + THEME_BOOT
        + "</script>\n</head>\n<body>\n"
        + TOGGLE_HTML
        + "\n"
        + body
        + "\n<script>"
        + THEME_TOGGLE_JS
        + "</script>\n</body>\n</html>\n"
    )


def brief_rows():
    """Every dated markdown brief, newest first."""
    rows = []
    for name in sorted(os.listdir(BRIEFS), reverse=True):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.md$", name)
        if not m:
            continue
        date, slug = m.groups()
        rows.append((date, slug.replace("-", " "), name))
    return rows


def archive_page(style, links):
    """A plain index of the markdown briefs, linking to GitHub's renderer.

    Rendering markdown here would mean writing a markdown parser or taking a
    dependency, and both are the wrong trade for a link list. GitHub already
    renders these files well.
    """
    rows = brief_rows()
    items = []
    for date, label, name in rows:
        pretty = datetime.strptime(date, "%Y-%m-%d").strftime("%a %-d %b %Y")
        items.append(
            f'      <li><a href="{REPO}/blob/main/briefs/{name}">'
            f"<span class=\"arch-date\">{pretty}</span>"
            f'<span class="arch-label">{html.escape(label)}</span></a></li>'
        )
    body = (
        '<div class="wrap">\n'
        '  <header class="masthead">\n'
        '    <div class="kicker">Archive</div>\n'
        "    <h1>Every brief</h1>\n"
        '    <p class="lede">One file per meeting, oldest kept as written. '
        "The front page carries only what is still upcoming.</p>\n"
        "  </header>\n"
        '  <section class="part">\n'
        '    <ul class="arch">\n' + "\n".join(items) + "\n    </ul>\n"
        f'    <p class="foot"><a href="index.html">&larr; Back to the watch</a> · '
        f'<a href="{REPO}">Repository</a></p>\n'
        "  </section>\n"
        "</div>"
    )
    extra = TOGGLE_CSS + """
  .arch{list-style:none;margin:0;padding:0;}
  .arch li{border-bottom:1px solid var(--rule);}
  .arch a{display:flex;gap:1.2em;align-items:baseline;padding:.7em 0;
    text-decoration:none;color:var(--ink);}
  .arch a:hover .arch-label{color:var(--accent);}
  .arch-date{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13px;
    color:var(--ink-faint);white-space:nowrap;font-variant-numeric:tabular-nums;}
  .arch-label{font-weight:600;}
  .foot{margin-top:2em;font-size:15px;color:var(--ink-soft);}
"""
    return page("Brief Archive · Council Agenda Watch", links, style, body,
                extra, "Every council agenda brief, one file per meeting.")


def main():
    with open(FRAGMENT, encoding="utf-8") as fh:
        src = fh.read()
    title, links, style, body = split_fragment(src)

    os.makedirs(DOCS, exist_ok=True)

    # Link the archive from the front page, just above whatever the fragment
    # ends with. Injected here rather than in the fragment so the artifact copy
    # never carries a link to a page that only exists on Pages.
    nav = ('<div class="wrap"><p class="foot" style="font-size:15px;color:var(--ink-soft);'
           'border-top:1px solid var(--rule);padding-top:1.2em;margin-top:0;">'
           f'<a href="archive.html">All briefs &rarr;</a> · '
           f'<a href="{REPO}">Repository</a> · '
           f'Built {datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")}'
           "</p></div>")

    index = page(title, links, style, body + "\n" + nav, TOGGLE_CSS,
                 "What is on the next Vancouver WA and Clark County WA council "
                 "agendas, what is at stake, and where public comment is open.")
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)

    with open(os.path.join(DOCS, "archive.html"), "w", encoding="utf-8") as fh:
        fh.write(archive_page(style, links))

    # Without this GitHub Pages runs the output through Jekyll, which ignores
    # files and directories beginning with an underscore and can rewrite what
    # it thinks is Liquid syntax.
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    print(f"docs/index.html    {os.path.getsize(os.path.join(DOCS,'index.html')):>7,} bytes")
    print(f"docs/archive.html  {os.path.getsize(os.path.join(DOCS,'archive.html')):>7,} bytes"
          f"  ({len(brief_rows())} briefs)")


if __name__ == "__main__":
    main()
