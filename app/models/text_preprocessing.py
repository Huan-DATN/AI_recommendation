import unicodedata
import re

def normalize_unicode(text):
    """
    Normalize Unicode characters to ensure consistency in text data.

    Args:
        text (str): Input text to normalize

    Returns:
        str: Normalized text
    """
    if not isinstance(text, str):
        return ""

    # Normalize to NFKC form (compatible composition)
    # This converts characters like ｆｕｌｌ-ｗｉｄｔｈ to full-width
    # and also handles accented characters, etc.
    normalized_text = unicodedata.normalize('NFKC', text)
    return normalized_text

def to_lowercase(text):
    """
    Convert text to lowercase for processing.

    Args:
        text (str): Input text to convert

    Returns:
        str: Lowercase text
    """
    if not isinstance(text, str):
        return ""

    return text.lower()

def preprocess_text(text):
    """
    Apply full text preprocessing pipeline:
    1. Unicode normalization
    2. Lowercase conversion

    Args:
        text (str): Raw input text

    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str):
        return ""

    # Apply preprocessing steps in sequence
    processed_text = text
    processed_text = normalize_unicode(processed_text)
    processed_text = to_lowercase(processed_text)

    return processed_text
