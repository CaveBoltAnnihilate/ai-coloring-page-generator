"""Wraps a diffusers pipeline; caches the loaded model between jobs."""
from __future__ import annotations

from typing import Any

from loguru import logger
from PIL import Image

from coloringforge.core.device_router import DeviceRouter
from coloringforge.models.generation_request import GenerationRequest
from coloringforge.services.model_registry import ModelRegistry
from coloringforge.utils.seed_utils import resolve_seed


class DiffusionHandler:
    def __init__(self, gen_cfg: dict[str, Any], registry: ModelRegistry, router: DeviceRouter) -> None:
        self.gen_cfg = gen_cfg
        self.registry = registry
        self.router = router
        self._pipe = None

    def _ensure_pipe(self, pipeline_id: str):
        if self._pipe is not None:
            return self._pipe
        weights = self.registry.resolve(pipeline_id)
        logger.info("Loading pipeline {} from {}", pipeline_id, weights)
        from diffusers import StableDiffusionPipeline
        import torch

        dtype = torch.float16 if self.router.half else torch.float32
        self._pipe = StableDiffusionPipeline.from_pretrained(
            str(weights), torch_dtype=dtype, safety_checker=None
        ).to(self.router.active_device)
        return self._pipe

    def generate(self, request: GenerationRequest, source: Image.Image | None) -> Image.Image:
        pipe = self._ensure_pipe(request.pipeline_id)
        seed = resolve_seed(request.seed)
        import torch

        generator = torch.Generator(device=self.router.active_device).manual_seed(seed)
        result = pipe(
            prompt=request.effective_prompt(),
            image=source,
            strength=request.denoise_strength,
            num_inference_steps=request.steps,
            guidance_scale=request.guidance_scale,
            width=request.width,
            height=request.height,
            generator=generator,
        )
        request.seed = seed
        return result.images[0]