#!/bin/sh
# Polls source files for content changes and rewrites them in-place
# to trigger inotify events inside the container.
# Needed because snap Docker bind mounts don't propagate host inotify events.

WATCH_DIR="${1:-.}"
INTERVAL="${2:-2}"
HASH_DIR="/tmp/dev-watch-hashes"
mkdir -p "$HASH_DIR"

echo "[dev-watch] Watching $WATCH_DIR every ${INTERVAL}s"

while true; do
  sleep "$INTERVAL"
  find "$WATCH_DIR" \( -name '*.vue' -o -name '*.ts' -o -name '*.tsx' -o -name '*.css' -o -name '*.json' \) -not -path '*/node_modules/*' | while read -r f; do
    HASH_FILE="$HASH_DIR/$(echo "$f" | md5sum | cut -d' ' -f1)"
    NEW_HASH=$(md5sum "$f" | cut -d' ' -f1)
    OLD_HASH=""
    [ -f "$HASH_FILE" ] && OLD_HASH=$(cat "$HASH_FILE")
    if [ "$NEW_HASH" != "$OLD_HASH" ]; then
      echo "$NEW_HASH" > "$HASH_FILE"
      if [ -n "$OLD_HASH" ]; then
        # File actually changed - rewrite it to trigger inotify
        TMPF=$(mktemp)
        cat "$f" > "$TMPF"
        cat "$TMPF" > "$f"
        rm "$TMPF"
        echo "[dev-watch] Changed: $f"
      fi
    fi
  done
done
