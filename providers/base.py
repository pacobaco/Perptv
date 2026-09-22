from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class GenerationRequest:
    prompt: str
    seconds: int
    width: int
    height: int
    reference: Path | None = None


class VideoProvider:
    name = "base"

    def available(self) -> bool:
        return False

    def generate(self, req: GenerationRequest, dest: Path) -> Path:
        raise NotImplementedError
