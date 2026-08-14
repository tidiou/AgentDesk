from typing import Any, Literal
from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    """Represents parsed content from pdf, docx, pptx, or txt files."""

    filename: str
    file_type: Literal["pdf", "docx", "pptx", "txt"]
    text: str                      # full extracted text, concatenated
    page_count: int | None = None  # relevant for pdf/pptx (slides), None for txt/docx
    sections: list[str] = Field(default_factory=list)  # detected headings, if any
    word_count: int


class ParsedTable(BaseModel):
    """Represents parsed content from csv, xlsx, or xls files."""

    filename: str
    file_type: Literal["csv", "xlsx", "xls"]
    columns: list[str]
    row_count: int
    preview_rows: list[dict[str, Any]]  # first N rows, for the preview card
    dtypes: dict[str, str]              # column name -> inferred type (e.g. "int64", "object")


class ParsedStructured(BaseModel):
    """Represents parsed content from json files."""

    filename: str
    file_type: Literal["json"]
    data: Any                    # the raw parsed JSON (dict, list, etc.)
    top_level_keys: list[str] = Field(default_factory=list)  # if data is a dict
    item_count: int | None = None  # if data is a list