"""Application context — owns config, services, and the Qt application."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from loguru import logger

from coloringforge.core.pipeline import ColoringPipeline
from coloringforge.core.device_router import DeviceRouter
from coloringforge.services.model_registry import ModelRegistry
from coloringforge.services.export_service import ExportService
from coloringforge.utils.config_loader import load_config


@dataclass
class AppContext:
    config: dict[str, Any]
    registry: ModelRegistry = field(init=False)
    pipeline: ColoringPipeline = field(init=False)
    exporter: ExportService = field(init=False)
    device_router: DeviceRouter = field(init=False)

    @classmethod
    def from_default_config(cls) -> "AppContext":
        cfg = load_config(Path("config/default.yaml"))
        return cls(config=cfg)

    def bootstrap(self) -> None:
        self.device_router = DeviceRouter(self.config["device"])
        self.registry = ModelRegistry(self.config["paths"]["models_dir"])
        self.pipeline = ColoringPipeline(self.config, self.registry, self.device_router)
        self.exporter = ExportService(self.config["export"])
        logger.info("AppContext bootstrapped on device={}", self.device_router.active_device)

    def run_gui(self) -> int:
        from coloringforge.handlers.gui_handler import launch_gui
        return launch_gui(self)