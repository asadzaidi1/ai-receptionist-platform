"""Provider-neutral contract for a future calling vendor. No network implementation is included."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ProviderRequest:
    provider_idempotency_key: str
    lead_id: str
    campaign_id: str
    brain_version: str
    script_version: str
    policy_version: str

@dataclass(frozen=True)
class ProviderResponse:
    provider_idempotency_key: str
    provider_call_id: str
    status: str

class CallingProvider(Protocol):
    name: str
    def create_call(self, request: ProviderRequest) -> ProviderResponse:
        """Create exactly one provider call using the supplied idempotency key."""
        ...

class NoLiveProvider:
    name = 'no-live-provider'
    def create_call(self, request: ProviderRequest) -> ProviderResponse:
        raise RuntimeError('No calling provider configured; Phase 2 is staging-only')
