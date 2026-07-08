
from langchain.messages import SystemMessage, ToolMessage
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from typing import Callable
from src.skills import SKILLS, load_skill

visible_tools = [load_skill]

class InjectSkillsPromptMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt"""

    def __init__(self):
        """Initializes and creates the SKILLS prompt."""
        # Build skills prompt from the SKILLS list
        skills_list = []
        for skill in SKILLS:
            skills_list.append(
                f"- **{skill['name']}**: {skill['description']}"
            )
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Injects skill descriptions into the system prompt."""

        # Build the skills addendum
        skills_addendum = (
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about how to handle a specific type of request."
        )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)

class ActiveSkillsMiddleware(AgentMiddleware):
    """Middleware that tracks in the agent state which skills have been loaded into the context"""
    
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Allows dynamically loading tools associated with a skill"""

        messages = request.state["messages"]

        active_skills = set()
        for message in messages:
            if not isinstance(message, ToolMessage):
                continue
            
            for skill in SKILLS:
                if f"Skill loaded: \'{skill['name']}\'" in message.content:
                    active_skills.add(skill["name"])

        request.state["active_skills"] = active_skills

        return handler(request)

class DynamicSkillToolFilterMiddleware(AgentMiddleware):
    """Middleware that dynamically loads tools associated with a skill when it is loaded into the context"""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Allows dynamically loading tools associated with a skill."""

        state = request.state
        active_skills = state.get("active_skills", set())
        
        for active_skill in active_skills:
            for skill in SKILLS:
                if skill["name"] == active_skill:
                    request = request.override(tools=[*visible_tools, *skill["tools"]])
        else:
            request = request.override(tools=visible_tools)
        
        return handler(request)