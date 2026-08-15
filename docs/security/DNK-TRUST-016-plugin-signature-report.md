# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-TRUST-016-plugin-signature-report"
# purpose: "Security report for DNK-TRUST-016 Plugin Provenance & Ed25519 Signature Verification"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

# Security Report: DNK-TRUST-016 Plugin Provenance & Ed25519 Signature Verification

## 1. Canonical Package Hashing (SHA-256)
- **Canonicalization Rules:**
  - Sorted relative file paths (`/` normalized path separators).
  - Line ending normalization (`\r\n` -> `\n`).
  - Strict exclusion of `.git`, `__pycache__`, `.pytest_cache`, `.DS_Store`, `.venv`.
  - Symlinks strictly rejected (`ValueError("Symlinks strictly forbidden")`).
  - Hash Algorithm: `SHA-256` (`canonicalization_version: "1.0"`).

## 2. Ed25519 Signature Verification
- Implemented using `cryptography.hazmat.primitives.asymmetric.ed25519`.
- Pure public key verification at runtime.
- Private keys NEVER stored or checked into repository/Docker images (verified by secret scan).

## 3. Trust Registry & Key Management (`TrustRegistry`)
- Key model: `key_id`, `algorithm` (`Ed25519`), `publisher`, `public_key_b64`, `status` (`KeyStatus`), `valid_from`, `fingerprint`.
- Statuses: `pending`, `active`, `expired`, `revoked`, `compromised`.
- Key resolution uses cryptographically signed fingerprint matching, never raw publisher string.

## 4. Plugin Trust State Machine (`PluginTrustState`)
- States: `unverified`, `hash_verified`, `signature_verified`, `trusted`, `rejected`, `revoked`, `quarantined`.
- Enforced Transition Graph: Invalid transitions raise `409 INVALID_PLUGIN_TRUST_TRANSITION`.

## 5. Security Policy Matrix
- Valid hash + valid Ed25519 signature + active key -> `TRUSTED`
- Tampered package / hash mismatch -> `REJECTED`
- Unsigned plugin in production -> `REJECTED` / blocked
- Revoked key -> `QUARANTINED`
- Unknown / expired key -> `REJECTED`

## 6. Secrets Scan & Hygiene
- Scanned repository for private key material (`.pem`, `.key`, `BEGIN PRIVATE KEY`): ZERO matches.
