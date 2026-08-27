#!/usr/bin/env bash
# Council agenda watch — local cron runner.
#
# Runs the whole job on this machine: gather, read attachments, write briefs,
# rebuild the GitHub Pages site, commit and push (which publishes it), then
# raise a Taskwarrior task to review the result.
#
# WHY LOCAL. This ran as a Claude Code cloud routine first
# (trig_01RT8WqXFyTLpGRsE8gHBGmp, now disabled). The cloud sandbox sits behind
# an Anthropic-managed egress proxy that allowlists package registries and API
# hosts; clark.wa.gov and vancouverwa.api.civicclerk.com are not on it and
# answered 403 to CONNECT. There is no per-account setting to add them outside
# the Enterprise admin console. See briefs/raw/2026-08-27-digest.md for the
# failed run. Re-enabling the cloud routine is one API call if that ever
# changes.
#
# WHEN. Wednesday and Friday evening — see README.md "Running it". Clark
# County's Tuesday agenda is due 5pm Wednesday; Council Time additions by
# Friday noon.
#
# EXIT CODES. 0 work done or nothing to do; 1 setup problem (missing claude,
# bad repo); 2 the gather failed (usually network); 3 the brief run died
# part-way (session limit, timeout) — work may be uncommitted.

set -uo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT" || exit 1

# Email is OFF by default — no MTA is configured on this machine yet, and the
# intended destination is a local todo app rather than a mailbox. Turn it on
# with EMAIL_ENABLED=1 once ~/.msmtprc exists (see README.md).
EMAIL_ENABLED="${EMAIL_ENABLED:-0}"
EMAIL_TO="${EMAIL_TO:-zefreak@gmail.com}"

# The notification path. data/notify-hook.sh is called for every notification
# with the urgency as $1, the subject as $2 and the full summary on stdin. It
# creates a Taskwarrior task; Taskwarrior's own on-add hook raises the desktop
# popup, so the task IS the notification. Exit 0 means handled; any non-zero
# exit falls back to a plain notify-send, so a broken hook cannot swallow a
# brief. Swap the hook to change where notifications go — no edit here.
NOTIFY_HOOK="$PROJECT/data/notify-hook.sh"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/sf/bin/claude}"
MODEL="${MODEL:-opus}"

STAMP="$(date +%Y-%m-%d-%H%M)"
LOGDIR="$PROJECT/briefs/raw"
LOG="$LOGDIR/run-$STAMP.log"
BOTTOM_LINE="$LOGDIR/.last-bottom-line.txt"
mkdir -p "$LOGDIR"

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }

# --------------------------------------------------------------- notify
# cron has no desktop session, so notify-send needs to be told which bus to
# talk to. Find the user's session bus from a running process rather than
# assuming /run/user/$UID/bus exists.
desktop_notify() {
  local urgency="$1" title="$2" body="$3"
  command -v notify-send >/dev/null 2>&1 || return 0
  if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
    local bus="/run/user/$(id -u)/bus"
    [ -S "$bus" ] && export DBUS_SESSION_BUS_ADDRESS="unix:path=$bus"
  fi
  [ -n "${DBUS_SESSION_BUS_ADDRESS:-}" ] || { log "no dbus session; skipped desktop notification"; return 0; }
  notify-send --urgency="$urgency" --app-name="Agenda Watch" "$title" "$body" \
    2>>"$LOG" || log "notify-send failed"
}

# Email needs an MTA. mail/mailx are installed but have nothing behind them,
# so msmtp is what actually delivers. Disabled by default; when explicitly
# enabled but unusable, say so loudly rather than failing silently — a missed
# brief must never look like a quiet week.
email_notify() {
  local subject="$1" body="$2"
  [ "$EMAIL_ENABLED" = "1" ] || return 0
  if ! command -v msmtp >/dev/null 2>&1 || [ ! -f "$HOME/.msmtprc" ]; then
    log "EMAIL NOT SENT — EMAIL_ENABLED=1 but msmtp missing or ~/.msmtprc absent."
    desktop_notify critical "Agenda Watch — email not configured" \
      "Brief was written but could not be emailed. Set up msmtp (README)."
    return 0
  fi
  printf 'To: %s\nFrom: %s\nSubject: %s\nContent-Type: text/plain; charset=UTF-8\n\n%s\n' \
    "$EMAIL_TO" "$EMAIL_TO" "$subject" "$body" \
    | msmtp --read-recipients 2>>"$LOG" \
    || { log "msmtp failed — see log"; desktop_notify critical \
         "Agenda Watch — email failed" "See $LOG"; }
}

