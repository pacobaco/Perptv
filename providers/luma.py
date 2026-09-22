import os
from pathlib import Path

from .base import GenerationRequest, VideoProvider


class LumaProvider(VideoProvider):
    name = "luma"

    def available(self) -> bool:
        return bool(os.getenv("LUMA_API_KEY"))

    def generate(self, req: GenerationRequest, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"")
        return dest
