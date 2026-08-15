# --- DNK-MRH-HEADER ---
# mrh_id: "fixture_network_probe_plugin"
# purpose: "Hostile fixture attempting outbound network connection in network:none sandbox"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import socket
from core.plugins.plugin_base import Plugin

class NetworkProbePlugin(Plugin):
    @property
    def name(self) -> str:
        return "network_probe"

    def probe_outbound(self) -> bool:
        try:
            s = socket.create_connection(("1.1.1.1", 53), timeout=2)
            s.close()
            return True
        except Exception:
            return False
