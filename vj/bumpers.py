from __future__ import annotations

import subprocess
from pathlib import Path


IDENT = "station/overlays/perptv-ident.mp4"


def ensure_ident(path: Path, seconds: int = 4) -> Path:
    """Build a silent color ident if no designed bumper exists."""
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x111111:s=1280x720:d={seconds}",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-vf", "drawtext=text='PERPTV':fontcolor=yellow:fontsize=96:x=(w-text_w)/2:y=(h-text_h)/2",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            str(path),
        ],
        check=True,
    )
    return path


def interleave(clips: list[Path], every: int, bumper: Path) -> list[Path]:
    if every <= 0:
        return clips
    out: list[Path] = []
    for i, clip in enumerate(clips, start=1):
        out.append(clip)
        if i % every == 0:
            out.append(bumper)
    return out
