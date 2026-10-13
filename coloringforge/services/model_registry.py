"""Resolves pipeline IDs to local weight directories; downloads on miss."""
from __future__ import annotations

from pathlib import Path

from loguru import logger

KNOWN_PIPELINES = {
    "lineart-sd15": "stable-diffusion-v1-5-lineart",
    "lineart-sdxl": "stable-diffusion-xl-lineart",
    "sketch-canny": "controlnet-canny-sd15",
}


class ModelRegistry:
    def __init__(self, models_dir: str | Path) -> None:
        self.root = Path(models_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, pipeline_id: str) -> Path:
        if pipeline_id not in KNOWN_PIPELINES:
            raise KeyError(f"Unknown pipeline '{pipeline_id}'. Known: {sorted(KNOWN_PIPELINES)}")
        target = self.root / KNOWN_PIPELINES[pipeline_id]
        if not target.exists():
            logger.warning("Weights missing at {} — run `coloringforge fetch`", target)
            raise FileNotFoundError(target)
        return target

    def available(self) -> list[str]:
        return [pid for pid, folder in KNOWN_PIPELINES.items() if (self.root / folder).exists()]