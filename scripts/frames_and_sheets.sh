#!/usr/bin/env bash
# Extract per-segment frames and build contact sheets for the RemotionPlaybook workflow.
#
# For every segment_*.mp4 in SEGMENTS_DIR this produces, under OUT_DIR/<segment name>/:
#   frame_1.png .. frame_6.png   six evenly spaced ground-truth frames
#   contact_sheet.png            3x2 tiled collage with frame numbers, for non-video models
#
# Usage: bash frames_and_sheets.sh out/segments out/frames

set -euo pipefail

SEGMENTS_DIR="${1:?usage: frames_and_sheets.sh SEGMENTS_DIR OUT_DIR}"
OUT_DIR="${2:?usage: frames_and_sheets.sh SEGMENTS_DIR OUT_DIR}"
FRAMES=6

for seg in "$SEGMENTS_DIR"/segment_*.mp4; do
  name="$(basename "$seg" .mp4)"
  dst="$OUT_DIR/$name"
  mkdir -p "$dst"

  dur=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$seg")

  # 6 evenly spaced frames, avoiding the exact first/last frame (often mid-transition)
  for i in $(seq 1 $FRAMES); do
    ts=$(python3 -c "print(f'{$dur * $i / ($FRAMES + 1):.3f}')")
    ffmpeg -y -loglevel error -ss "$ts" -i "$seg" -frames:v 1 "$dst/frame_$i.png"
  done

  # 3x2 contact sheet with frame index labels
  ffmpeg -y -loglevel error \
    -i "$dst/frame_1.png" -i "$dst/frame_2.png" -i "$dst/frame_3.png" \
    -i "$dst/frame_4.png" -i "$dst/frame_5.png" -i "$dst/frame_6.png" \
    -filter_complex "\
      [0]scale=640:-1,drawtext=text='1':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[a];\
      [1]scale=640:-1,drawtext=text='2':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[b];\
      [2]scale=640:-1,drawtext=text='3':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[c];\
      [3]scale=640:-1,drawtext=text='4':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[d];\
      [4]scale=640:-1,drawtext=text='5':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[e];\
      [5]scale=640:-1,drawtext=text='6':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[f];\
      [a][b][c]hstack=3[top];[d][e][f]hstack=3[bottom];[top][bottom]vstack=2" \
    "$dst/contact_sheet.png"

  echo "$name: $FRAMES frames + contact sheet -> $dst"
done
