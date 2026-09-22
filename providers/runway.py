import os
from pathlib import Path

import requests

from .base import GenerationRequest, VideoProvider


class RunwayProvider(VideoProvider):
    name = "runway"

    def available(self) -> bool:
        return bool(os.getenv("RUNWAY_API_KEY"))

    def generate(self, req: GenerationRequest, dest: Path) -> Path:
        # Scaffolding: replace with current Runway endpoint/schema.
        headers = {"Authorization": f"Bearer {os.getenv('RUNWAY_API_KEY')}"}
        payload = {
            "prompt": req.prompt,
            "duration": req.seconds,
            "width": req.width,
            "height": req.height,
        }
        requests.post(
            os.getenv("RUNWAY_API_BASE", "https://api.runwayml.com/v1/generate"),
            json=payload,
            headers=headers,
            timeout=30,
        )
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"")  # replace with downloaded MP4 bytes
        return dest
