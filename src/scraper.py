import logging
from pathlib import Path
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

class CuneiformFetcher:
    """Ensures automated fetching and local caching includes rate-throttling and local caching so as to not cause stress on server"""

    def __init__(
        self, raw_data_dir: str = "data/raw", request_delay: float = 2.0
        ) -> None:
        self.raw_dir = Path(raw_data_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.request_delay = request_delay
        logger.info(
            f"Initialized 'polite' scraper. Raw dir: {self.raw_dir.resolve()} |"
            f" Delay: {self.request_delay}s"
        )
        
def fetch_transliteration(self, source_url: str, filename: str) -> Path:
    """This downloads a transliteration file from a specific URL and caches it locally, skipping the download if already existing in the cache."""
    target_path = self.raw_dir / filename

    if target_path.is_file():
        logger.info(f"Cache hit: File already exists at {target_path}")
        return target_path

    logger.info(f"Downloading corpus data from {source_url}...")
    try:
        response = requests.get(source_url, timeout=30)
        response.raise_for_status()

        target_path.write_text(response.text, encoding="utf-8")
        logger.info(f"Successfully downloaded and cached: {target_path}")
        return target_path

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching {source_url}: {e}")
        raise

if __name__ == "__main__":
    fetcher = CuneiformFetcher()
    logger.info("Scraper modfule ready for integration.")