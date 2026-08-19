# AgentDesk

An agentic AI-powered toolkit that ingests documents and spreadsheets, then runs selectable AI-driven transformations to generate structured outputs — UAT test specifications, data analytics reports, and more to come.

## What it does

Upload a file, pick a function, get a result:

- **SRS Document → UAT Test Spec** — upload a Software Requirements Specification (PDF, Word, PowerPoint, or plain text), and AgentDesk extracts testable requirements and generates a structured set of UAT test cases (steps, expected results, priority), exportable to Excel.
- **CSV/Excel → Data Analytics** — upload tabular data, and AgentDesk computes real statistics (via pandas), then uses AI to generate plain-language insights and chart recommendations, rendered as live charts. Reports can be shared via a read-only link.

## Tech stack

- **Backend:** FastAPI (Python) — async, Pydantic-validated
- **Frontend:** React + Vite, React Router for client-side routing
- **AI:** Anthropic Claude (primary), OpenAI (automatic fallback) — both accessed via tool-calling (forced structured output), not free-text prompting
- **Data:** pandas, openpyxl, python-docx, python-pptx, pdfplumber for parsing; recharts for chart rendering

## Supported file formats

| Category | Formats |
|---|---|
| Document | `.pdf` (text-based only, no OCR), `.docx`, `.pptx`, `.txt` |
| Table | `.csv`, `.xlsx`, `.xls` |
| Structured | `.json` |

## Project structure

```
AgentDesk/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI entrypoint, router mounting, CORS
│       ├── config.py                # API keys, model config
│       ├── routers/                 # HTTP endpoints
│       │   ├── ingest.py            # file upload
│       │   └── functions/           # one router per AI function
│       ├── parsers/                 # file → ParsedDocument/ParsedTable/ParsedStructured
│       ├── schemas/                 # Pydantic models (request/response contracts)
│       ├── functions/               # AI generation logic per function
│       └── services/
│           ├── ai_client.py         # provider-agnostic Claude/OpenAI wrapper (text + tool calls)
│           ├── file_storage.py      # temp file handling
│           ├── job_store.py         # in-memory upload-session tracking
│           └── share_store.py       # in-memory shareable-link storage
│
└── frontend/
    └── src/
        ├── App.jsx                  # route definitions
        ├── MainApp.jsx               # main upload/generate workflow
        ├── pages/                    # standalone routed pages (e.g. shared report view)
        ├── components/                # UploadZone, FilePreviewCard, results views, etc.
        └── api/client.js              # fetch wrappers to the backend
```

## Architecture notes

- **Ingestion is decoupled from function logic.** Every file is parsed into one of three shapes (`ParsedDocument`, `ParsedTable`, `ParsedStructured`) regardless of which function will use it — functions never touch raw files or format-specific parsing.
- **AI calls always go through `ai_client.py`.** Structured outputs are enforced via forced tool-calling (not prompt-based JSON), which is more reliable and mirrors how real agentic tool use works. Anthropic is tried first; if it fails (e.g. rate limit, insufficient credit), the same request silently falls back to OpenAI.
- **Deterministic computation before AI reasoning, where possible.** Analytics doesn't hand raw rows to the AI — pandas computes real statistics first, and the AI reasons over those (accurate arithmetic, AI judgment where it adds value — not the reverse).

## Setup

### Prerequisites
- Python 3.10+
- Node.js + npm

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```
At least one key is required; both enables automatic fallback.

Run:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`.

## Current scope / known limitations

This is a proof of concept, with a few deliberate simplifications:

- **No user accounts or auth** — single-session use
- **No file persistence** — uploaded files are temporary, cleaned up after use; nothing survives a backend restart
- **Shareable links are in-memory only** — they stop working if the backend restarts
- **No multi-file runs** — each function operates on one uploaded file at a time
- **PDF support is text-based only** — scanned/image PDFs (no text layer) aren't supported
- **Excel multi-sheet files** — only the first sheet is read

## Roadmap

- Additional functions (document reconciliation, multi-doc synthesis, consistency checking)
- Analytics export (Excel/PDF report)
- Real persistence (database + object storage) and user accounts
- Agentic file-fetching (local folder access, cloud drive connectors)