import requests
from bs4 import BeautifulSoup

from app.schemas.parsed import ParsedDocument, ParsedStructured

MAX_CONTENT_BYTES = 5 * 1024 * 1024
REQUEST_TIMEOUT_SECONDS = 15


def fetch_url_content(url: str) -> tuple[str, bytes]:
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            headers={"User-Agent": "AgentDesk/1.0"},
        )
    except requests.RequestException as e:
        raise ValueError(f"Could not reach '{url}': {e}")

    if response.status_code != 200:
        raise ValueError(f"'{url}' returned HTTP {response.status_code}")

    if len(response.content) > MAX_CONTENT_BYTES:
        raise ValueError(f"Response from '{url}' exceeds the {MAX_CONTENT_BYTES // (1024*1024)}MB size limit")

    content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
    return content_type, response.content


def parse_url_to_document(url: str, html_bytes: bytes) -> ParsedDocument:
    soup = BeautifulSoup(html_bytes, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    if not text.strip():
        raise ValueError(f"No readable text content found at '{url}'")

    return ParsedDocument(
        filename=url,
        file_type="txt",
        text=text,
        word_count=len(text.split()),
    )


def parse_url_to_structured(url: str, json_bytes: bytes) -> ParsedStructured:
    import json as json_lib
    try:
        data = json_lib.loads(json_bytes)
    except json_lib.JSONDecodeError as e:
        raise ValueError(f"'{url}' claimed to be JSON but failed to parse: {e}")

    top_level_keys = list(data.keys()) if isinstance(data, dict) else []
    item_count = len(data) if isinstance(data, list) else None

    return ParsedStructured(
        filename=url,
        file_type="json",
        data=data,
        top_level_keys=top_level_keys,
        item_count=item_count,
    )


def parse_url(url: str) -> tuple[str, "ParsedDocument | ParsedStructured"]:
    content_type, raw_bytes = fetch_url_content(url)

    if "json" in content_type:
        return "structured", parse_url_to_structured(url, raw_bytes)
    elif "html" in content_type:
        return "document", parse_url_to_document(url, raw_bytes)
    else:
        try:
            text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            raise ValueError(f"Unrecognized content type '{content_type}' at '{url}'")
        return "document", ParsedDocument(filename=url, file_type="txt", text=text, word_count=len(text.split()))