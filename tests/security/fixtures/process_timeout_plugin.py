# --- DNK-MRH-HEADER ---
# mrh_id: "fixture_process_timeout_plugin"
# purpose: "Hostile fixture sleeping past process timeout limit"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import time
from core.plugins.plugin_base import Plugin

class ProcessTimeoutPlugin(Plugin):
    @property
    def name(self) -> str:
        return "process_timeout"

    def execute_long_task(self) -> None:
        time.sleep(300)
