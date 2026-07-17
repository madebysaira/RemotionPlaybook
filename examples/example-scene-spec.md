# Example: a filled-in scene spec

What a good Gemini scene-reader output looks like, so you can judge whether yours are detailed
enough. This one describes a common brand-video scene: a prompt bar with typed text, then a
generated image card sliding in.

## Scene summary
A user "types" a prompt and the product answers with a generated image card; motion feel is snappy
with one soft spring on the card entrance.

## Canvas
Near-black background (#0B0B0F) with a subtle radial gradient lightening toward center, faint film
grain across the whole frame.

## Elements
1. Prompt bar. Rounded rectangle, centered horizontally, 55% canvas width, sitting at 62% height.
   Dark gray fill (#1A1A22), 1px lighter border. Contains placeholder text then typed text
   "a lighthouse at dusk, cinematic". IN FRONT of background, BEHIND nothing.
2. Typing caret. 2px white vertical bar inside the prompt bar, blinks at ~1Hz while idle.
3. Image card. Rounded rectangle, 38% canvas width, 4:5 ratio, positioned upper right (72% x, 30%
   y). Contains a photographic image: lighthouse on a cliff at dusk, warm sky, cinematic grade.
   IN FRONT of background. The label (element 4) sits ON TOP of this card, bottom-left corner.
4. Label chip on card. Small pill, white text "Generated in 4s", dark translucent fill. IN FRONT of
   image card.

## Animation timeline
- 0.0s to 0.3s: prompt bar fades in (opacity 0→1) and rises 24px, ease-out.
- 0.3s to 1.6s: text types character by character, ~28 chars/s, caret visible throughout.
- 1.6s to 1.75s: caret blinks off, prompt bar dims slightly (opacity 1→0.85).
- 1.75s to 2.4s: image card enters from right edge, slide distance ~30% canvas width, spring with
  slight overshoot (~4px past rest, settles once). Simultaneously scales 0.92→1.0.
- 2.4s to 2.7s: label chip fades in on the card, no movement.
- 2.7s to end: hold; grain and caret-blink are the only motion.

## Carry-over
Nothing enters mid-flight. The image card and chip are still on screen at cut; the next scene
receives them at rest.

## Remotion mapping
- Prompt bar entrance: interpolate() on opacity + translateY with Easing.out(Easing.cubic).
- Typing: derive visible substring from frame index; caret via frame % blink math.
- Card entrance: spring() with damping ~12 for the overshoot; drive translateX and scale from the
  same spring value.
- Grain: looping noise PNG at low opacity, or a tiny canvas shader if you have one already.

## Difficulty flags
1. The chip must be a child of the card (moves with it during the spring), not a sibling.
2. Overshoot amount is subtle; damping too low reads as cartoonish immediately.
3. Typing speed varies slightly in the source; constant speed reads fine, do not overfit.
