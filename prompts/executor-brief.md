# Executor Brief (Claude Code / Codex)

Give this to the coding agent inside your Remotion project, together with ONE scene spec from the
Gemini scene reader and that segment's extracted frames.

---

You are recreating one segment of a motion graphics video in Remotion. You own exactly this segment;
do not touch other segments' compositions.

Inputs you have:
1. A scene spec written by a video-capable model. Trust it for motion and timing; it saw the video
   and you did not.
2. Ground-truth frames from the original segment at known timestamps.
3. The Remotion skills / best-practices docs in your context.

Process, in order:
1. Read the spec fully. List the elements, the z-order, and the timeline before writing code.
2. Build a first pass as a self-contained `<Composition>` for this segment. Respect carry-over
   elements: receive them via props in their mid-flight state; never rebuild their entrance.
3. Source images per the spec (public sources like Pexels/Pixabay, or generate to the description).
   Placeholder gray boxes are acceptable only in pass one.
4. Render stills at the exact ground-truth timestamps
   (`npx remotion still <comp> --frame=<n>`), and compare against the ground-truth frames yourself:
   layout, z-order, motion state at that instant, easing feel implied between adjacent stills.
5. State your differences honestly, fix, re-render, repeat. Do not declare a pass finished while a
   listed difference remains.
6. When you believe the segment is a 9/10 against the grading rubric, stop and present: the still
   comparisons, what you compromised on and why.

Hard rules:
- If the spec says an image is BEHIND text, build it behind the text. Check z-order in your still
  comparison every pass; this is the most common failure.
- Use spring() for anything the spec calls bouncy/elastic; use interpolate() with easing for the
  rest. Linear motion is almost always wrong in brand videos.
- No magic numbers scattered in JSX: keep timing constants at the top of the file so a human can
  retune the feel in one place.