# Returns 0 only when the hook says it handled the notification. A missing or
# non-executable hook counts as not handled, so the popup still happens.
run_hook() {
  local urgency="$1" subject="$2" body="$3"
  [ -x "$NOTIFY_HOOK" ] || return 1
  printf '%s' "$body" | "$NOTIFY_HOOK" "$urgency" "$subject" >>"$LOG" 2>&1
}

# The hook creates a Taskwarrior task, and ~/.task/hooks/on-add.notify raises
# the desktop notification as a side effect of the add. So when the hook
# handles it, do NOT also call notify-send — that would pop twice. The plain
# popup is the fallback for when there is no task to make: a quiet run, or a
# broken/absent hook.
notify_both() {
  local urgency="$1" subject="$2" body="$3"
  email_notify "$subject" "$body"
  if run_hook "$urgency" "$subject" "$body"; then
    log "notification handled by $NOTIFY_HOOK"
  else
    desktop_notify "$urgency" "$subject" "$body"
  fi
}

# --------------------------------------------------------------- preflight
[ -x "$CLAUDE_BIN" ] || { log "FATAL: claude not executable at $CLAUDE_BIN"; \
  notify_both critical "Agenda Watch — setup error" \
  "claude not found at $CLAUDE_BIN"; exit 1; }

log "=== run start, project $PROJECT"

# Pull first so a cloud run or a manual edit elsewhere does not cause a
# conflict at push time.
git pull --ff-only >>"$LOG" 2>&1 || log "warning: git pull --ff-only failed; continuing"

# --------------------------------------------------------------- gather
log "running agenda_watch.py"
GATHER="$(timeout 900 python3 data/agenda_watch.py 2>&1)"
GATHER_RC=$?
printf '%s\n' "$GATHER" >>"$LOG"

if [ $GATHER_RC -ne 0 ]; then
  log "FATAL: gather failed (rc=$GATHER_RC)"
  notify_both critical "Agenda Watch — gather FAILED" \
"The agenda fetch failed and no brief was written. This is usually a network
problem reaching clark.wa.gov or vancouverwa.api.civicclerk.com.

Log: $LOG

$(printf '%s' "$GATHER" | tail -15)"
  exit 2
fi

if printf '%s' "$GATHER" | grep -q "No new or changed agendas"; then
  log "nothing new; sending quiet notification"
  notify_both low "Agenda Watch — nothing new" \
"No new or changed agendas were published since the last run.

This is the routine working, not failing. Next run per crontab.
Log: $LOG"
  exit 0
fi

DIGEST="$LOGDIR/$(date +%Y-%m-%d)-digest.md"
log "digest written: $DIGEST"

# --------------------------------------------------------------- brief
# BRIEF-PROMPT.md is the instruction set; the prompt below only orchestrates.
: > "$BOTTOM_LINE"

read -r -d '' PROMPT <<PROMPT_EOF
Run the council agenda watch brief for this repo. You are in $PROJECT.

READ FIRST, in order: CLAUDE.md, BRIEF-PROMPT.md, README.md. BRIEF-PROMPT.md is
the full instruction set — the lens, what to look for, the output structure and
the accuracy rules. Follow it rather than improvising. README.md carries the
gotchas; several cause silent wrong answers, not errors.

The gather has already run. Its digest is at $DIGEST — read it; do not re-run
the script.

1. For every meeting in the digest, READ THE ATTACHMENTS. Do not brief from
   agenda titles; titles are written to be uncontroversial and the substance is
   in the staff reports, ordinances and presentations. Download with curl and
   read with pdftotext -layout. 'python3 data/agenda_watch.py --fetch <agendaId>'
   pulls Vancouver meeting-level files. If you flag an item without opening its
   attachments, say so explicitly in the brief.

2. Before briefing any housing, zoning, comprehensive plan, impact fee or
   homelessness item, read context/README.md and consult the analysis in
   context/. It already holds the local landscape and the counter-arguments.
   Do not re-derive what is there and do not contradict it without saying so.
   Those files are copies and may be stale — treat a figure there as a lead to
   verify against the agenda's own attachments, not as current fact.

3. Write one markdown brief per meeting to briefs/<meeting-date>-<body>.md per
   BRIEF-PROMPT.md section 5. Every brief ends with 'What I could not check'.

4. Update briefs/agenda-watch.html — the rolling page SOURCE. Read
   briefs/PUBLISHING.md for the rules. Keep the title 'Council Agenda Watch'
   unchanged and honour the existing design system. The page shows UPCOMING
   meetings; drop ones that have passed.

   It is a FRAGMENT: no doctype, html, head or body tags. Do not add them.
   The site build wraps it.

5. Run: python3 data/build_site.py
   That regenerates docs/ from the fragment. GitHub Pages serves docs/ on main,
   so the push in the next step IS the publish — there is no separate step and
   nothing is left pending. If the build errors, fix the fragment and re-run;
   do not commit a stale docs/.

