# The Playbook

The full workflow for recreating a brand video in Remotion with AI agents. Read once top to bottom
before running anything. Each step says what to do, what tool does it, and why it exists, because
half the value is knowing which steps you can bend.

## 0. Setup (once)

- Node 18+ and a Remotion project: `npx create-video@latest` (pick the blank template).
- Add Remotion's official agent skills to Claude Code. Remotion's docs are agent-ready: paste any
  doc URL into Claude Code and it fetches markdown automatically (remotion.dev/docs/ai). The skills
  are the single biggest quality unlock. Without them the agent does not know what Remotion can do,
  and you get generic fades.
- ffmpeg installed. Python 3.10+ with `scenedetect[opencv]` and `Pillow` for the scripts.
- API access to Gemini 3.1 Pro or newer. Older versions write mushy scene specs.

## 1. Pick a reference video

Pick motion you actually admire, not just a famous brand. Good references have one clear animation
idea per scene. Dense videos with three overlapping ideas per second (some Higgsfield spots) are
recreatable but cost far more iterations.

Save it as `source.mp4`. Keep it under ~90 seconds for a first run.

## 2. Segment it

```bash
python3 scripts/scene_split.py source.mp4 out/segments
```

The script runs scene-cut detection first (PySceneDetect content mode). If detection produces
segments longer than 8s or shorter than 1.5s, it falls back to fixed 5-second cuts for those spans.

Why hybrid: the original system used fixed 5s cuts and its builder admitted the number was
arbitrary. Cut-detection gives each segment exactly one animation idea, which is what the executor
agent needs. But motion graphics with constant spikes can fool the detector, so the 5s fallback
stays. If your segments look wrong, force fixed mode with `--fixed 5`.

## 3. Frames and contact sheets

```bash
bash scripts/frames_and_sheets.sh out/segments out/frames
```

Per segment this produces: 6 evenly-spaced frames, plus one contact sheet (a 3x2 tiled collage,
timestamped). The contact sheet is the trick that lets non-video models reason about motion: start
state, in-between states, end state, all in one image. Claude Code cannot watch video; it can read
a contact sheet.

## 4. Gemini writes the scene spec

For each segment, send Gemini:
- the segment video file,
- the contact sheet,
- the prompt in `prompts/gemini-scene-reader.md`.

Gemini returns a structured scene spec: elements present, layout, every animation with direction,
easing, timing, overlaps, plus which Remotion primitives most likely achieve it. Collect all specs
into one `scene-playbook.md` for the video.

Do not skip the images-in-scene section of the spec. Good motion graphics look good largely because
of the images in them; the spec tells the executor what image content to source or generate.

## 5. Claude Code executes, one segment at a time

Open your Remotion project in Claude Code. Give it `prompts/executor-brief.md`, the scene spec for
segment 1, and that segment's frames. The brief tells it to: build a first pass, render stills at
the same timestamps as the ground-truth frames, compare, and iterate.

One agent owns one segment. Do not let it wander across the whole timeline; overlap bugs multiply.

## 6. Grade to 9, then move on

After each iteration, grade with `prompts/grading-rubric.md`, using both Gemini and Claude as
graders. The rubric scores layout fidelity, animation direction, easing feel, timing, and polish on
explicit criteria. A segment needs 9/10 from both graders to be done.

You are the third grader. If a pass looks wrong at a glance, say exactly what is wrong ("the panel
should slide from the right, and the text is too early") and restart the pass. Vague displeasure
produces vague fixes.

## 7. Render and repurpose

When all segments pass, stitch and render. Now make it yours:
- Swap reference images for your product shots or generated brand assets.
- Change copy, colors, and type to your brand system.
- Keep the motion. The motion is what you were buying.

## 8. Capture learnings (the compounding step)

After every video, tell Claude Code: "Update learnings.md with every effect we built, the prompts
that produced them, and the mistakes we fixed." Effects you liked become named, reusable patterns.
This file is why run five takes 10 minutes and run one took a day. Over time it becomes your taste,
written down, and you stop needing reference videos for standard scenes.

## Cost and time expectations

With the setup above: roughly 10-15 minutes of agent runtime per minute of source video once your
learnings file is warm, longer on the first runs. Use the biggest reasoning models for the executor
and graders; small models spend more of your time than they save money. Video calls to Gemini are
the main API cost; contact sheets exist partly to keep those calls small (send the sheet, not the
whole video, for grading passes).

## Failure modes we hit so you do not

- **Image behind text.** Both executors reliably miss that a background image sits behind
  foreground text and build them as siblings. The scene-reader prompt now asks for explicit z-order,
  and the rubric checks it.
- **Animation overlap at segment boundaries.** An element mid-flight at a cut belongs to both
  segments. The spec marks carry-over elements; the executor brief says to receive them, not
  recreate them.
- **Detector overcutting on spiky motion.** See the `--fixed 5` fallback in step 2.
- **Generic first passes.** If the first pass looks like a template, the agent is missing the
  Remotion skills context. Fix the setup, do not iterate through it.
