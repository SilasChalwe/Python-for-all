"""
Mini Project — Web Scraper
============================
A reusable web scraper that demonstrates:
  - OOP design with a base Scraper class
  - requests session with retry logic
  - BeautifulSoup for HTML parsing
  - Extracting structured data
  - Rate limiting and polite scraping
  - Saving results to JSON

Requirements:
  pip install requests beautifulsoup4

Usage:
  python web_scraper.py
"""

import json
import time
import logging
from dataclasses import dataclass, asdict
from typing import Optional
from urllib.parse import urljoin, urlparse

# Gracefully handle missing dependencies
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from bs4 import BeautifulSoup
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False
    print("Missing dependencies. Install with: pip install requests beautifulsoup4")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ScrapedArticle:
    """Represents a scraped article or page."""
    title:   str
    url:     str
    summary: str = ""
    tags:    list = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict:
        return asdict(self)


class WebScraper:
    """
    A polite, reusable web scraper with:
    - Automatic retry on failure
    - Rate limiting (delay between requests)
    - Rotating user agents
    - BeautifulSoup parsing
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    ]

    def __init__(self, delay: float = 1.0, timeout: int = 10, max_retries: int = 3):
        """
        Args:
            delay:       Seconds to wait between requests (be polite!).
            timeout:     Request timeout in seconds.
            max_retries: Number of automatic retries on failure.
        """
        self.delay       = delay
        self.timeout     = timeout
        self._agent_idx  = 0
        self.session     = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> "requests.Session":
        """Create a requests Session with automatic retry logic."""
        if not DEPS_AVAILABLE:
            return None
        session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://",  adapter)
        session.mount("https://", adapter)
        return session

    @property
    def _headers(self) -> dict:
        """Rotate user agents to be less detectable."""
        agent = self.USER_AGENTS[self._agent_idx % len(self.USER_AGENTS)]
        self._agent_idx += 1
        return {"User-Agent": agent, "Accept-Language": "en-US,en;q=0.9"}

    def fetch(self, url: str) -> Optional["BeautifulSoup"]:
        """Fetch a URL and return a BeautifulSoup object, or None on failure."""
        if not DEPS_AVAILABLE:
            logger.error("Dependencies not installed.")
            return None
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, headers=self._headers, timeout=self.timeout)
            response.raise_for_status()
            time.sleep(self.delay)   # rate limiting
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_links(self, soup: "BeautifulSoup", base_url: str) -> list:
        """Extract all absolute links from a page."""
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            absolute = urljoin(base_url, href)
            if urlparse(absolute).scheme in ("http", "https"):
                links.append(absolute)
        return list(set(links))   # deduplicate

    def extract_text(self, soup: "BeautifulSoup") -> str:
        """Extract clean text from a page, removing scripts/styles."""
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return " ".join(soup.get_text(separator=" ").split())

    def scrape_article(self, url: str) -> Optional[ScrapedArticle]:
        """Scrape a single article URL and return a ScrapedArticle."""
        soup = self.fetch(url)
        if not soup:
            return None

        # Try to find the title
        title = ""
        for selector in ["h1", "title", "meta[property='og:title']"]:
            tag = soup.find(selector)
            if tag:
                title = tag.get("content", "") or tag.get_text(strip=True)
                break

        # Try to find a summary / description
        summary = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            summary = meta_desc.get("content", "")

        # Extract tags from meta keywords
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        tags = []
        if meta_keywords:
            tags = [t.strip() for t in meta_keywords.get("content", "").split(",")]

        return ScrapedArticle(title=title, url=url, summary=summary, tags=tags)

    def scrape_multiple(self, urls: list) -> list:
        """Scrape multiple URLs and return a list of ScrapedArticle objects."""
        results = []
        for url in urls:
            article = self.scrape_article(url)
            if article:
                results.append(article)
        return results

    def save_results(self, results: list, filepath: str):
        """Save scraping results to a JSON file."""
        data = [r.to_dict() if hasattr(r, "to_dict") else r for r in results]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(data)} results to {filepath}")


def demo():
    """Demonstrate the scraper (uses publicly available test pages)."""
    scraper = WebScraper(delay=0.5)

    # Demo URLs (these may not all be available)
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
    ]

    print("=" * 50)
    print("  🕷️  WEB SCRAPER DEMO")
    print("=" * 50)

    if not DEPS_AVAILABLE:
        print("\nInstall dependencies first:")
        print("  pip install requests beautifulsoup4")
        return

    for url in test_urls:
        soup = scraper.fetch(url)
        if soup:
            title = soup.title.string if soup.title else "No title"
            text_preview = scraper.extract_text(soup)[:100]
            print(f"\n  URL: {url}")
            print(f"  Title: {title}")
            print(f"  Preview: {text_preview}...")


if __name__ == "__main__":
    demo()
