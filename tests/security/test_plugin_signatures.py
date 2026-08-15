# --- DNK-MRH-HEADER ---
# mrh_id: "test_plugin_signatures"
# purpose: "Ed25519 signature generation and verification tests (DNK-TRUST-016)"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import os
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
from core.plugins.trust_engine import PluginTrustPolicyEngine, PluginTrustState


def test_valid_ed25519_signature_passes(tmp_path):
    # Ephemeral test key pair (never persisted)
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    pub_b64 = base64.b64encode(pub_key.public_bytes_raw()).decode("utf-8")

    reg = TrustRegistry()
    key_entry = TrustedKey(
        key_id="test-key-01",
        algorithm="Ed25519",
        publisher="DNK Test Publisher",
        public_key_b64=pub_b64,
        status=KeyStatus.ACTIVE,
        valid_from="2026-08-15T00:00:00Z"
    )
    reg.register_key(key_entry)

    pkg_dir = tmp_path / "signed_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('signed')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    sig_bytes = priv_key.sign(hash_res["value"].encode("utf-8"))
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    engine = PluginTrustPolicyEngine(reg, is_production=True)
    eval_res = engine.evaluate_package(
        package_dir=str(pkg_dir),
        expected_hash=hash_res["value"],
        signature_b64=sig_b64,
        key_id="test-key-01"
    )

    assert eval_res["status"] == PluginTrustState.TRUSTED
    assert eval_res["fingerprint"] == key_entry.fingerprint


def test_wrong_public_key_fails(tmp_path):
    priv_key1 = ed25519.Ed25519PrivateKey.generate()
    priv_key2 = ed25519.Ed25519PrivateKey.generate()
    pub_key2 = priv_key2.public_key()
    pub_b64_2 = base64.b64encode(pub_key2.public_bytes_raw()).decode("utf-8")

    reg = TrustRegistry()
    reg.register_key(TrustedKey(
        key_id="key-02", algorithm="Ed25519", publisher="Test", public_key_b64=pub_b64_2, status=KeyStatus.ACTIVE, valid_from="2026"
    ))

    pkg_dir = tmp_path / "signed_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('test')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    # Signed by key1, but registered with key2
    sig_bytes = priv_key1.sign(hash_res["value"].encode("utf-8"))
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    engine = PluginTrustPolicyEngine(reg, is_production=True)
    eval_res = engine.evaluate_package(
        package_dir=str(pkg_dir),
        expected_hash=hash_res["value"],
        signature_b64=sig_b64,
        key_id="key-02"
    )

    assert eval_res["status"] == PluginTrustState.REJECTED
    assert "Invalid signature" in eval_res["reason"]


def test_unsigned_plugin_blocked_in_production(tmp_path):
    reg = TrustRegistry()
    pkg_dir = tmp_path / "unsigned_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_text("print('unsigned')")

    hash_res = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    engine = PluginTrustPolicyEngine(reg, is_production=True)

    eval_res = engine.evaluate_package(
        package_dir=str(pkg_dir),
        expected_hash=hash_res["value"],
        signature_b64=None,
        key_id=None
    )

    assert eval_res["status"] == PluginTrustState.REJECTED
    assert "Unsigned plugin blocked in production" in eval_res["reason"]


def test_no_private_keys_in_repo():
    # Verify no private key files exist in tests or core
    for root, dirs, files in os.walk(str(ROOT)):
        if ".git" in root or ".venv" in root:
            continue
        for f in files:
            assert not f.endswith(".pem")
            assert not f.endswith(".key")
            assert "private_key" not in f
