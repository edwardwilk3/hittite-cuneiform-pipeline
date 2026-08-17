from pathlib import Path
import sys

# Ensure project root is in path for runtime execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.scraper import CuneiformFetcher, fetch_transliteration


def test_scraper_caching_and_init():
  print("Running scraper test...")

  # Initialize the fetcher instance
  fetcher = CuneiformFetcher(raw_data_dir="data/test_raw", request_delay=1.0)

  # Verify directory was successfully created
  assert fetcher.raw_dir.exists(), "Raw directory was not created!"
  print(f"[PASS] Directory verified at: {fetcher.raw_dir.resolve()}")

  # Define public test sample URL and target filename
  test_url = (
      "https://raw.githubusercontent.com/octocat/Hello-World/master/README"
  )
  test_filename = "test_corpus.txt"

  # First fetch (should perform a network download and cache the file)
  file_path = fetch_transliteration(fetcher, test_url, test_filename)
  assert file_path.is_file(), "Downloaded file does not exist!"
  print(f"[PASS] Successfully fetched and cached file at: {file_path}")

  # Second fetch (should trigger a cache hit and return the existing path)
  cached_path = fetch_transliteration(fetcher, test_url, test_filename)
  assert cached_path == file_path, "Cache path mismatch!"
  print("[PASS] Cache hit verified successfully.")

  print("All scraper tests passed!")


if __name__ == "__main__":
  test_scraper_caching_and_init()