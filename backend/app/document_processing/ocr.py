"""Point d'extension OCR (Tesseract ou autre).

Cette version n'exécute aucun OCR. Les PDF scannés sont signalés comme tels
au lieu d'inventer du texte.
"""


def ocr_available() -> bool:
    return False


def ocr_page_image(_image_bytes: bytes) -> str:
    raise RuntimeError("OCR optionnel non activé. Installez Tesseract et branchez ce module pour l'activer.")
