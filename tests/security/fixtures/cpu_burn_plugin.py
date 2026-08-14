# --- DNK-MRH-HEADER ---
# mrh_id: "fixture_cpu_burn_plugin"
# purpose: "Hostile fixture attempting CPU burn for sandbox cgroups verification"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import time
from core.plugins.plugin_base import Plugin

class CpuBurnPlugin(Plugin):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "cpuburnplugin"

    def run_burn(self) -> None:
        start = time.time()
        while time.time() - start < 10:
            _ = 2 ** 1000
