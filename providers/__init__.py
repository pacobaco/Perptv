from __future__ import annotations

import os
import random
from typing import Iterable

from .base import VideoProvider
from .kling import KlingProvider
from .luma import LumaProvider
from .pika import PikaProvider
from .runway import RunwayProvider

REGISTRY = {
    "runway": RunwayProvider,
    "kling": KlingProvider,
    "luma": LumaProvider,
    "pika": PikaProvider,
}


def enabled_providers(entries: Iterable[dict]) -> list[tuple[int, VideoProvider]]:
    out: list[tuple[int, VideoProvider]] = []
    for entry in entries:
        cls = REGISTRY.get(entry["name"])
        if not cls or not entry.get("enabled", True):
            continue
        provider = cls()
        if provider.available():
            out.append((max(1, int(entry.get("weight", 1))), provider))
    return out


def pick_provider(weighted: list[tuple[int, VideoProvider]]) -> VideoProvider:
    names = []
    for weight, provider in weighted:
        names.extend([provider] * weight)
    if not names:
        raise RuntimeError("No video providers have credentials")
    return random.choice(names)


def env_set(*keys: str) -> bool:
    return all(os.getenv(k) for k in keys)
