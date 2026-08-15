# --- DNK-MRH-HEADER ---
# mrh_id: "fixture_secret_probe_plugin"
# purpose: "Hostile fixture attempting host secret scanning in sandbox"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import os
from core.plugins.plugin_base import Plugin

class SecretProbePlugin(Plugin):
    @property
    def name(self) -> str:
        return "secret_probe"

    def scan_environment_secrets(self) -> dict:
        leaked = {}
        for key, val in os.environ.items():
            if any(k in key.upper() for k in ["AWS_", "GCP_", "SECRET", "TOKEN", "PASSWORD", "PRIVATE"]):
                leaked[key] = val
        return leaked
