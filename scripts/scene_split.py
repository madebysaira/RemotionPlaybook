#!/usr/bin/env python3
"""Split a source video into scene-based segments for the RemotionPlaybook workflow.

Runs scene-cut detection first (PySceneDetect, content mode). Spans that come out longer
than MAX_LEN or shorter than MIN_LEN fall back to fixed-length cuts, because spiky motion
graphics can fool the detector. Force fixed cutting entirely with --fixed N.

Usage:
    python3 scene_split.py source.mp4 out/segments
    python3 scene_split.py source.mp4 out/segments --fixed 5
"""
import argparse
import subprocess
import sys
from pathlib import Path

MIN_LEN = 1.5
MAX_LEN = 8.0


def video_duration(src: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(src)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def detect_scenes(src: Path) -> list[tuple[float, float]]:
    try:
        from scenedetect import detect, ContentDetector
    except ImportError:
        print("PySceneDetect not installed (pip install 'scenedetect[opencv]'). "
              "Falling back to fixed 5s cuts.", file=sys.stderr)
        return []
    scenes = detect(str(src), ContentDetector())
    return [(s.get_seconds(), e.get_seconds()) for s, e in scenes]


def fixed_spans(start: float, end: float, length: float) -> list[tuple[float, float]]:
    spans, t = [], start
    while t < end - 0.05:
        spans.append((t, min(t + length, end)))
        t += length
    return spans


def normalize(spans: list[tuple[float, float]], duration: float,
              fixed_len: float) -> list[tuple[float, float]]:
    if not spans:
        return fixed_spans(0.0, duration, fixed_len)
    result = []
    for start, end in spans:
        length = end - start
        if length > MAX_LEN:
            result.extend(fixed_spans(start, end, fixed_len))
        elif length < MIN_LEN and result:
            # merge stub into the previous span
            prev_start, _ = result[-1]
            result[-1] = (prev_start, end)
        else:
            result.append((start, end))
    return result


def cut(src: Path, spans: list[tuple[float, float]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for i, (start, end) in enumerate(spans, 1):
        dst = outdir / f"segment_{i:02d}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
             "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an", str(dst)],
            check=True)
        print(f"{dst.name}  {start:6.2f}s -> {end:6.2f}s  ({end - start:.2f}s)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source")
    ap.add_argument("outdir")
    ap.add_argument("--fixed", type=float, default=None,
                    help="skip detection, cut every N seconds")
    args = ap.parse_args()

    src, outdir = Path(args.source), Path(args.outdir)
    if not src.exists():
        sys.exit(f"source not found: {src}")

    duration = video_duration(src)
    fixed_len = args.fixed or 5.0
    spans = ([] if args.fixed else detect_scenes(src))
    spans = normalize(spans, duration, fixed_len)
    print(f"{len(spans)} segments from {duration:.1f}s of video")
    cut(src, spans, outdir)


if __name__ == "__main__":
    main()
