# RemotionPlaybook

Recreate any brand video with AI agents, then make it yours.

## Who this is for

You need a brand video that looks like it cost real money. You are not a motion designer, you do not
have weeks for After Effects, and the agency quote made you close the tab. If you can run Claude
Code (or Codex) and paste a YouTube link, this playbook gets you from "video I admire" to "Remotion
project I own" in about 15 minutes per run.

I watched a masterclass interview where a data engineer explained the system he built to do exactly
this. It was genuinely clever. It was also completely undownloadable: no scripts, no prompts, no
playbook file, just a promise to maybe open source one project someday. So I rebuilt the whole
system, wrote down every step, and fixed the gaps he admitted on camera. That is this repo.

## What you get in the first 2 minutes

1. `scripts/` has the exact ffmpeg and Python commands for segmenting a video, extracting frames,
   and building contact sheets. They run as is.
2. `prompts/` has the full agent prompts: the Gemini scene reader, the executor brief for Claude
   Code, and a concrete 10-point grading rubric (the video only says "it knows what good looks
   like" and this repo actually defines it).
3. `playbook/playbook.md` is the complete workflow, in order, with the reasoning behind each step
   so you can adapt it instead of cargo-culting it.

## The system in one paragraph

Take a reference brand video (ElevenLabs, Higgsfield, Adobe Firefly, anything with motion you
admire). Split it into segments. Extract frames and tile them into a contact sheet so models that
cannot watch video can still understand motion. Let Gemini (the only major model that truly reads
video) write a detailed scene spec per segment. Hand that spec plus the frames to Claude Code, which
builds it in Remotion, compares its render against the ground-truth frames, and iterates. Two
graders score each segment against the rubric; only 9/10 or better moves on. Render the MP4. Then
swap in your own brand, colors, screenshots, and copy. You never wrote a keyframe.

## What this repo improves over the source video

| Gap in the video | What this repo does |
|---|---|
| Fixed 5-second cuts (guest admits the number is arbitrary) | Scene-cut detection pre-pass via PySceneDetect, with 5s fallback for spiky motion graphics where detection misfires |
| No downloadable scripts | All segmentation, frame, and contact-sheet commands in `scripts/`, tested |
| Vague grading ("grade is nine, stop") | Explicit 10-point rubric in `prompts/grading-rubric.md` |
| No cost or licensing talk | Model roles and budget notes below, plus an honest licensing section |
| Playbook lives in his head and four private MD files | The whole thing is `playbook/playbook.md` |

## Model roles (and why)

| Role | Model | Why |
|---|---|---|
| Scene understanding | Gemini 3.1 Pro or newer | The one frontier model that natively understands video. Older Gemini versions produce weaker scene specs, do not bother. |
| Code execution | Claude Code (big model, Opus tier) | Best executor once it has a good spec. Small models burn more time than they save here. |
| Second opinion / variety | Codex | Interprets the same spec differently; sometimes its take on an animation is the better one. Optional but useful. |
| Grading | Gemini + Claude together | Two graders with different failure modes catch more than one. |

## Honest notes before you start

**Licensing.** Remotion is free for individuals and companies up to 3 people, and needs a paid
company license beyond that. Check remotion.dev/license before shipping client work.

**On recreating brand videos.** You are studying and rebuilding motion language, the same way every
designer keeps a reference folder. The output you publish should carry your brand, your assets, your
copy. Do not ship someone else's video with the logo swapped.

**It is not hands-off.** The agents iterate autonomously per segment, but you still direct: pick the
reference, reject bad passes early, and push your own visual taste into the templates. The playbook
has checkpoints for exactly this.

## Quick start

```bash
git clone https://github.com/madebysaira/RemotionPlaybook
cd RemotionPlaybook
# 1. Drop your reference video in as source.mp4
# 2. Detect scenes and segment
python3 scripts/scene_split.py source.mp4 out/segments
# 3. Frames + contact sheets per segment
bash scripts/frames_and_sheets.sh out/segments out/frames
# 4. Feed prompts/gemini-scene-reader.md + a segment + its contact sheet to Gemini
# 5. Hand Gemini's spec + prompts/executor-brief.md to Claude Code in a Remotion project
# 6. Grade with prompts/grading-rubric.md, iterate to 9+, render
```

Full detail, including the Remotion project setup and the learnings-file habit that makes run five
better than run one, is in [playbook/playbook.md](playbook/playbook.md).

## Credit

The system described here was explained by the builder of creatively.ai in the FRMWRKD-EXPLAINED
interview ["Remotion Masterclass: The VERY ADVANCED System Behind AI Motion Graphics"](https://youtu.be/PFHVxq1S6F0).
Watch it for the demos and the thinking out loud. This repo is an independent reconstruction with
fixes and additions, not an official release of his kit.
