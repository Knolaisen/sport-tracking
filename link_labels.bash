#!/bin/bash

# Run this from inside the 'sport-tracking' folder.
# It will look in ./data/Football2025 for match folders.

BASE_DIR="$(pwd)/data/Football2025"

if [ ! -d "$BASE_DIR" ]; then
  echo "❌ Could not find $BASE_DIR"
  echo "Run this script from the sport-tracking folder (where ./data/Football2025 lives)."
  exit 1
fi

echo "Creating label symlinks under $BASE_DIR ..."

# Find every 'labels' dir under Football2025
find "$BASE_DIR" -type d -name "labels" | while read -r LABEL_DIR; do
    TRAIN_DIR="$LABEL_DIR/train"
    if [ -d "$TRAIN_DIR" ]; then
        # Example:
        # LABEL_DIR = .../RBK-VIKING/labels
        # GAME_DIR  = .../RBK-VIKING
        GAME_DIR="$(dirname "$LABEL_DIR")"
        DATA_LABELS_DIR="$GAME_DIR/data/labels/train"

        # Make sure target dir exists
        mkdir -p "$DATA_LABELS_DIR"

        echo "→ $(realpath --relative-to="$BASE_DIR" "$TRAIN_DIR") → $(realpath --relative-to="$BASE_DIR" "$DATA_LABELS_DIR")"

        count=0
        for LABEL_FILE in "$TRAIN_DIR"/*.txt; do
            [ -e "$LABEL_FILE" ] || continue
            ln -sf "$LABEL_FILE" "$DATA_LABELS_DIR/$(basename "$LABEL_FILE")"
            count=$((count + 1))
        done

        echo "   linked $count label file(s)"
    fi
done

echo "✅ Done."

