from pathlib import Path

from app.parsers.base import get_file_category, ParsedResult, UnsupportedFileTypeError
from app.parsers.document_parser import parse_document
from app.parsers.table_parser import parse_table
from app.parsers.structured_parser import parse_json


def parse_any(filepath: Path) -> ParsedResult:
    """
    Single entry point for ingestion: given any supported file,
    detects its category and dispatches to the right parser,
    returning a ParsedDocument, ParsedTable, or ParsedStructured.
    """
    category = get_file_category(filepath.name)  # raises UnsupportedFileTypeError if unknown

    dispatch = {
        "document": parse_document,
        "table": parse_table,
        "structured": parse_json,
    }

    return dispatch[category](filepath)