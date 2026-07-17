# Grading Rubric

The original system's builder said his agents "know what good looks like" and stop at 9/10. That is
not reproducible, so here is the rubric written down. Grade every finished segment with TWO models
(Gemini with the video + render, Claude with contact sheet + rendered stills). A segment passes at
9.0+ from both.

Score each criterion 0-2. Total out of 10.

## 1. Layout fidelity (0-2)
- 2: Every element present, positioned and sized to match; nothing extra invented.
- 1: All elements present but one is noticeably misplaced or missized.
- 0: Missing or invented elements.

## 2. Z-order and stacking (0-2)
- 2: All overlap relationships match the source, including image-behind-text cases.
- 1: One stacking error that does not destroy the composition.
- 0: Foreground/background relationships wrong anywhere it is noticeable.

## 3. Motion direction and distance (0-2)
- 2: Every animated element moves the right way, the right amount, from the right origin.
- 1: One element's direction/origin/distance is off.
- 0: Multiple motions wrong, or a keystone motion (the scene's main idea) wrong.

## 4. Timing and easing feel (0-2)
- 2: Starts and ends within ~100ms of source; easing character matches (snappy stays snappy,
  floaty stays floaty); overlapping motions overlap the same way.
- 1: Timing right but easing feels mechanically different, or one overlap is sequenced wrong.
- 0: The rhythm of the scene is different from the source.

## 5. Polish (0-2)
- 2: Type, color, and image quality make it usable in a real brand video today. No jitter, no
  pop-in artifacts, no default-looking fonts unless the source uses them.
- 1: Structurally right but one polish flaw a client would notice.
- 0: Looks like a programmer's recreation.

## Grader instructions
- Grade independently; do not read the other grader's score first.
- Cite the criterion number for every point deducted, with the timestamp where you saw the problem.
  Deductions without a visible cause do not count.
- A 9 means: a working motion designer would accept this as a draft of the source scene. If you
  would not say that sentence out loud, it is not a 9.
