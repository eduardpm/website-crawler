import difflib
import re


def extract_info_known_sources(
    text: str, known_product_list: list[str], cutoff: float = 0.8
) -> str | None:
    """
    Extracts the most likely name from the input string using regex and fuzzy matching.
    """
    text_lower = text.lower()

    # Step 1: Check for exact brand matches using regex
    for brand in known_product_list:
        # Regex to match brand name, possibly followed by numbers or letters
        pattern = r"(?i)" + re.escape(brand) + r"\S*"
        if re.search(pattern, text_lower):
            return brand  # return the exact brand found via regex match

    # Step 2: Fuzzy matching as fallback
    close_matches = difflib.get_close_matches(
        text, known_product_list, n=1, cutoff=cutoff
    )
    return close_matches[0] if close_matches else None


def extract_info(text: str, pattern: re.Pattern) -> re.Match | None:
    """
    Extracts the first occurrence of a pattern from the input string using regex.
    """
    return re.search(pattern, text)
