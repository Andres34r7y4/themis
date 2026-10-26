"""Themis governance assets.

This package ships the Markdown governance contract (agent, loops, roles,
tasks and templates) so that ``themis init`` can scaffold it into any
repository, including when Themis is installed from a wheel.
"""

from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent

__all__ = ["ASSETS_DIR"]
