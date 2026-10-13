"""Generation pipeline: preprocess -> diffuse -> line-extract -> postprocess."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger
from PIL import Image

from coloringforge.core.device_router import DeviceRouter
from coloringforge.models.generation_request import GenerationRequest
from coloringforge.models.generation_result import GenerationResult
from coloringforge.services.model_registry import ModelRegistry
from coloringforge.handlers.preprocess_handler import PreprocessHandler
from coloringforge.handlers.diffusion_handler import DiffusionHandler
from coloringforge.handlers.lineart_handler import LineArtHandler
from coloringforge.handlers.postprocess_handler import PostprocessHandler


@dataclass
class ColoringPipeline:
    config: dict[str, Any]
    registry: ModelRegistry
    device_router: DeviceRouter

    def __post_init__(self) -> None:
        self.pre = PreprocessHandler(self.config["preprocess"])
        self.diff = DiffusionHandler(self.config["generation"], self.registry, self.device_router)
        self.line = LineArtHandler(self.config["generation"])
        self.post = PostprocessHandler(self.config["export"])

    def run(self, request: GenerationRequest) -> GenerationResult:
        logger.info("Pipeline run: mode={} prompt={!r}", request.mode, request.prompt[:60])
        source: Image.Image | None = None
        if request.source_path:
            source = self.pre.load_and_normalize(Path(request.source_path))

        rendered = self.diff.generate(request, source)
        line_art = self.line.extract(rendered, request.line_weight)
        final = self.post.finalize(line_art, request)

        out_path = Path(self.config["paths"]["output_dir"]) / f"{request.job_id}.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        final.save(out_path, "PNG", dpi=(self.config["export"]["dpi"],) * 2)
        logger.info("Pipeline complete -> {}", out_path)
        return GenerationResult(job_id=request.job_id, image_path=out_path, seed=request.seed)