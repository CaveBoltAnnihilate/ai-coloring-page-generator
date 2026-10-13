"""Headless CLI: coloringforge generate --prompt '...' --out out.png"""
from __future__ import annotations

import click
from loguru import logger

from coloringforge.core.app_context import AppContext
from coloringforge.models.generation_request import GenerationRequest


@click.group()
def cli() -> None:
    """ColoringForge headless interface."""


@cli.command()
@click.option("--prompt", required=True, help="Text prompt describing the page.")
@click.option("--source", default=None, help="Optional source image to stylize.")
@click.option("--steps", default=28, type=int)
@click.option("--seed", default=-1, type=int)
def generate(prompt: str, source: str | None, steps: int, seed: int) -> None:
    ctx = AppContext.from_default_config()
    ctx.bootstrap()
    req = GenerationRequest(prompt=prompt, source_path=source, steps=steps, seed=seed)
    result = ctx.pipeline.run(req)
    logger.success("Wrote {}", result.image_path)


if __name__ == "__main__":
    cli()