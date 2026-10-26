import re

WHITESPACE = re.compile(r"[ \t]+")
MULTINEWLINE = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = WHITESPACE.sub(" ", normalized)
    normalized = MULTINEWLINE.sub("\n\n", normalized)
    return normalized.strip()
