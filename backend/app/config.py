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
# ~4 chars per token, so 300k chars is roughly 75k tokens. UAT generation
# chunks the document, but Summary still sends it in one call, so this must
# stay inside GPT-4o's 128k-token window (the fallback) with room to spare.
MAX_DOCUMENT_CHARS = 300_000

# UAT chunking. Each chunk (~5k tokens of SRS text) gets its own AI call.
# Smaller chunks = fewer test cases per answer = less risk of truncation,
# but more calls. 300k chars / 20k = at most 15 parts.
UAT_CHUNK_CHARS = 20_000
# Parallel AI calls. Higher is faster but more likely to hit provider rate limits.
UAT_MAX_PARALLEL = 4
# Output budget per call. Kept under ~21k: above that the Anthropic SDK
# refuses non-streaming requests (it expects them to run too long).
UAT_MAX_TOKENS_PER_CALL = 12_000