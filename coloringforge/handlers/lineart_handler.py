"""Extract clean black line art from a rendered image."""
from __future__ import annotations

from typing import Any

import cv2
import numpy as np
from PIL import Image


class LineArtHandler:
    def __init__(self, gen_cfg: dict[str, Any]) -> None:
        self.cfg = gen_cfg

    def extract(self, image: Image.Image, line_weight: int = 2) -> Image.Image:
        gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        dodge = cv2.divide(inv, 255 - blur, scale=256)
        _, binary = cv2.threshold(
            dodge,
            int(self.cfg.get("threshold_block", 14)),
            int(self.cfg.get("threshold_c", 42)),
            cv2.THRESH_BINARY,
        )
        kernel = np.ones((line_weight, line_weight), np.uint8)
        thick = cv2.dilate(binary, kernel, iterations=1)
        return Image.fromarray(255 - thick).convert("L")