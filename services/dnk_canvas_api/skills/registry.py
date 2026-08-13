# --- DNK-MRH-HEADER ---
# mrh_id: "skills/registry.py"
# purpose: "Manage registering, discovering, validating, and executing design skills with TimelineLogger integration."
# canonical_source: true
# status: "Active"
# version: "1.1.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# license: "DNK-INTERNAL"
# --- END DNK-MRH-HEADER ---

import inspect
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from .models import BaseSkill
from .dnk_ui_generate_workspace import DNKUiGenerateWorkspaceSkill


class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        # Register default skills
        self.register(DNKUiGenerateWorkspaceSkill())

    def register(self, skill: BaseSkill):
        self._skills[skill.contract.id] = skill

    def get_skill(self, skill_id: str) -> Optional[BaseSkill]:
        return self._skills.get(skill_id)

    def list_skills(self) -> Dict[str, Any]:
        return {skill_id: skill.contract.dict() for skill_id, skill in self._skills.items()}

    async def execute_skill(
        self,
        skill_id: str,
        params: Dict[str, Any],
        run_id: Optional[UUID] = None,
        timeline_logger: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Execute a skill with TimelineLogger action tracking."""
        skill = self.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill '{skill_id}' not found in registry")
        
        exec_run_id = run_id or uuid4()
        if timeline_logger:
            await timeline_logger.log_action_start(
                run_id=exec_run_id,
                agent_id="skill_registry",
                action_name=f"execute_skill:{skill_id}",
                payload=params,
            )
        
        try:
            if hasattr(skill, "execute"):
                if inspect.iscoroutinefunction(skill.execute):
                    result = await skill.execute(params)
                else:
                    result = skill.execute(params)
            else:
                result = {"status": "executed"}

            if timeline_logger:
                await timeline_logger.log_action_end(
                    run_id=exec_run_id,
                    agent_id="skill_registry",
                    action_name=f"execute_skill:{skill_id}",
                    status="success",
                    payload=result if isinstance(result, dict) else {"result": str(result)},
                )
            return result
        except Exception as e:
            if timeline_logger:
                await timeline_logger.log_action_end(
                    run_id=exec_run_id,
                    agent_id="skill_registry",
                    action_name=f"execute_skill:{skill_id}",
                    status="failed",
                    payload={"error": str(e)},
                )
            raise e


# Global registry instance
registry = SkillRegistry()
