"""Load user images and normalize them for the diffusion stage."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image


class PreprocessHandler:
    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg

    def load_and_normalize(self, path: Path) -> Image.Image:
        img = Image.open(path).convert("RGB")
        max_edge = int(self.cfg.get("max_edge_px", 2048))
        w, h = img.size
        if max(w, h) > max_edge:
            scale = max_edge / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        arr = np.asarray(img)
        if self.cfg.get("grayscale", True):
            arr = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)
        if self.cfg.get("auto_contrast", True):
            arr = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX)
        k = int(self.cfg.get("blur_kernel", 3))
        if k > 1:
            arr = cv2.GaussianBlur(arr, (k, k), 0)
        return Image.fromarray(arr)