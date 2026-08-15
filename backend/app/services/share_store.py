import uuid
from app.schemas.analytics import AnalyticsResponse

# Same in-memory-only limitation as job_store — lost on restart.
# Consistent with the PoC's "no real persistence" scope for now.
_shared_analytics: dict[str, AnalyticsResponse] = {}


def create_share(result: AnalyticsResponse) -> str:
    share_id = str(uuid.uuid4())
    _shared_analytics[share_id] = result
    return share_id


def get_shared_analytics(share_id: str) -> AnalyticsResponse | None:
    return _shared_analytics.get(share_id)