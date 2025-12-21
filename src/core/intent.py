from dataclasses import dataclass
from typing import Dict, Any, Optional, Literal

IntentSource = Literal["ai", "ui", "api"]


@dataclass(frozen=True)
class Intent:
    action: str
    params: Dict[str, Any]
    source: IntentSource

    # AI signals (non-authoritative)
    confidence: Optional[float] = None
    requires_confirmation: Optional[bool] = None
