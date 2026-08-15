# --- DNK-MRH-HEADER ---
# mrh_id: "test_plugin_provenance"
# purpose: "Canonical SHA-256 package hashing & provenance tests (DNK-TRUST-016)"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import os
import sys
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.provenance import CanonicalPackageHasher


def test_valid_package_hash_passes(tmp_path):
    pkg_dir = tmp_path / "sample_plugin"
    pkg_dir.mkdir()
    (pkg_dir / "plugin.py").write_bytes(b"print('hello')\n")
    (pkg_dir / "plugin.json").write_bytes(b"{\"name\": \"sample\"}\n")

    res1 = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))
    res2 = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))

    assert res1["algorithm"] == "sha256"
    assert res1["value"] == res2["value"]
    assert res1["file_count"] == 2


def test_modified_package_fails_hash(tmp_path):
    pkg_dir = tmp_path / "sample_plugin"
    pkg_dir.mkdir()
    f1 = pkg_dir / "plugin.py"
    f1.write_bytes(b"original_content\n")

    res1 = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))

    # Tamper file
    f1.write_bytes(b"tampered_content\n")
    res2 = CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))

    assert res1["value"] != res2["value"]


def test_symlink_rejection(tmp_path):
    pkg_dir = tmp_path / "symlink_plugin"
    pkg_dir.mkdir()
    target_file = tmp_path / "outside.txt"
    target_file.write_text("outside")

    symlink_file = pkg_dir / "link.py"
    os.symlink(str(target_file), str(symlink_file))

    with pytest.raises(ValueError, match="Symlinks strictly forbidden"):
        CanonicalPackageHasher.calculate_package_hash(str(pkg_dir))


def test_canonicalization_line_ending_normalization(tmp_path):
    pkg1 = tmp_path / "pkg1"
    pkg2 = tmp_path / "pkg2"
    pkg1.mkdir()
    pkg2.mkdir()

    (pkg1 / "file.txt").write_bytes(b"line1\r\nline2\r\n")
    (pkg2 / "file.txt").write_bytes(b"line1\nline2\n")

    h1 = CanonicalPackageHasher.calculate_package_hash(str(pkg1))
    h2 = CanonicalPackageHasher.calculate_package_hash(str(pkg2))

    assert h1["value"] == h2["value"]
