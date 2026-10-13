"""Bundles finished pages into PDFs for printing or sharing."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class ExportService:
    def __init__(self, export_cfg: dict[str, Any]) -> None:
        self.cfg = export_cfg

    def bundle_pdf(self, pages: Sequence[Path], out_pdf: Path) -> Path:
        c = canvas.Canvas(str(out_pdf), pagesize=letter)
        pw, ph = letter
        for page in pages:
            img = Image.open(page)
            c.drawImage(ImageReader(img), 0, 0, width=pw, height=ph, preserveAspectRatio=True)
            c.showPage()
        c.save()
        return out_pdf