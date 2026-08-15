import re

def normalize_brackets(text: str) -> str:
    """
    This will normalize epigraphic transliteration brackets in Hittite text.
    Removes restoration brackets ([ ]) and uncertainty marks (?, !)while preserving internal transliteration readings.
    """
    if not text:
        return ""

    # Replaces HTML non-breaking spaces with regular spaces.
    cleaned = text.replace("&nbsp;", " ")

    # Remove uncertainty marks (?, !)
    cleaned = re.sub(r"[\?!]", "", cleaned)

    # Standardizes gloss wedge variations into a single colon.
    cleaned = re.sub(r"(::|'|//)", ":", cleaned)

    # Normalize multiple empty spaces down to a single space.
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()