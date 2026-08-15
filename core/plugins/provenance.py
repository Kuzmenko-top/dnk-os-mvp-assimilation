# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_provenance"
# purpose: "Canonical SHA-256 package hashing & provenance verification for Agent Plugins"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import os
import hashlib
import pathlib
from typing import Dict, Any, List

EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", ".idea", "node_modules"}
EXCLUDED_FILES = {".DS_Store", "package-lock.json", "thumbs.db"}

class CanonicalPackageHasher:
    @staticmethod
    def calculate_file_hash(filepath: str) -> str:
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            content = f.read()
            # Normalize line endings \r\n -> \n
            normalized = content.replace(b"\r\n", b"\n")
            sha.update(normalized)
        return sha.hexdigest()

    @classmethod
    def calculate_package_hash(cls, package_dir: str) -> Dict[str, Any]:
        pkg_path = pathlib.Path(package_dir).resolve()
        if not pkg_path.exists() or not pkg_path.is_dir():
            raise FileNotFoundError(f"Package directory does not exist: {package_dir}")

        records: List[str] = []

        for root, dirs, files in os.walk(str(pkg_path)):
            # Prune excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for f in sorted(files):
                if f in EXCLUDED_FILES or f.endswith(".pyc"):
                    continue

                full_p = os.path.join(root, f)
                
                # Check for symlinks -> reject strictly
                if os.path.islink(full_p):
                    raise ValueError(f"Symlinks strictly forbidden in canonical package hash: {full_p}")

                rel_p = os.path.relpath(full_p, str(pkg_path)).replace("\\", "/")
                file_h = cls.calculate_file_hash(full_p)
                records.append(f"{rel_p}:{file_h}")

        records.sort()
        manifest_body = "\n".join(records).encode("utf-8")
        package_sha = hashlib.sha256(manifest_body).hexdigest()

        return {
            "algorithm": "sha256",
            "value": package_sha,
            "canonicalization_version": "1.0",
            "file_count": len(records)
        }
