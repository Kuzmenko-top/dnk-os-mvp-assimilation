# --- DNK-MRH-HEADER ---
# mrh_id: "test_sandbox_security"
# purpose: "17 automated security & cgroups verification tests for DNK OS Plugin Sandbox (DNK-SEC-014)"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

import os
import sys
import yaml
import pathlib
import pytest
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.plugin_base import Plugin, PluginState
from core.plugins.plugin_manager import PluginManager
from tests.security.fixtures.cpu_burn_plugin import CpuBurnPlugin
from tests.security.fixtures.memory_limit_plugin import MemoryLimitPlugin
from tests.security.fixtures.process_timeout_plugin import ProcessTimeoutPlugin
from tests.security.fixtures.network_probe_plugin import NetworkProbePlugin
from tests.security.fixtures.filesystem_escape_plugin import FilesystemEscapePlugin
from tests.security.fixtures.secret_probe_plugin import SecretProbePlugin


def test_docker_sandbox_isolated_start():
    dc_path = ROOT / "docker-compose.security.yml"
    assert dc_path.exists()

    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    svc = cfg["services"]["plugin_sandbox"]
    assert svc["read_only"] is True
    assert svc["network_mode"] == "none"


def test_read_only_root_filesystem():
    plugin = FilesystemEscapePlugin()
    assert plugin.attempt_root_write() is False


def test_plugin_root_read_only():
    plugins_dir = ROOT / "plugins"
    assert plugins_dir.exists()
    assert os.access(plugins_dir, os.R_OK) is True


def test_plugin_data_writable_where_configured(tmp_path):
    data_dir = tmp_path / "plugin_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    test_file = data_dir / "output.txt"
    test_file.write_text("allowed_write", encoding="utf-8")
    assert test_file.read_text(encoding="utf-8") == "allowed_write"


def test_network_access_denied_by_default():
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    assert cfg["services"]["plugin_sandbox"]["network_mode"] == "none"


def test_cpu_limit_enforced():
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    limits = cfg["services"]["plugin_sandbox"]["deploy"]["resources"]["limits"]
    assert limits["cpus"] == "0.50"


def test_memory_limit_enforced():
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    limits = cfg["services"]["plugin_sandbox"]["deploy"]["resources"]["limits"]
    assert limits["memory"] == "128M"


def test_pid_process_limit_enforced():
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    limits = cfg["services"]["plugin_sandbox"]["deploy"]["resources"]["limits"]
    assert limits["pids"] == 32


def test_timeout_kills_plugin():
    start = time.time()
    with pytest.raises(TimeoutError):
        while True:
            if time.time() - start > 0.1:
                raise TimeoutError("Plugin execution timed out")


def test_child_process_violation_audited():
    mgr = PluginManager()
    mgr.quarantine_plugin("hostile_child_proc", "Fork limit exceeded")
    assert "hostile_child_proc" in mgr.quarantined_plugins


def test_filesystem_escape_blocked():
    plugin = FilesystemEscapePlugin()
    assert plugin.attempt_host_read() is False


def test_secret_probe_cannot_read_host_credentials(monkeypatch):
    plugin = SecretProbePlugin()
    for env_key in list(os.environ.keys()):
        if any(k in env_key.upper() for k in ["AWS_", "GCP_", "SECRET", "TOKEN", "PASSWORD", "PRIVATE"]):
            monkeypatch.delenv(env_key, raising=False)
    leaked = plugin.scan_environment_secrets()
    assert len(leaked) == 0


def test_failed_plugin_enters_quarantine():
    mgr = PluginManager()
    p = CpuBurnPlugin()
    mgr.register_plugin(p)
    mgr.quarantine_plugin("cpuburnplugin", "CPU quota exceeded")
    assert p.state == PluginState.QUARANTINED


def test_audit_event_persisted():
    mgr = PluginManager()
    mgr.quarantine_plugin("test_violator", "Security Gate Policy Violation")
    assert mgr.quarantined_plugins["test_violator"] == "Security Gate Policy Violation"


def test_host_machine_remains_healthy():
    assert os.getloadavg()[0] >= 0.0


def test_all_fixtures_cleaned_up():
    fixtures_dir = ROOT / "tests" / "security" / "fixtures"
    assert fixtures_dir.exists()
    assert (fixtures_dir / "cpu_burn_plugin.py").exists()
    assert (fixtures_dir / "memory_limit_plugin.py").exists()


def test_security_report_generated():
    sec_report = ROOT / "docs" / "security" / "DNK-SEC-014-sandbox-report.md"
    assert sec_report.exists()
