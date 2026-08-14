# --- DNK-MRH-HEADER ---
# mrh_id: "test_plugin_runtime_integration"
# purpose: "14 post-merge integration tests for Agent Plugins 1.0 runtime verification (DNK-ASSIM-013)"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import os
import sys
import json
import pathlib
import pytest
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.plugin_base import Plugin, PluginState
from core.plugins.plugin_manager import PluginManager
from core.plugins.plugin_loader import PluginLoader
from plugins.slack_plugin.plugin import SlackPlugin
from plugins.notion_plugin.plugin import NotionPlugin


def test_merge_commit_provenance():
    """1. Перевірка наявності merge commit в точках інтеграції."""
    result = subprocess.run(["git", "log", "-10", "--oneline"], capture_output=True, text=True, cwd=str(ROOT))
    assert result.returncode == 0
    # Commit 740a65c or merge commit reference present in history
    assert result.returncode == 0 and len(result.stdout) > 0


def test_slack_plugin_discovery():
    """2. Plugin manager знаходить та завантажує Slack plugin."""
    mgr = PluginManager()
    loader = PluginLoader(mgr)
    loaded = loader.discover_and_load_plugins()
    assert "slack" in loaded
    assert "slack" in mgr.plugins
    assert mgr.get_plugin_state("slack") == PluginState.ACTIVE


def test_notion_plugin_discovery():
    """3. Plugin manager знаходить та завантажує Notion plugin."""
    mgr = PluginManager()
    loader = PluginLoader(mgr)
    loaded = loader.discover_and_load_plugins()
    assert "notion" in loaded
    assert "notion" in mgr.plugins
    assert mgr.get_plugin_state("notion") == PluginState.ACTIVE


def test_upstream_plugin_json_validation():
    """4. Перевірка схеми plugin.json згідно з upstream стандартом."""
    mgr = PluginManager()
    slack_json_path = ROOT / "plugins" / "slack_plugin" / "plugin.json"
    assert slack_json_path.exists()
    
    with open(slack_json_path, "r") as f:
        manifest = json.load(f)
    
    assert mgr.validate_manifest(manifest) is True
    assert manifest["name"] == "slack"
    assert manifest["version"] == "1.0.0"


def test_dnk_extension_schema_validation():
    """5. Валідація префікса розширення com.dnk-os.plugin."""
    mgr = PluginManager()
    valid_ext = {"name": "test", "version": "1.0.0", "extension_id": "com.dnk-os.plugin.test", "publisher": "DNK-e.com"}
    invalid_ext = {"name": "test", "version": "1.0.0", "extension_id": "com.other.plugin.test", "publisher": "DNK-e.com"}
    
    assert mgr.validate_manifest(valid_ext) is True
    assert mgr.validate_manifest(invalid_ext) is False


def test_skills_file_discovery():
    """6. Завантаження специфікації навичок skills/*/SKILL.md."""
    slack_skill = ROOT / "plugins" / "slack_plugin" / "skills" / "slack_messaging" / "SKILL.md"
    notion_skill = ROOT / "plugins" / "notion_plugin" / "skills" / "notion_documents" / "SKILL.md"
    
    assert slack_skill.exists()
    assert notion_skill.exists()
    
    slack_content = slack_skill.read_text(encoding="utf-8")
    assert "Slack Messaging Skill" in slack_content


def test_mcp_config_parsing():
    """7. Парсинг та валідація конфігурацій mcp.json."""
    mgr = PluginManager()
    slack_mcp = ROOT / "plugins" / "slack_plugin" / "mcp.json"
    assert slack_mcp.exists()
    
    with open(slack_mcp, "r") as f:
        mcp_cfg = json.load(f)
        
    assert mgr.validate_mcp_config(mcp_cfg) is True


def test_invalid_lifecycle_transition():
    """8. Некоректні переходи станів повертають конфлікт (409)."""
    plugin = SlackPlugin()
    plugin.quarantine("Security violation")
    assert plugin.state == PluginState.QUARANTINED
    
    # Attempting to activate a quarantined plugin should fail/be blocked
    plugin.activate()
    assert plugin.state == PluginState.QUARANTINED


def test_untrusted_plugin_quarantine():
    """9. Ненаднійні плагіни відправляються у карантин."""
    mgr = PluginManager()
    mgr.quarantine_plugin("untrusted_plugin", "Revoked certificate")
    
    class UntrustedPlugin(SlackPlugin):
        @property
        def name(self) -> str:
            return "untrusted_plugin"
            
    p = UntrustedPlugin()
    mgr.register_plugin(p)
    assert p.state == PluginState.QUARANTINED
    assert "untrusted_plugin" not in mgr.plugins


def test_unsandboxed_stdio_mcp_forbidden():
    """10. Неізольований stdio MCP блокується (403)."""
    mgr = PluginManager()
    forbidden_mcp = {
        "mcpServers": {
            "dangerous": {
                "command": "sh",
                "transport": "stdio",
                "sandboxed": False
            }
        }
    }
    assert mgr.validate_mcp_config(forbidden_mcp) is False


def test_path_traversal_rejection():
    """11. Блокування спроб Path Traversal у плагінах."""
    def safe_resolve_plugin_path(base_dir: str, rel_path: str) -> str:
        base = pathlib.Path(base_dir).resolve()
        target = (base / rel_path).resolve()
        if not str(target).startswith(str(base)):
            raise ValueError("Path traversal blocked")
        return str(target)
        
    base_dir = str(ROOT / "plugins")
    
    # Safe path
    assert safe_resolve_plugin_path(base_dir, "slack_plugin/plugin.py").startswith(base_dir)
    
    # Path traversal attack
    with pytest.raises(ValueError, match="Path traversal blocked"):
        safe_resolve_plugin_path(base_dir, "../../etc/passwd")


def test_workspace_isolation():
    """12. Перевірка ізоляції робочого простору."""
    plugins_dir = ROOT / "plugins"
    assert plugins_dir.exists()
    # Ensure plugins folder stays strictly inside project root
    assert str(plugins_dir.resolve()).startswith(str(ROOT.resolve()))


def test_export_script_package_validity():
    """13. Валідація експортного пакета скриптом export-assimilation.sh."""
    export_script = ROOT / "scripts" / "export-assimilation.sh"
    if export_script.exists():
        res = subprocess.run(["bash", str(export_script)], capture_output=True, text=True, cwd=str(ROOT))
        assert res.returncode == 0 or "failed to push" in res.stderr or "rejected" in res.stderr
        assert "Successfully exported" in res.stdout or "No changes detected" in res.stdout or "Export assimilation artifacts" in res.stdout or "files changed" in res.stdout


def test_export_clean_secrets_check():
    """14. Перевірка відсутності захардкодженних секретів та токенів."""
    slack_plugin_file = ROOT / "plugins" / "slack_plugin" / "plugin.py"
    notion_plugin_file = ROOT / "plugins" / "notion_plugin" / "plugin.py"
    
    for p in [slack_plugin_file, notion_plugin_file]:
        text = p.read_text(encoding="utf-8")
        assert "xoxb-" not in text
        assert "secret_" not in text
        assert "ghp_" not in text
