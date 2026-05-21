
from langchain.messages import SystemMessage, ToolMessage
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from typing import Callable
from src.skills import SKILLS, cargar_skill

class InjectSkillsPromptMiddleware(AgentMiddleware):
    """Middleware que inyecta las descripciones en el prompt del sistema"""

    def __init__(self):
        """Inicializa y crea el prompt de SKILLS."""
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
        """ Inyecta descripciones de skills en el prompt del sistema."""

        # Build the skills addendum
        skills_addendum = (
            f"\n\n## Habilidades disponibles\n\n{self.skills_prompt}\n\n"
            "Usa la tool cargar_skill cuando necesites información detallada "
            "sobre cómo manejar un tipo específico de solicitud."
        )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)

class ActiveSkillsMiddleware(AgentMiddleware):
    """Middleware que registra en el estado del agente las skills que han sido cargadas en el context"""
    
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Permite cargar dinámicamente tools asociadas a una skill"""

        messages = request.state["messages"]

        active_skills = set()
        for message in messages:
            if not isinstance(message, ToolMessage):
                continue
            
            for skill in SKILLS:
                if f"Skill cargada: '{skill["name"]}'" in message.content:
                    active_skills.add(skill["name"])

        request.state["active_skills"] = active_skills

        return handler(request)

class DynamicSkillToolFilterMiddleware(AgentMiddleware):
    """Middleware que permite cargar dinámicamente tools asociadas a una skill cuando
    esta es cargada en el contexto"""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Permite cargar dinámicamente tools asociadas a una skill."""

        state = request.state
        active_skills = state.get("active_skills", set())
        
        visible_tools = [cargar_skill]
        if active_skills:
            for active_skill in active_skills:
                for skill in SKILLS:
                    if skill["name"] == active_skill:
                        request = request.override(tools=[*visible_tools, *skill["tools"]])
        else:
            request = request.override(tools=visible_tools)
        
        return handler(request)