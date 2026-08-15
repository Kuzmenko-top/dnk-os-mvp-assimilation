# --- DNK-MRH-HEADER ---
# mrh_id: "test_plugin_trust_registry"
# purpose: "Trust registry & state machine transitions tests (DNK-TRUST-016)"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import sys
import base64
import pathlib
import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.provenance import CanonicalPackageHasher
from core.plugins.trust_registry import TrustRegistry, TrustedKey, KeyStatus
from core.plugins.trust_engine import (
    PluginTrustStateMachine,
    PluginTrustState,
    PluginTrustTransitionError,
    PluginTrustPolicyEngine
)


def test_trust_state_invalid_transition_raises_409():
    sm = PluginTrustStateMachine(PluginTrustState.UNVERIFIED)
    
    # Direct jump from UNVERIFIED to TRUSTED is forbidden
    with pytest.raises(PluginTrustTransitionError) as exc_info:
        sm.transition_to(PluginTrustState.TRUSTED)

    assert exc_info.value.code == 409
    assert "409 INVALID_PLUGIN_TRUST_TRANSITION" in str(exc_info.value)


def test_revoked_key_quarantines_plugin(tmp_path):
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    pub_b64 = base64.b64encode(pub_key.public_bytes_raw()).decode("utf-8")

    reg = TrustRegistry()
    key_entry = TrustedKey(
        key_id="revoked-key-01",
        algorithm="Ed25519",
        publisher="Compromised Publisher",
        public_key_b64=pub_b64,
        status=KeyStatus.REVOKED,
        valid_from="2026-01-01"
    )
    reg.register_key(key_entry)

    pkg_dir = tmp_path / "revoked_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('revoked')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    sig_bytes = priv_key.sign(hash_res["value"].encode("utf-8"))
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    engine = PluginTrustPolicyEngine(reg, is_production=True)
    eval_res = engine.evaluate_package(
        package_dir=str(pkg_dir),
        expected_hash=hash_res["value"],
        signature_b64=sig_b64,
        key_id="revoked-key-01"
    )

    assert eval_res["status"] == PluginTrustState.QUARANTINED
    assert "Revoked key" in eval_res["reason"]


def test_expired_key_rejected(tmp_path):
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    pub_b64 = base64.b64encode(pub_key.public_bytes_raw()).decode("utf-8")

    reg = TrustRegistry()
    reg.register_key(TrustedKey(
        key_id="expired-key-01",
        algorithm="Ed25519",
        publisher="Expired Publisher",
        public_key_b64=pub_b64,
        status=KeyStatus.EXPIRED,
        valid_from="2020-01-01"
    ))

    pkg_dir = tmp_path / "expired_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('expired')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    sig_bytes = priv_key.sign(hash_res["value"].encode("utf-8"))
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    engine = PluginTrustPolicyEngine(reg, is_production=True)
    eval_res = engine.evaluate_package(
        package_dir=str(pkg_dir),
        expected_hash=hash_res["value"],
        signature_b64=sig_b64,
        key_id="expired-key-01"
    )

    assert eval_res["status"] == PluginTrustState.REJECTED
    assert "Expired key" in eval_res["reason"]


def test_duplicate_verification_is_idempotent(tmp_path):
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    pub_b64 = base64.b64encode(pub_key.public_bytes_raw()).decode("utf-8")

    reg = TrustRegistry()
    reg.register_key(TrustedKey(
        key_id="idemp-key-01", algorithm="Ed25519", publisher="DNK", public_key_b64=pub_b64, status=KeyStatus.ACTIVE, valid_from="2026"
    ))

    pkg_dir = tmp_path / "idemp_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('idemp')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    sig_bytes = priv_key.sign(hash_res["value"].encode("utf-8"))
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    engine = PluginTrustPolicyEngine(reg, is_production=True)
    res1 = engine.evaluate_package(str(pkg_dir), hash_res["value"], sig_b64, "idemp-key-01")
    res2 = engine.evaluate_package(str(pkg_dir), hash_res["value"], sig_b64, "idemp-key-01")

    assert res1 == res2
