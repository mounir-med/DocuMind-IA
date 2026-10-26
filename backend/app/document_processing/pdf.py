from dataclasses import dataclass
import re
import unicodedata

import fitz

from app.core.exceptions import ValidationAppError
from app.core.security import is_pdf_header


_L = r"[A-Za-zÀ-ÿ]"
# Certains PDF (exports Keynote/PowerPoint) ont une table Unicode erronée : les
# ligatures "ti", "tt", "ft" sont extraites sous forme de "=", "$", "1", "E", "R"...
_SUSPECT = re.compile(rf"(?<={_L})[=$](?={_L})|(?<=[a-zé])[ER](?=[a-zéèê])")


def repair_text(text: str) -> str:
    """Répare les ligatures mal encodées (Introduc=on -> Introduction)."""
    t = unicodedata.normalize("NFKC", text)  # ﬁ -> fi, ﬂ -> fl
    t = re.sub(rf"(?<={_L})==(?={_L})", "titi", t)           # répé==on -> répétition
    t = re.sub(rf"(?<={_L})[=$1](?={_L})", "ti", t)          # Introduc=on, posi1on
    t = re.sub(rf"(?<={_L}{{2}})[=$](?=\W|$)", "ti", t)      # répéti= -> répétition
    t = re.sub(r"(?<!\w)[=$](?=tre\b)", "ti", t)             # =tre -> titre
    t = re.sub(r"(?<=[a-zé])[ER](?=[a-zéèê])", "tt", t)      # aEribut, boRom
    t = re.sub(r"\b([Aa])[ER](?=[a-zé])", r"\1tt", t)        # AEribut
    t = re.sub(r"\blew\b|\blei\b", "left", t)               # lew|center -> left|center
    t = re.sub(r"^[!\u2022▪■]\s+", "", t, flags=re.MULTILINE)  # puces mal décodées
    return t


def looks_corrupted(text: str) -> bool:
    """Heuristique : beaucoup de '=' / '$' au milieu de mots => encodage douteux."""
    words = max(len(text.split()), 1)
    return len(_SUSPECT.findall(text)) / words > 0.01


@dataclass
class PageText:
    page_number: int
    text: str


@dataclass
class ExtractionResult:
    pages: list[PageText]
    page_count: int
    char_count: int
    likely_scanned: bool


def extract_pdf(payload: bytes) -> ExtractionResult:
    if not payload or not is_pdf_header(payload):
        raise ValidationAppError("Le fichier n'est pas un PDF valide.")
    try:
        document = fitz.open(stream=payload, filetype="pdf")
    except Exception as exc:  # noqa: BLE001
        raise ValidationAppError("PDF corrompu ou illisible.") from exc

    pages: list[PageText] = []
    try:
        if document.is_encrypted:
            raise ValidationAppError("Les PDF protégés par mot de passe ne sont pas pris en charge.")
        for index, page in enumerate(document, start=1):
            text = repair_text(page.get_text("text") or "")
            pages.append(PageText(page_number=index, text=text))
        page_count = document.page_count
    finally:
        document.close()

    char_count = sum(len(page.text.strip()) for page in pages)
    non_empty = sum(1 for page in pages if len(page.text.strip()) > 20)
    likely_scanned = page_count > 0 and char_count < 80 and non_empty == 0
    return ExtractionResult(
        pages=pages,
        page_count=page_count,
        char_count=char_count,
        likely_scanned=likely_scanned,
    )
