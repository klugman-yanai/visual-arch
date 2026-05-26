#!/usr/bin/env python3
"""Optional Playwright render smoke test for map-it HTML."""

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
NODE_WAIT_MS = 45_000
DRAWER_WAIT_MS = 10_000


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
                await page.wait_for_selector(".react-flow__node, .arch-node", timeout=NODE_WAIT_MS)
                react_nodes = await page.locator(".react-flow__node").count()
                vanilla_nodes = await page.locator(".arch-node").count()
                node_count = react_nodes or vanilla_nodes
                arch_nodes = page.locator(".react-flow__node-arch, .arch-node")
                title_visible = await page.locator(".brand-title").first.is_visible()
                if node_count < 3:
                    raise AssertionError(f"{name}: expected at least 3 rendered nodes, got {node_count}")
                if await arch_nodes.count() < 3:
                    raise AssertionError(f"{name}: expected at least 3 architecture nodes")
                if not title_visible:
                    raise AssertionError(f"{name}: title is not visible")
                duplicate_controls = await page.evaluate(
                    """
                    () => {
                        const visible = (el) => {
                            const style = window.getComputedStyle(el);
                            const rect = el.getBoundingClientRect();
                            return style.visibility !== 'hidden'
                                && style.display !== 'none'
                                && rect.width > 0
                                && rect.height > 0;
                        };
                        const labels = Array.from(document.querySelectorAll('button'))
                            .filter((button) => visible(button))
                            .filter((button) => !button.closest('.detail-drawer'))
                            .map((button) => (
                                button.getAttribute('aria-label')
                                || button.getAttribute('title')
                                || button.textContent
                                || ''
                            ).trim().replace(/\\s+/g, ' '))
                            .filter(Boolean);
                        const counts = labels.reduce((acc, label) => {
                            acc[label] = (acc[label] || 0) + 1;
                            return acc;
                        }, {});
                        return Object.entries(counts)
                            .filter(([, count]) => count > 1)
                            .map(([label, count]) => `${label} (${count})`);
                    }
                    """
                )
                if duplicate_controls:
                    raise AssertionError(f"{name}: duplicate visible controls: {', '.join(duplicate_controls)}")
                await arch_nodes.first.click()
                await page.wait_for_selector(".detail-drawer .source-chip", timeout=DRAWER_WAIT_MS)
                drawer_count = await page.locator(".detail-drawer").count()
                selected_title = await page.locator(".detail-drawer .drawer-title").first.text_content()
                source_count = await page.locator(".detail-drawer .source-chip").count()
                if drawer_count < 1 or not selected_title or source_count < 1:
                    raise AssertionError(f"{name}: selecting a node did not expose detail/source content")
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

    with tempfile.TemporaryDirectory(prefix="map-it-render-") as tmpdir:
        for name, viewport in VIEWPORTS.items():
            screenshot = Path(tmpdir) / f"{name}.png"
            command = [
                cli,
                "screenshot",
                "--browser=chromium",
                f"--viewport-size={viewport['width']}, {viewport['height']}",
                "--wait-for-selector=.react-flow__node,.arch-node",
                f"--timeout={NODE_WAIT_MS}",
                path.resolve().as_uri(),
                str(screenshot),
            ]
            result = subprocess.run(command, text=True, capture_output=True, timeout=60)
            if result.returncode != 0:
                message = (result.stderr or result.stdout).strip()
                raise AssertionError(f"{name}: Playwright CLI screenshot failed: {message}")
            if not screenshot.exists() or screenshot.stat().st_size < 10_000:
                raise AssertionError(f"{name}: screenshot was not created or looked empty")
            print(f"OK: {name} render screenshot created with global Playwright CLI")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render-check map-it HTML with Playwright when available.")
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    if not args.html.exists():
        print(f"ERROR: file does not exist: {args.html}", file=sys.stderr)
        raise SystemExit(1)
    asyncio.run(check(args.html))


if __name__ == "__main__":
    main()
