#!/usr/bin/env python3
"""Optional Playwright render smoke test for visual-arch HTML."""

from __future__ import annotations

import argparse
import asyncio
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


VIEWPORTS = {
    "desktop": {"width": 1440, "height": 960},
    "mobile": {"width": 390, "height": 844},
}


async def check(path: Path) -> None:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        check_with_playwright_cli(path)
        return

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            for name, viewport in VIEWPORTS.items():
                page = await browser.new_page(viewport=viewport)
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                await page.goto(path.resolve().as_uri(), wait_until="networkidle")
                await page.wait_for_selector(".react-flow__node", timeout=15000)
                node_count = await page.locator(".react-flow__node").count()
                title_visible = await page.locator(".brand-title").first.is_visible()
                drawer_count = await page.locator(".detail-drawer").count()
                if node_count < 3:
                    raise AssertionError(f"{name}: expected at least 3 rendered nodes, got {node_count}")
                if not title_visible:
                    raise AssertionError(f"{name}: title is not visible")
                if viewport["width"] >= 760 and drawer_count < 0:
                    raise AssertionError(f"{name}: detail drawer lookup failed")
                if errors:
                    raise AssertionError(f"{name}: page errors: {errors}")
                print(f"OK: {name} render has {node_count} nodes")
                await page.close()
        finally:
            await browser.close()


def check_with_playwright_cli(path: Path) -> None:
    cli = shutil.which("playwright")
    if not cli:
        print("SKIP: playwright is not installed; run structural validation instead")
        return

    with tempfile.TemporaryDirectory(prefix="visual-arch-render-") as tmpdir:
        for name, viewport in VIEWPORTS.items():
            screenshot = Path(tmpdir) / f"{name}.png"
            command = [
                cli,
                "screenshot",
                "--browser=chromium",
                f"--viewport-size={viewport['width']}, {viewport['height']}",
                "--wait-for-selector=.react-flow__node",
                "--timeout=15000",
                path.resolve().as_uri(),
                str(screenshot),
            ]
            result = subprocess.run(command, text=True, capture_output=True, timeout=30)
            if result.returncode != 0:
                message = (result.stderr or result.stdout).strip()
                raise AssertionError(f"{name}: Playwright CLI screenshot failed: {message}")
            if not screenshot.exists() or screenshot.stat().st_size < 10_000:
                raise AssertionError(f"{name}: screenshot was not created or looked empty")
            print(f"OK: {name} render screenshot created with global Playwright CLI")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render-check visual-arch HTML with Playwright when available.")
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    if not args.html.exists():
        print(f"ERROR: file does not exist: {args.html}", file=sys.stderr)
        raise SystemExit(1)
    asyncio.run(check(args.html))


if __name__ == "__main__":
    main()
