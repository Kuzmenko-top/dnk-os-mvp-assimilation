# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_plugin_manager"
# purpose: "Manage registration, manifest validation, lifecycle transitions, quarantine, and tool routing for plugins"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import logging
from typing import Dict, List, Optional, Any
from core.plugins.plugin_base import Plugin, PluginState

logger = logging.getLogger(__name__)

REQUIRED_MANIFEST_FIELDS = ["name", "version", "extension_id", "publisher"]

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.quarantined_plugins: Dict[str, str] = {}

    def validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        if not manifest or not isinstance(manifest, dict):
            return False
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest or not manifest[field]:
                return False
        ext_id = manifest.get("extension_id", "")
        if not ext_id.startswith("com.dnk-os.plugin"):
            return False
        return True

    def validate_mcp_config(self, mcp_config: Dict[str, Any]) -> bool:
        if not mcp_config or not isinstance(mcp_config, dict):
            return False
        mcp_servers = mcp_config.get("mcpServers", {})
        for name, server in mcp_servers.items():
            transport = server.get("transport", "stdio")
            sandboxed = server.get("sandboxed", False)
            if transport == "stdio" and not sandboxed:
                logger.warning(f"MCP server {name} blocked: unsandboxed stdio execution forbidden.")
                return False
        return True

    def register_plugin(self, plugin: Plugin, config: Optional[Dict[str, Any]] = None) -> None:
        if plugin.name in self.quarantined_plugins:
            plugin.quarantine(self.quarantined_plugins[plugin.name])
            logger.warning(f"Plugin {plugin.name} is quarantined and cannot be registered.")
            return

        try:
            plugin.initialize(config)
            plugin.activate()
            self.plugins[plugin.name] = plugin
        except Exception as e:
            plugin._state = PluginState.ERROR
            logger.error(f"Failed to initialize plugin {plugin.name}: {e}")

    def quarantine_plugin(self, plugin_name: str, reason: str) -> None:
        self.quarantined_plugins[plugin_name] = reason
        if plugin_name in self.plugins:
            self.plugins[plugin_name].quarantine(reason)

    def unregister_plugin(self, plugin_name: str) -> None:
        if plugin_name in self.plugins:
            self.plugins[plugin_name].shutdown()
            del self.plugins[plugin_name]

    def shutdown_plugin(self, plugin_name: str) -> None:
        if plugin_name in self.plugins:
            self.plugins[plugin_name].shutdown()

    def shutdown_all(self) -> None:
        for plugin in self.plugins.values():
            plugin.shutdown()

    def health_check_all(self) -> Dict[str, bool]:
        return {name: p.health_check() for name, p in self.plugins.items()}

    def get_plugin_state(self, plugin_name: str) -> Optional[PluginState]:
        plugin = self.plugins.get(plugin_name)
        return plugin.state if plugin else None

    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        return self.plugins.get(plugin_name)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        tools = []
        for plugin in self.plugins.values():
            if plugin.state in [PluginState.INITIALIZED, PluginState.ACTIVE]:
                tools.extend(plugin.get_tools())
        return tools

    def get_all_event_handlers(self) -> Dict[str, List[callable]]:
        handlers: Dict[str, List[callable]] = {}
        for plugin in self.plugins.values():
            if plugin.state in [PluginState.INITIALIZED, PluginState.ACTIVE]:
                plugin_handlers = plugin.get_event_handlers()
                for event_type, handler in plugin_handlers.items():
                    if event_type not in handlers:
                        handlers[event_type] = []
                    handlers[event_type].append(handler)
        return handlers

    def trigger_event(self, event_type: str, event_data: dict) -> Dict[str, Any]:
        results = {}
        handlers = self.get_all_event_handlers().get(event_type, [])
        for handler in handlers:
            try:
                handler(event_data)
                results[getattr(handler, "__name__", "handler")] = {"success": True, "error": None}
            except Exception as e:
                results[getattr(handler, "__name__", "handler")] = {"success": False, "error": str(e)}
        return results
