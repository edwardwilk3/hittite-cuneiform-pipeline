import re

def normalize_brackets(text: str) -> str:
    """
    This will normalize epigraphic transliteration brackets in Hittite text.
    Removes restoration brackets while preserving internal transliteration readings.
    """
    if not text:
        return ""

    # Remove square restoration brackets []
    cleaned = re.sub(r"[\[\]]", "", text)

    # Normalize multiple whitespace spaces down to a single space.
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()
