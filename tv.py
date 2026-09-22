#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv

from host.hls import write_vod_playlist
from providers import enabled_providers, pick_provider
from providers.base import GenerationRequest
from vj.bumpers import IDENT, ensure_ident, interleave

load_dotenv()


def load_config() -> dict:
    return json.loads(Path("config.json").read_text(encoding="utf-8"))


def prune_library(media: Path, max_clips: int) -> list[Path]:
    clips = sorted(media.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    while len(clips) > max_clips:
        clips.pop(0).unlink(missing_ok=True)
    return clips


def next_name(media: Path, provider: str) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return media / f"{stamp}-{provider}.mp4"


def main() -> None:
    cfg = load_config()
    media = Path(cfg["paths"]["media"])
    media.mkdir(parents=True, exist_ok=True)

    weighted = enabled_providers(cfg["providers"])
    provider = pick_provider(weighted)
    prompt = random.choice(cfg["prompts"])
    dest = next_name(media, provider.name)

    refs = list(Path(cfg["paths"]["originals"]).glob("*"))
    req = GenerationRequest(
        prompt=prompt,
        seconds=int(cfg["station"]["clip_seconds"]),
        width=int(cfg["station"]["target_width"]),
        height=int(cfg["station"]["target_height"]),
        reference=random.choice(refs) if refs else None,
    )
    print(f"generating via {provider.name}: {prompt}")
    provider.generate(req, dest)

    clips = prune_library(media, int(cfg["station"]["max_clips"]))
    bumper = ensure_ident(Path(IDENT))
    sequenced = interleave(clips, int(cfg["station"]["insert_bumper_every"]), bumper)

    public = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1")
    playlist = write_vod_playlist(
        sequenced,
        Path(cfg["paths"]["playlist"]),
        public,
        target_duration=int(cfg["station"]["clip_seconds"]),
    )
    print(f"wrote {playlist} ({len(sequenced)} items)")


if __name__ == "__main__":
    main()
