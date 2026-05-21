
from langchain.messages import SystemMessage
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from typing import Callable
from src.skills import SKILLS

class SkillMiddleware(AgentMiddleware):
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
