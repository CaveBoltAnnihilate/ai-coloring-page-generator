"""Bootstrap entry point. Keeps startup thin — all real work lives in core."""
from __future__ import annotations

import sys
from loguru import logger

from coloringforge.core.app_context import AppContext
from coloringforge.utils.logging_setup import configure_logging


def main() -> int:
    configure_logging()
    logger.info("ColoringForge {} starting", __import__("coloringforge").__version__)
    try:
        ctx = AppContext.from_default_config()
        ctx.bootstrap()
        return ctx.run_gui()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    except Exception as exc:  # noqa: BLE001 — top-level guard, log and exit clean
        logger.exception("Fatal startup error: {}", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())