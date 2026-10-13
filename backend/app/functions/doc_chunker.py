"""
Splits long document text into chunks small enough for one AI call each.

Why chunk at all? A single AI call has two limits: how much it can read
(context window) and how much it can write (max_tokens). For UAT generation
the *output* limit bites first: a long SRS produces more test cases than fit
in one response. Splitting the input keeps each response small.

Why split on headings? A requirement and its details usually live under one
heading. Cutting there keeps related text together, so the model doesn't see
half a requirement in one chunk and the other half in the next.
"""
import re

# Numbered headings as they appear in PDFs/txt SRS documents, e.g.
# "3 Functional Requirements", "3.2 User Login", "4.1.3. Password Reset".
# Kept deliberately strict (short line, starts with a section number) so
# ordinary sentences like "2 users can log in at once" are rarely matched.
_NUMBERED_HEADING = re.compile(r"^\s*\d+(\.\d+)*\.?\s+[A-Z][^\n]{0,80}$")


def _is_heading(line: str, known_headings: set[str]) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped in known_headings:          # docx: real Word heading styles
        return True
    return bool(_NUMBERED_HEADING.match(stripped))  # pdf/txt: numbering heuristic


def _split_into_blocks(text: str, headings: list[str]) -> list[str]:
    """Groups lines into blocks, each starting at a heading."""
    known = {h.strip() for h in headings if h.strip()}
    blocks, current = [], []
    for line in text.splitlines():
        if _is_heading(line, known) and current:
            blocks.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _hard_split(block: str, max_chars: int) -> list[str]:
    """Splits an oversized block on line boundaries (or mid-line as a last resort)."""
    pieces, current, size = [], [], 0
    for line in block.splitlines():
        # A single gigantic line (e.g. a PDF with no line breaks) gets sliced.
        while len(line) > max_chars:
            if current:
                pieces.append("\n".join(current)); current, size = [], 0
            pieces.append(line[:max_chars]); line = line[max_chars:]
        if size + len(line) + 1 > max_chars and current:
            pieces.append("\n".join(current)); current, size = [], 0
        current.append(line); size += len(line) + 1
    if current:
        pieces.append("\n".join(current))
    return pieces


def chunk_document(text: str, headings: list[str], max_chars: int) -> list[str]:
    """
    Returns the document as a list of chunks, each at most max_chars long.
    Short documents come back as a single chunk, unchanged.
    """
    if len(text) <= max_chars:
        return [text]

    # Greedy packing: keep adding whole sections to the current chunk until
    # the next one would overflow it, then start a new chunk.
    chunks, current, size = [], [], 0
    for block in _split_into_blocks(text, headings):
        parts = [block] if len(block) <= max_chars else _hard_split(block, max_chars)
        for part in parts:
            if size + len(part) + 1 > max_chars and current:
                chunks.append("\n".join(current)); current, size = [], 0
            current.append(part); size += len(part) + 1
    if current:
        chunks.append("\n".join(current))
    return [c for c in chunks if c.strip()]


def split_in_half(text: str) -> tuple[str, str]:
    """Splits text roughly in half at the nearest line break (used on retry)."""
    mid = len(text) // 2
    cut = text.rfind("\n", 0, mid)
    if cut <= 0:
        cut = text.find("\n", mid)
    if cut <= 0:
        cut = mid
    return text[:cut], text[cut:]
