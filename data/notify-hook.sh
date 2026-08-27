#!/usr/bin/env bash
# Agenda watch notification hook — creates a Taskwarrior task.
#
# Called by run_watch.sh for every notification:
#   $1  urgency: low | normal | critical
#   $2  subject line
#   stdin: the full summary text
#
# CONTRACT WITH THE CALLER. Exit 0 means "handled — do not raise a popup of
# your own". Any non-zero exit means "no task was created", and run_watch.sh
# falls back to a plain notify-send. That is not only an error path: a `low`
# urgency run (nothing new on any agenda) deliberately creates no task and
# exits non-zero, because a to-do saying "nothing happened" is noise.
#
# WHY NO notify-send HERE. ~/.task/hooks/on-add.notify already raises a
# desktop notification for every task added. Creating the task IS the
# notification; a second popup would double up.
#
# THE DBUS LINE BELOW IS LOAD-BEARING. That on-add hook shells out to
# notify-send and swallows every exception, so under cron — where there is no
# session bus — it would fail completely silently and you would get a task
# with no popup and no error. Export the bus before calling task so the hook
# inherits it.

set -uo pipefail

URGENCY="${1:-normal}"
SUBJECT="${2:-Agenda Watch}"
BODY="$(cat)"

export HOME="${HOME:-/home/scottr}"
command -v task >/dev/null 2>&1 || { echo "notify-hook: task not on PATH"; exit 1; }

if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
  bus="/run/user/$(id -u)/bus"
  [ -S "$bus" ] && export DBUS_SESSION_BUS_ADDRESS="unix:path=$bus"
fi

# Nothing new is not a to-do. Let the caller raise its quiet popup instead.
[ "$URGENCY" = "low" ] && { echo "notify-hook: low urgency, no task created"; exit 2; }

# Taskwarrior parses each argument for attribute syntax, so a stray colon or
# plus in a brief's own wording would be read as a modifier and silently eaten.
# Strip the description down to safe characters; the real text goes in an
# annotation, where it is only ever stored.
sanitize() { printf '%s' "$1" | tr '\n' ' ' | tr -cd '[:alnum:] .,()/&-' | cut -c1-180; }

TODAY="$(date +%Y-%m-%d)"

# The failure task is tagged separately, and that tag is part of the dedupe
# key below. Without it a failed run on a day that already had a good one gets
# folded into the existing "review the page" task as another annotation --
# burying the loud case inside the quiet one, which is precisely backwards.
if [ "$URGENCY" = "critical" ]; then
  DESC="Agenda watch FAILED $TODAY - check the run log"
  KIND=(+agendafail)
  FILTER=(+agendafail)
  EXTRA=(priority:H due:today)
else
  DESC="Review updated council agenda page - $TODAY"
  KIND=()
  FILTER=(-agendafail)
  EXTRA=(due:tomorrow)
fi

# One task per kind per day. A Wednesday and a Friday run each get their own,
# but a re-run on the same day annotates the existing task rather than
# stacking duplicates in the bar.
EXISTING="$(task rc.verbose=nothing rc.hooks=off status:pending +agendawatch \
             "${FILTER[@]}" description.has:"$TODAY" _ids 2>/dev/null | head -1)"

if [ -n "$EXISTING" ]; then
  ID="$EXISTING"
  echo "notify-hook: task $ID already exists for $TODAY, annotating"
  # Annotating fires no on-add hook, so a second run on the same day would be
  # completely silent -- exactly the run that has something new to say. Raise
  # the popup here instead. The app name matches a dunst rule that makes it
  # stick until dismissed; see README.
  if command -v notify-send >/dev/null 2>&1 && [ -n "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
    notify-send -a "Agenda Watch" -u "$URGENCY" \
      "$SUBJECT" "$(printf '%s' "$BODY" | head -3)" 2>/dev/null || true
  fi
else
  task rc.verbose=nothing add project:council +agendawatch "${KIND[@]}" \
    "${EXTRA[@]}" "$(sanitize "$DESC")" >/dev/null 2>&1 \
    || { echo "notify-hook: task add failed"; exit 1; }
  ID="$(task rc.verbose=nothing rc.hooks=off status:pending +agendawatch \
         "${FILTER[@]}" description.has:"$TODAY" _ids 2>/dev/null | head -1)"
  [ -n "$ID" ] || { echo "notify-hook: task added but could not be found again"; exit 1; }
fi

# The bottom line, then where to look. Annotations are the right home for the
# brief's own wording — they are stored verbatim and never re-parsed.
FIRST="$(printf '%s' "$BODY" | grep -v '^[[:space:]]*$' | head -3)"
while IFS= read -r line; do
  [ -n "$line" ] || continue
  task rc.verbose=nothing rc.hooks=off "$ID" annotate -- "$(sanitize "$line")" >/dev/null 2>&1
done <<< "$FIRST"

task rc.verbose=nothing rc.hooks=off "$ID" annotate -- \
  "$(sanitize "$SUBJECT")" >/dev/null 2>&1

echo "notify-hook: taskwarrior task $ID created/updated"
exit 0
