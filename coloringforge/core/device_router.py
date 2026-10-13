"""Picks cuda / cpu and enforces a VRAM guard before loading big models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loguru import logger


@dataclass
class DeviceRouter:
    device_cfg: dict[str, Any]

    def __post_init__(self) -> None:
        self.active_device = self._resolve()
        self.half = bool(self.device_cfg.get("half_precision", True)) and self.active_device == "cuda"

    def _resolve(self) -> str:
        prefer = self.device_cfg.get("prefer", "auto")
        if prefer in ("cuda", "cpu"):
            return prefer
        try:
            import torch
            if torch.cuda.is_available():
                free_gb = torch.cuda.mem_get_info()[0] / (1024 ** 3)
                guard = float(self.device_cfg.get("vram_guard_gb", 6))
                if free_gb >= guard:
                    logger.info("CUDA available, {:.1f} GB free", free_gb)
                    return "cuda"
                logger.warning("CUDA present but only {:.1f} GB free (< guard {})", free_gb, guard)
        except Exception as exc:  # noqa: BLE001
            logger.debug("torch probe failed: {}", exc)
        return "cpu"