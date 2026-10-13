"""Page composition: margins, bleed, optional cover sheet."""
from __future__ import annotations

from typing import Any

from PIL import Image, ImageOps

MM_PER_INCH = 25.4
PAGE_SIZES = {
    "letter": (8.5, 11.0),
    "a4": (8.27, 11.69),
    "square": (8.0, 8.0),
}


class PostprocessHandler:
    def __init__(self, export_cfg: dict[str, Any]) -> None:
        self.cfg = export_cfg

    def finalize(self, line_art: Image.Image, request) -> Image.Image:
        dpi = int(self.cfg.get("dpi", 300))
        pw_in, ph_in = PAGE_SIZES.get(self.cfg.get("page_size", "letter"), PAGE_SIZES["letter"])
        margin_px = int(self.cfg.get("margin_mm", 12) / MM_PER_INCH * dpi)
        page = Image.new("L", (int(pw_in * dpi), int(ph_in * dpi)), 255)

        avail = (page.width - 2 * margin_px, page.height - 2 * margin_px)
        fitted = ImageOps.contain(line_art, avail, Image.LANCZOS)
        page.paste(fitted, ((page.width - fitted.width) // 2, margin_px), fitted)
        return page