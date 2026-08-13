# --- DNK-MRH-HEADER ---
# mrh_id: "test_agent_plugins_spec"
# purpose: "13 automated verification tests for Agent Plugins 1.0 specifications"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import sys
import pathlib
import pytest
from uuid import uuid4
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.plugin_base import Plugin, PluginState
from core.plugins.plugin_manager import PluginManager
from plugins.slack_plugin.plugin import SlackPlugin
from plugins.notion_plugin.plugin import NotionPlugin
from core.services.security_gate_service import InlineSecurityGateService
from core.models.security import SecurityPolicy

class MockPlugin(Plugin):
    @property
    def name(self) -> str:
        return "mock"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_tools(self) -> list:
        return [{"name": "mock_action", "description": "Mock tool"}]

    def get_event_handlers(self) -> dict:
        return {"on_mock": self.on_event}

    def on_event(self, data: dict) -> None:
        pass


def test_manifest_validation_valid():
    mgr = PluginManager()
    manifest = {
        "name": "test_plugin",
        "version": "1.0.0",
        "extension_id": "com.dnk-os.plugin.test",
        "publisher": "DNK-e.com Maksym"
    }
    assert mgr.validate_manifest(manifest) is True


def test_manifest_validation_invalid():
    mgr = PluginManager()
    invalid_manifest = {"name": "test_plugin", "version": "1.0.0"}
    assert mgr.validate_manifest(invalid_manifest) is False


def test_extension_id_prefix_validation():
    mgr = PluginManager()
    wrong_ext = {
        "name": "test",
        "version": "1.0.0",
        "extension_id": "org.external.plugin.test",
        "publisher": "External"
    }
    assert mgr.validate_manifest(wrong_ext) is False


def test_plugin_lifecycle_state_machine():
    plugin = MockPlugin()
    assert plugin.state == PluginState.UNINITIALIZED

    mgr = PluginManager()
    mgr.register_plugin(plugin)
    assert plugin.state == PluginState.ACTIVE

    mgr.shutdown_plugin("mock")
    assert plugin.state == PluginState.STOPPED


def test_plugin_quarantine_untrusted():
    mgr = PluginManager()
    mgr.quarantine_plugin("malicious", "Revoked certificate")

    class MaliciousPlugin(MockPlugin):
        @property
        def name(self) -> str:
            return "malicious"

    p = MaliciousPlugin()
    mgr.register_plugin(p)
    assert p.state == PluginState.QUARANTINED
    assert "malicious" not in mgr.plugins


def test_unsandboxed_stdio_mcp_blocked():
    mgr = PluginManager()
    bad_mcp = {
        "mcpServers": {
            "untrusted": {
                "command": "bash",
                "transport": "stdio",
                "sandboxed": False
            }
        }
    }
    assert mgr.validate_mcp_config(bad_mcp) is False


def test_slack_plugin_adapter():
    plugin = SlackPlugin()
    assert plugin.name == "slack"
    assert plugin.extension_id == "com.dnk-os.plugin.slack"
    tools = plugin.get_tools()
    assert len(tools) == 1
    assert tools[0]["name"] == "send_slack_message"


def test_notion_plugin_adapter():
    plugin = NotionPlugin()
    assert plugin.name == "notion"
    assert plugin.extension_id == "com.dnk-os.plugin.notion"
    tools = plugin.get_tools()
    assert len(tools) == 1
    assert tools[0]["name"] == "create_notion_page"


def test_register_plugin():
    mgr = PluginManager()
    p = MockPlugin()
    mgr.register_plugin(p)
    assert "mock" in mgr.plugins
    assert mgr.get_plugin_state("mock") == PluginState.ACTIVE


def test_unregister_plugin():
    mgr = PluginManager()
    p = MockPlugin()
    mgr.register_plugin(p)
    mgr.unregister_plugin("mock")
    assert "mock" not in mgr.plugins


def test_get_all_tools():
    mgr = PluginManager()
    mgr.register_plugin(SlackPlugin())
    mgr.register_plugin(NotionPlugin())
    tools = mgr.get_all_tools()
    tool_names = [t["name"] for t in tools]
    assert "send_slack_message" in tool_names
    assert "create_notion_page" in tool_names


def test_get_all_event_handlers():
    mgr = PluginManager()
    mgr.register_plugin(SlackPlugin())
    handlers = mgr.get_all_event_handlers()
    assert "on_slack_message" in handlers


def test_security_gate_for_plugins():
    gate = InlineSecurityGateService()
    policy = SecurityPolicy(
        id=uuid4(),
        name="Block Slack tool",
        action_patterns=["send_slack_message"],
        conditions={},
        require_approval=True,
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    gate.create_policy(policy)

    decision = gate.evaluate_policy(uuid4(), "send_slack_message", {}, {})
    assert decision.allowed is False