6. Commit and push: git add -A, commit with a message stating the findings not
   just 'update briefs', then push to origin main. If the push is rejected
   because the remote moved, pull --rebase and retry.
   data/.agenda-watch-state.json is committed on purpose so seen-agenda state
   persists between runs; if it conflicts, take the remote version.

7. LAST STEP, REQUIRED: write a plain-text summary to $BOTTOM_LINE — first line
   is a single sentence bottom line, then a blank line, then up to six bullet
   lines for what needs action, each naming the body, the item and any deadline.
   No markdown headers, no links. This file is the body of the notification the
   user actually reads, so if it is empty they get nothing useful.

JUDGEMENT: the reader is on the left and organises with DSA. Rank by how easily
something passes unnoticed — consent items pass without debate unless pulled,
work sessions take no public comment but shape proposals, special meetings need
only 24 hours' notice. Do not manufacture urgency; if nothing is relevant the
brief is three lines saying so. Where an item is genuinely good, say so.
Flag public comment deadlines and sign-up mechanisms wherever comment is open.

If you hit a blocker, still commit what you completed and state in
$BOTTOM_LINE exactly what failed and what is missing.
PROMPT_EOF

log "invoking claude (model=$MODEL)"
# KNOWN BLOCKER, 26 Aug 2026 run. --permission-mode acceptEdits auto-approves file
# edits ONLY. Bash and WebFetch still prompt, and there is nobody at a terminal under
# cron, so every attempt to curl an attachment or run pdftotext was denied. The gather
# succeeded (it runs as a separate process, above) but the brief step could not open a
# single staff report and had to be written from agenda titles. That is the one thing
# BRIEF-PROMPT.md §2 says must not happen.
#
# The fix is a tool allowlist on this invocation, something like:
#
#   --allowedTools 'Bash(curl:*)' 'Bash(pdftotext:*)' 'Bash(pdfinfo:*)' \
#                  'Bash(python3 data/*)' 'WebFetch(domain:clark.wa.gov)' \
#                  'WebFetch(domain:vancouverwa.api.civicclerk.com)' \
#
# left commented because the exact flag spelling was NOT verified against the installed
# claude build during that run, and a wrong flag makes claude exit immediately — which
# would turn a degraded brief into no brief at all, silently. Verify with
# `claude --help | grep -i allowed`, then uncomment, then test with a manual run before
# trusting cron with it.
# --allowedTools is load-bearing and was missing on the first run.
# --permission-mode acceptEdits auto-approves EDITS ONLY; Bash and WebFetch
# still prompt, and under cron nobody is there to approve. The result was a
# silent hollowing-out: every curl, pdftotext and git call was denied, so the
# briefs got written from agenda titles alone and nothing was committed, while
# the script still exited 0. Naming the tools explicitly is preferred over
# --dangerously-skip-permissions: the job's needs are known and bounded.
printf '%s' "$PROMPT" | timeout 3600 "$CLAUDE_BIN" -p \
  --model "$MODEL" \
  --permission-mode acceptEdits \
  --allowedTools "Bash WebFetch Read Write Edit Glob Grep" \
  >>"$LOG" 2>&1
CLAUDE_RC=$?
log "claude exited rc=$CLAUDE_RC"

# --------------------------------------------------------------- notify
if [ -s "$BOTTOM_LINE" ]; then
  SUMMARY="$(cat "$BOTTOM_LINE")"
else
  SUMMARY="The brief run produced no summary file. Something went wrong — check
the log and the repo before assuming there was nothing to report.

Log: $LOG"
fi

# Exit 3, not 0. A brief run that died — usually the account session limit, or
# a timeout — must be distinguishable from success by anything watching exit
# codes, not only by the notification. Work already written to disk is left in
# place and committed on the next run.
if [ $CLAUDE_RC -ne 0 ]; then
  notify_both critical "Agenda Watch — brief run failed (rc=$CLAUDE_RC)" \
"$SUMMARY

Uncommitted work may be sitting in the working tree — check 'git status'.
Log: $LOG"
  exit 3
fi

FIRSTLINE="$(head -1 "$BOTTOM_LINE" 2>/dev/null)"
[ -n "$FIRSTLINE" ] || FIRSTLINE="Agenda watch ran — see log"

notify_both normal "Agenda Watch — $(date +%a\ %d\ %b)" \
"$SUMMARY

ARTIFACT REPUBLISH IS PENDING — cron cannot publish it. From an interactive
Claude Code session in this repo: 'republish the agenda watch artifact'.
Artifact: https://claude.ai/code/artifact/401e7202-daea-4512-8c70-0b8fe2b1cd51
Log: $LOG"

log "=== run complete"
exit 0
