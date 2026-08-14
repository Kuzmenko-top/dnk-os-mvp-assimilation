# --- DNK-MRH-HEADER ---
# mrh_id: "fixture_memory_limit_plugin"
# purpose: "Hostile fixture attempting memory allocation past cgroups limit"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

from core.plugins.plugin_base import Plugin

class MemoryLimitPlugin(Plugin):
    @property
    def name(self) -> str:
        return "memory_limit"

    def allocate_memory(self) -> None:
        # Attempt allocating 256MB bytearray (exceeds 128MB limit)
        _ = bytearray(256 * 1024 * 1024)
