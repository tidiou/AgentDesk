import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not ANTHROPIC_API_KEY and not OPENAI_API_KEY:
    raise RuntimeError(
        "At least one of ANTHROPIC_API_KEY or OPENAI_API_KEY must be set in backend/.env"
    )

CLAUDE_MODEL = "claude-sonnet-4-5"
OPENAI_MODEL = "gpt-4o"  # fallback model

# Max characters of extracted document text accepted at ingestion.
# ~4 chars per token, so 200k chars is roughly 50k tokens: comfortably inside
# both Claude's and GPT-4o's context windows, leaving room for the prompt.
# Tune this if legitimate documents get rejected.
MAX_DOCUMENT_CHARS = 200_000