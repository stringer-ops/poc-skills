from typing import Callable, TypedDict
from langchain_core.tools import tool
from src.tools import cherokee_phrase, inuktitut_phrase, maori_phrase

class Skill(TypedDict):
    """A skill that can be disclosed by the agent"""
    name: str  # Skill identifier
    description: str  # Brief skill description. It will be in the system prompt
    content: str  # Full skill functionality in detail
    tools: list[Callable]  # List of tools associated with the skill

SKILLS: list[Skill] = [
    {
        "name": "speak_cherokee",
        "description": """Returns a random phrase in Cherokee, the language of the indigenous peoples of the 
            southeastern United States, traditionally used by the Cherokee people""",
        "content": """Call the 'cherokee_phrase' tool which retrieves a random phrase in Cherokee. 
            The tool should also return its English translation and pronunciation. In the message you return 
            to the user, you must include the Cherokee phrase, its English translation, and its pronunciation""",
        "tools": [cherokee_phrase]
    },
    {
        "name": "speak_inuktitut",
        "description": """Returns a random phrase in Inuktitut or Inuit, a language spoken in the Canadian Arctic, 
            known for its syllabic writing system""",
        "content": """Call the 'inuktitut_phrase' tool which retrieves a random phrase in Inuktitut or Inuit. 
            The tool should also return its English translation and pronunciation. In the message you return to the user, 
            you must include the Inuit phrase, its English translation, and its pronunciation""",
        "tools": [inuktitut_phrase]
    },
    {
        "name": "speak_maori",
        "description": """Returns a random phrase in Maori, the language of the indigenous peoples of 
            New Zealand (Aotearoa), belonging to the Polynesian language family""",
        "content": """Call the 'maori_phrase' tool which retrieves a random phrase in Maori. The tool 
            should also return its English translation and pronunciation. In the message you return to the user, 
            you must include the Maori phrase, its English translation, and its pronunciation""",
        "tools": [maori_phrase]
    },
]

@tool
def cargar_skill(skill_name: str) -> str:
    """Loads a specific skill into the prompt.

    Returns the skill name and all prompt information associated with it to properly handle its use cases.
    """
    
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Skill loaded: '{skill['name']}'\n{skill['content']}"
        
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"
