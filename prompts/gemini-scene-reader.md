# Gemini Scene Reader

Send this prompt to Gemini 3.1 Pro (or newer) together with ONE video segment and its contact
sheet. It returns the scene spec that Claude Code or Codex will execute in Remotion.

---

You are analyzing a short segment of a motion graphics brand video so that a coding agent can
recreate it in Remotion (a React-based video framework). The coding agent cannot watch video. Your
description is everything it will know. Be precise about motion; never say "animates in" when you
can say "slides in from the right over 400ms, decelerating".

Watch the segment and study the contact sheet, then respond in exactly this structure:

## Scene summary
One sentence: what this scene communicates and its overall motion feel (snappy, floaty, mechanical,
elastic).

## Canvas
Background color/gradient/texture. Any global effects (grain, vignette, blur, shader-like washes).

## Elements
Numbered list. For each element:
- What it is (text, image, UI panel, cursor, shape, chart).
- Content: exact text if readable; for images, describe subject and style so a similar one can be
  sourced or generated.
- Position and approximate size relative to the canvas.
- Z-ORDER: state explicitly what is in front of and behind this element. If an image sits behind
  text, say so in both elements' entries. This is the most commonly missed detail.

## Animation timeline
Chronological. For every motion:
- Timestamp range (e.g. 0.0s to 0.8s).
- Element affected.
- Motion: direction, distance, scale change, rotation, opacity.
- Easing feel: linear, ease-out, spring/bounce, overshoot.
- Overlaps: which motions run simultaneously.

## Carry-over
Elements already mid-animation when the segment starts (they belong to the previous scene; the
executor must receive them, not build them). Elements still moving when the segment ends.

## Remotion mapping
For each animation, the Remotion primitives most likely to achieve it (spring(), interpolate(),
Sequence offsets, transforms). If an effect exceeds core Remotion, say what class of technique it
needs (SVG path, canvas shader, particle loop).

## Difficulty flags
Anything you predict the executor will get wrong, ranked. Typical suspects: z-order, overlapping
timelines, text kerning during scale, motion blur fakes.
