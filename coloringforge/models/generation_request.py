"""Request model describing one coloring page job."""
from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, Field

Mode = Literal["text", "photo", "sketch"]


class GenerationRequest(BaseModel):
    prompt: str = ""
    negative_prompt: str = "color, shading, gradient, photorealism"
    source_path: str | None = None
    mode: Mode = "text"
    pipeline_id: str = "lineart-sd15"
    steps: int = Field(default=28, ge=4, le=80)
    guidance_scale: float = Field(default=7.5, ge=1.0, le=20.0)
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    seed: int = -1
    denoise_strength: float = Field(default=0.72, ge=0.1, le=1.0)
    line_weight: int = Field(default=2, ge=1, le=6)
    job_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])

    def effective_prompt(self) -> str:
        base = "clean black and white line art, coloring book page, thick outlines, white background"
        return f"{base}, {self.prompt}".strip(", ")
</｜｜DSML｜｜ parameter>