# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_trust_registry"
# purpose: "Ed25519 signature verification & trusted public key registry for Agent Plugins"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import base64
import hashlib
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Any
from cryptography.hazmat.primitives.asymmetric import ed25519

class KeyStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    COMPROMISED = "compromised"

@dataclass
class TrustedKey:
    key_id: str
    algorithm: str
    publisher: str
    public_key_b64: str
    status: KeyStatus
    valid_from: str
    valid_until: Optional[str] = None
    revoked_at: Optional[str] = None

    @property
    def fingerprint(self) -> str:
        pub_bytes = base64.b64decode(self.public_key_b64)
        return hashlib.sha256(pub_bytes).hexdigest()

    def get_public_key_obj(self) -> ed25519.Ed25519PublicKey:
        pub_bytes = base64.b64decode(self.public_key_b64)
        return ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)

class TrustRegistry:
    def __init__(self):
        self.keys: Dict[str, TrustedKey] = {}

    def register_key(self, key: TrustedKey) -> None:
        self.keys[key.key_id] = key

    def revoke_key(self, key_id: str, reason: str = "Revoked by admin") -> bool:
        if key_id in self.keys:
            self.keys[key_id].status = KeyStatus.REVOKED
            self.keys[key_id].revoked_at = "2026-08-15T00:00:00Z"
            return True
        return False

    def get_key(self, key_id: str) -> Optional[TrustedKey]:
        return self.keys.get(key_id)

    def verify_signature(self, key_id: str, message_bytes: bytes, signature_b64: str) -> bool:
        key = self.get_key(key_id)
        if not key or key.status != KeyStatus.ACTIVE:
            return False

        try:
            sig_bytes = base64.b64decode(signature_b64)
            pub_key = key.get_public_key_obj()
            pub_key.verify(sig_bytes, message_bytes)
            return True
        except Exception:
            return False
