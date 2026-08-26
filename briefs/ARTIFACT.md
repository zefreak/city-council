# Rolling artifact

The shareable copy of the agenda watch. **One page, one URL, republished each run** — never a new
page per meeting.

**URL:** https://claude.ai/code/artifact/401e7202-daea-4512-8c70-0b8fe2b1cd51

**Source:** `briefs/agenda-watch.html`

## Republishing

Edit `briefs/agenda-watch.html`, then call the `Artifact` tool with:

- `file_path` — `briefs/agenda-watch.html` (the same path every time; a different path claims a
  new URL)
- `url` — the URL above, so the republish updates this page instead of creating a second one
- `favicon` — 🏛️, unchanged. Viewers find the tab by its icon; a changed favicon reads as a
  different page.

Keep the `<title>` (`Council Agenda Watch`) stable too.

## What goes on it

Upcoming meetings only. When a meeting has passed, drop it from the page — the markdown briefs in
`briefs/` are where the history lives. The "Recently passed" section is for the most recent
meeting where the outcome still matters; prune it once it stops being useful.

If artifact publishing is unavailable in the run environment, commit the markdown anyway and say
in the run output that the artifact step was skipped. Never silently drop half the deliverable.
