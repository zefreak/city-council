# Publishing

**The page is published by pushing to `main`.** GitHub Pages serves the `docs/` directory, so
there is no separate publish step and nothing is ever left pending — which is the reason for the
move. The headless `claude -p` run has no `Artifact` tool, but it can `git push`.

**Live:** https://zefreak.github.io/city-council/
**Archive:** https://zefreak.github.io/city-council/archive.html

## The three files

| File | What it is | Edited by |
|---|---|---|
| `briefs/agenda-watch.html` | the page's **source fragment** — content and design | the brief-writing run |
| `data/build_site.py` | wraps the fragment in a document, adds the theme toggle, builds the archive | rarely |
| `docs/` | **generated. Never edit by hand** — the next build overwrites it | nothing |

After editing the fragment:

```bash
python3 data/build_site.py
git add -A && git commit -m "..." && git push
```

## The fragment is a fragment

`briefs/agenda-watch.html` starts at `<title>`. It has **no `<!doctype>`, `<html>`, `<head>` or
`<body>`** and must not gain any — `build_site.py` adds them, and the claude.ai `Artifact` tool
supplies its own, so the same file works either way. Keeping the skeleton out of the file the
agent edits also means a bad edit cannot break the document structure.

## What goes on it

Upcoming meetings only. When a meeting has passed, drop it — the markdown briefs in `briefs/` are
the history, and `docs/archive.html` indexes them automatically from the filenames, so a brief
named `YYYY-MM-DD-<body>.md` needs no other registration.

## Theme

Three states: system (no attribute), light, dark. The toggle cycles them and persists the choice
in `localStorage` under `agenda-watch-theme`; "system" clears the key rather than storing a value,
so a viewer who never touches it follows their OS forever. The colour tokens all live in the
fragment; `build_site.py` contains no colours, only the toggle's layout.

The boot script that reads `localStorage` is inline in `<head>` **on purpose**. Deferring it to
the end of the body would paint the wrong theme first and flash.

## The old claude.ai artifact

`https://claude.ai/code/artifact/401e7202-daea-4512-8c70-0b8fe2b1cd51` was the previous home. It is
no longer updated by the run. Give it one final republish pointing at the Pages URL, or leave it —
but do not resume publishing to both, because two copies drifting apart is worse than one.
