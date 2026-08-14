from pathlib import Path
from app.schemas.parsed import ParsedDocument, ParsedTable, ParsedStructured

ParsedResult = ParsedDocument | ParsedTable | ParsedStructured

SUPPORTED_EXTENSIONS = {
    ".pdf": "document",
    ".docx": "document",
    ".pptx": "document",
    ".txt": "document",
    ".csv": "table",
    ".xlsx": "table",
    ".xls": "table",
    ".json": "structured",
}


class UnsupportedFileTypeError(Exception):
    """Raised when a file extension isn't in SUPPORTED_EXTENSIONS."""


def get_file_category(filename: str) -> str:
    """Returns 'document', 'table', or 'structured' based on extension."""
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"'{ext}' is not a supported file type")
    return SUPPORTED_EXTENSIONS[ext]