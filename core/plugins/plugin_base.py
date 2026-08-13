# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_plugin_base"
# purpose: "Base abstract class for all system plugins enforcing Agent Plugins 1.0 contracts"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional

class PluginState(Enum):
    UNINITIALIZED = "UNINITIALIZED"
    REGISTERED = "REGISTERED"
    INITIALIZED = "INITIALIZED"
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    QUARANTINED = "QUARANTINED"
    ERROR = "ERROR"

class Plugin(ABC):
    def __init__(self):
        self._state: PluginState = PluginState.UNINITIALIZED
        self._quarantine_reason: Optional[str] = None

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    def extension_id(self) -> str:
        return f"com.dnk-os.plugin.{self.name}"

    @property
    def description(self) -> str:
        return ""

    @property
    def author(self) -> str:
        return "DNK-e.com Maksym"

    @property
    def capabilities(self) -> List[str]:
        return ["tools", "event_handlers"]

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {}

    @property
    def state(self) -> PluginState:
        return self._state

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._state = PluginState.INITIALIZED

    def activate(self) -> None:
        if self._state != PluginState.QUARANTINED:
            self._state = PluginState.ACTIVE

    def shutdown(self) -> None:
        self._state = PluginState.STOPPED

    def quarantine(self, reason: str) -> None:
        self._state = PluginState.QUARANTINED
        self._quarantine_reason = reason

    def health_check(self) -> bool:
        return self._state in [PluginState.INITIALIZED, PluginState.ACTIVE]

    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_event_handlers(self) -> Dict[str, callable]:
        pass
