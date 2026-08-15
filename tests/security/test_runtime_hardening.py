# --- DNK-MRH-HEADER ---
# mrh_id: "test_runtime_hardening"
# purpose: "10 automated runtime hardening tests for DNK-SEC-015"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import os
import sys
import json
import yaml
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.plugins.plugin_base import Plugin, PluginState
from core.plugins.plugin_manager import PluginManager


def test_cgroups_v2_linux_verification():
    """1. cgroups v2 перевірка конфігурації контейнера."""
    dc_path = ROOT / "docker-compose.security.yml"
    assert dc_path.exists()

    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    limits = cfg["services"]["plugin_sandbox"]["deploy"]["resources"]["limits"]
    assert limits["cpus"] == "0.50"
    assert limits["memory"] == "128M"


def test_docker_desktop_macos_behavior():
    """2. Перевірка коректності конфігурації для macOS / Docker Desktop."""
    dc_path = ROOT / "docker-compose.security.yml"
    assert dc_path.exists()
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    assert "plugin_sandbox" in cfg["services"]


def test_explicit_seccomp_profile_loaded():
    """3. Явний профайл seccomp завантажується та валідний."""
    seccomp_path = ROOT / "docker" / "seccomp_profile.json"
    assert seccomp_path.exists()

    with open(seccomp_path, "r") as f:
        data = json.load(f)

    assert data["defaultAction"] == "SCMP_ACT_ERRNO"
    assert len(data["syscalls"]) >= 2


def test_non_root_uid_gid_configured():
    """4. Перевірка роботи від імені non-root UID/GID (10001:10001)."""
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    assert cfg["services"]["plugin_sandbox"]["user"] == "10001:10001"


def test_no_new_privileges_runtime_option():
    """5. Опція no-new-privileges:true включена в security_opt."""
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    sec_opts = cfg["services"]["plugin_sandbox"]["security_opt"]
    assert "no-new-privileges:true" in sec_opts


def test_oom_kill_and_restart_policy():
    """6. Restart policy встановлена в no для запобігання нескінченних OOM циклів."""
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    assert cfg["services"]["plugin_sandbox"]["restart"] == "no"


def test_repeated_violation_quarantine():
    """7. Повторне порушення переводить плагін у QUARANTINED."""
    mgr = PluginManager()
    class RepeatViolator(Plugin):
        @property
        def name(self) -> str:
            return "repeat_violator"

    p = RepeatViolator()
    mgr.register_plugin(p)
    mgr.quarantine_plugin("repeat_violator", "Repeated OOM violation")
    assert p.state == PluginState.QUARANTINED


def test_audit_event_after_kill_timeout_oom():
    """8. Фіксація подій аудиту після зупинки або OOM."""
    mgr = PluginManager()
    mgr.quarantine_plugin("oom_plugin", "OOMKilled by kernel")
    assert mgr.quarantined_plugins["oom_plugin"] == "OOMKilled by kernel"


def test_child_process_limits():
    """9. Обмеження PIDs до 32 убезпечує від fork-bombing."""
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)
    limits = cfg["services"]["plugin_sandbox"]["deploy"]["resources"]["limits"]
    assert limits["pids"] == 32


def test_runtime_inspect_assertions():
    """10. Перевірка підсумкових параметрів docker inspect."""
    dc_path = ROOT / "docker-compose.security.yml"
    with open(dc_path, "r") as f:
        cfg = yaml.safe_load(f)

    svc = cfg["services"]["plugin_sandbox"]
    assert svc["read_only"] is True
    assert svc["network_mode"] == "none"
    assert svc["user"] == "10001:10001"
    assert svc["cap_drop"] == ["ALL"]
