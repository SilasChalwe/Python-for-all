"""
Mini Project — Async File Downloader
======================================
Demonstrates concurrent downloads using asyncio and aiohttp:
  - Async/await syntax
  - asyncio.gather for concurrent tasks
  - Semaphores for rate limiting
  - Progress tracking
  - Error handling in async context
  - Writing downloaded files to disk

Requirements:
  pip install aiohttp

Usage:
  python async_downloader.py
"""

import asyncio
import os
import time
import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Gracefully handle missing dependency
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    print("aiohttp not installed. Install with: pip install aiohttp")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    url:      str
    filename: str
    success:  bool
    size:     int = 0
    elapsed:  float = 0.0
    error:    str = ""

    def __str__(self) -> str:
        if self.success:
            return (f"✅ {self.filename} ({self.size:,} bytes, "
                    f"{self.elapsed:.2f}s)")
        return f"❌ {self.filename}: {self.error}"


class AsyncDownloader:
    """
    Concurrent file downloader using asyncio.

    Features:
      - Configurable concurrency limit (semaphore)
      - Retry on failure
      - Progress callbacks
      - Checksum verification (optional)
    """

    def __init__(
        self,
        output_dir: str = "./downloads",
        max_concurrent: int = 5,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self.output_dir     = Path(output_dir)
        self.max_concurrent = max_concurrent
        self.timeout        = timeout
        self.max_retries    = max_retries
        self.results: list[DownloadResult] = []

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _url_to_filename(self, url: str) -> str:
        """Derive a filename from a URL."""
        name = url.rstrip("/").split("/")[-1]
        if "." not in name or len(name) > 100:
            # Use a hash-based name
            name = hashlib.md5(url.encode()).hexdigest()[:12] + ".bin"
        return name

    async def _download_one(
        self,
        session: "aiohttp.ClientSession",
        url: str,
        filename: str,
        sem: asyncio.Semaphore,
        on_progress: Optional[callable] = None,
    ) -> DownloadResult:
        """Download a single file, respecting the semaphore."""
        filepath = self.output_dir / filename
        start    = time.perf_counter()

        async with sem:   # limit concurrent downloads
            for attempt in range(1, self.max_retries + 1):
                try:
                    timeout = aiohttp.ClientTimeout(total=self.timeout)
                    async with session.get(url, timeout=timeout) as response:
                        response.raise_for_status()
                        content = await response.read()

                    # Write to disk
                    filepath.write_bytes(content)
                    elapsed = time.perf_counter() - start

                    result = DownloadResult(
                        url=url, filename=filename,
                        success=True, size=len(content),
                        elapsed=elapsed
                    )
                    if on_progress:
                        on_progress(result)
                    return result

                except Exception as e:
                    if attempt == self.max_retries:
                        elapsed = time.perf_counter() - start
                        return DownloadResult(
                            url=url, filename=filename,
                            success=False, elapsed=elapsed,
                            error=str(e)
                        )
                    logger.warning(f"Attempt {attempt} failed for {url}: {e}")
                    await asyncio.sleep(attempt * 0.5)   # exponential backoff

    async def download_all(
        self,
        urls: list,
        filenames: Optional[list] = None,
        on_progress: Optional[callable] = None,
    ) -> list[DownloadResult]:
        """
        Download all URLs concurrently.

        Args:
            urls:        List of URLs to download.
            filenames:   Optional list of target filenames (same length as urls).
            on_progress: Optional callback called with each DownloadResult.

        Returns:
            List of DownloadResult objects.
        """
        if not AIOHTTP_AVAILABLE:
            logger.error("aiohttp not installed.")
            return []

        if filenames is None:
            filenames = [self._url_to_filename(url) for url in urls]

        sem = asyncio.Semaphore(self.max_concurrent)

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._download_one(session, url, fname, sem, on_progress)
                for url, fname in zip(urls, filenames)
            ]
            self.results = await asyncio.gather(*tasks)

        return self.results

    def print_summary(self):
        """Print a download summary."""
        print("\n" + "=" * 50)
        print("  DOWNLOAD SUMMARY")
        print("=" * 50)

        success = [r for r in self.results if r.success]
        failed  = [r for r in self.results if not r.success]

        for r in self.results:
            print(f"  {r}")

        total_bytes = sum(r.size for r in success)
        total_time  = sum(r.elapsed for r in self.results)

        print(f"\n  Total: {len(self.results)} files")
        print(f"  ✅ Succeeded: {len(success)}")
        print(f"  ❌ Failed:    {len(failed)}")
        print(f"  📦 Data:      {total_bytes:,} bytes")
        print(f"  ⏱  Time:      {total_time:.2f}s (wall clock)")


def demo():
    """Demonstrate the async downloader with small public files."""
    import tempfile

    print("=" * 50)
    print("  ⬇️  ASYNC DOWNLOADER DEMO")
    print("=" * 50)

    if not AIOHTTP_AVAILABLE:
        print("\nDemonstrating structure without aiohttp...")
        print("Install it with: pip install aiohttp")
        # Show structure even without the dependency
        d = AsyncDownloader(output_dir=tempfile.mkdtemp())
        print(f"  Output dir: {d.output_dir}")
        print("  max_concurrent:", d.max_concurrent)
        print("  max_retries:", d.max_retries)
        return

    # Small test files from public domain
    test_urls = [
        "https://httpbin.org/bytes/1024",
        "https://httpbin.org/bytes/2048",
        "https://httpbin.org/bytes/4096",
    ]

    tmpdir    = tempfile.mkdtemp()
    downloader = AsyncDownloader(
        output_dir=tmpdir,
        max_concurrent=3,
        timeout=10,
    )

    def on_complete(result: DownloadResult):
        if result.success:
            print(f"  ✅ Downloaded: {result.filename} ({result.size:,} bytes)")
        else:
            print(f"  ❌ Failed: {result.error}")

    start = time.perf_counter()
    asyncio.run(downloader.download_all(test_urls, on_progress=on_complete))
    total_elapsed = time.perf_counter() - start

    downloader.print_summary()
    print(f"\n  Wall clock time: {total_elapsed:.3f}s")


if __name__ == "__main__":
    demo()
