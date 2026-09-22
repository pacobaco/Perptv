from __future__ import annotations

from pathlib import Path


def write_vod_playlist(clips: list[Path], dest: Path, public_base: str, target_duration: int = 8) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        f"#EXT-X-TARGETDURATION:{target_duration}",
        "#EXT-X-MEDIA-SEQUENCE:0",
        "#EXT-X-PLAYLIST-TYPE:VOD",
    ]
    for clip in clips:
        url = f"{public_base.rstrip('/')}/media/{clip.name}"
        lines.append(f"#EXTINF:{target_duration:.3f},")
        lines.append(url)
    lines.append("#EXT-X-ENDLIST")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dest
