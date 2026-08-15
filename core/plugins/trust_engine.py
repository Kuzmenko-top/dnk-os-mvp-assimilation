# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_trust_engine"
# purpose: "Plugin Trust State Machine, Policy Engine, and Quarantine Integration"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

from enum import Enum
from typing import Dict, Optional, Any
from core.plugins.trust_registry import TrustRegistry, KeyStatus
from core.plugins.provenance import CanonicalPackageHasher

class PluginTrustState(Enum):
    UNVERIFIED = "unverified"
    HASH_VERIFIED = "hash_verified"
    SIGNATURE_VERIFIED = "signature_verified"
    TRUSTED = "trusted"
    REJECTED = "rejected"
    REVOKED = "revoked"
    QUARANTINED = "quarantined"

class PluginTrustTransitionError(Exception):
    def __init__(self, message: str = "409 INVALID_PLUGIN_TRUST_TRANSITION"):
        super().__init__(message)
        self.code = 409

# Graph of allowed transitions
ALLOWED_TRANSITIONS = {
    PluginTrustState.UNVERIFIED: {PluginTrustState.HASH_VERIFIED, PluginTrustState.REJECTED},
    PluginTrustState.HASH_VERIFIED: {PluginTrustState.SIGNATURE_VERIFIED, PluginTrustState.REJECTED},
    PluginTrustState.SIGNATURE_VERIFIED: {PluginTrustState.TRUSTED, PluginTrustState.REJECTED},
    PluginTrustState.TRUSTED: {PluginTrustState.REVOKED},
    PluginTrustState.REJECTED: {PluginTrustState.QUARANTINED},
    PluginTrustState.REVOKED: {PluginTrustState.QUARANTINED},
    PluginTrustState.QUARANTINED: set(),
}

class PluginTrustStateMachine:
    def __init__(self, initial_state: PluginTrustState = PluginTrustState.UNVERIFIED):
        self._state = initial_state

    @property
    def state(self) -> PluginTrustState:
        return self._state

    def transition_to(self, new_state: PluginTrustState) -> PluginTrustState:
        if new_state not in ALLOWED_TRANSITIONS.get(self._state, set()):
            raise PluginTrustTransitionError(f"409 INVALID_PLUGIN_TRUST_TRANSITION: Cannot transition from {self._state.value} to {new_state.value}")
        self._state = new_state
        return self._state

class PluginTrustPolicyEngine:
    def __init__(self, registry: TrustRegistry, is_production: bool = True):
        self.registry = registry
        self.is_production = is_production

    def evaluate_package(
        self,
        package_dir: str,
        expected_hash: str,
        signature_b64: Optional[str] = None,
        key_id: Optional[str] = None
    ) -> Dict[str, Any]:
        sm = PluginTrustStateMachine()

        # 1. Verify Package Hash
        calc_res = CanonicalPackageHasher.calculate_package_hash(package_dir)
        if calc_res["value"] != expected_hash:
            sm.transition_to(PluginTrustState.REJECTED)
            return {"status": sm.state, "reason": "Hash mismatch: package tampered"}

        sm.transition_to(PluginTrustState.HASH_VERIFIED)

        # 2. Verify Signature
        if not signature_b64 or not key_id:
            if self.is_production:
                sm.transition_to(PluginTrustState.REJECTED)
                return {"status": sm.state, "reason": "Unsigned plugin blocked in production"}
            else:
                return {"status": sm.state, "reason": "Hash verified, missing signature"}

        key = self.registry.get_key(key_id)
        if not key:
            sm.transition_to(PluginTrustState.REJECTED)
            return {"status": sm.state, "reason": "Unknown key_id"}

        if key.status == KeyStatus.REVOKED:
            sm.transition_to(PluginTrustState.REJECTED)
            sm.transition_to(PluginTrustState.QUARANTINED)
            return {"status": sm.state, "reason": "Revoked key: plugin quarantined"}

        if key.status == KeyStatus.EXPIRED:
            sm.transition_to(PluginTrustState.REJECTED)
            return {"status": sm.state, "reason": "Expired key"}

        sig_valid = self.registry.verify_signature(
            message_bytes=calc_res["value"].encode("utf-8"),
            signature_b64=signature_b64,
            key_id=key_id
        )

        if not sig_valid:
            sm.transition_to(PluginTrustState.REJECTED)
            return {"status": sm.state, "reason": "Invalid signature"}

        sm.transition_to(PluginTrustState.SIGNATURE_VERIFIED)
        sm.transition_to(PluginTrustState.TRUSTED)

        return {
            "status": sm.state,
            "reason": "Plugin signature and provenance fully trusted",
            "fingerprint": key.fingerprint,
            "hash": calc_res["value"]
        }
