from typing import Callable, TypedDict
from langchain_core.tools import tool
from src.tools import frase_cherokee, frase_inuktitut, frase_maori

class Skill(TypedDict):
    """Una skill que puede ser descubierta al agente"""
    name: str #Identificador de la skill
    description: str #Breve descripción de la skill. Se tendrá en el sistem prompt
    content: str #Funcionamiento total de la skill de forma detallada
    tools: list[Callable] #Lista de herramientas asociadas a la skill

SKILLS: list[Skill] = [
    {
        "name": "habla_cherokee",
        "description": """Devuelve una frase aleatoria en cherokee, la lengua de los pueblos indígenas del 
            sureste de EE. UU., utilizada tradicionalmente por el pueblo cherokee""",
        "content": """Llama a la tool 'frase_cherokee' que recupera una frase aleatoria en cherokee. La herramienta también debe
            devolver su traducción al inglés y su pronunciación. En el mensaje que devuelvas al usuario debes incluir la frase en cherokee, su traducción al inglés y su pronunciación""",
        "tools": [frase_cherokee]
    },
    {
        "name": "habla_inuktitut",
        "description": """Devuelve una frase aleatoria en inuit, una lengua hablada en el Ártico canadiense, conocida por su sistema de
            escritura silábico""",
        "content": """Llama a la tool 'frase_inuktitut' que recupera una frase aleatoria en inuit. La herramienta también debe
            devolver su traducción al inglés y su pronunciación. En el mensaje que devuelvas al usuario debes incluir la frase en inuit, su traducción al inglés y su pronunciación""",
        "tools": [frase_inuktitut]
    },
    {
        "name": "habla_maori",
        "description": """Devuelve una frase aleatoria en maorí, la lengua de los pueblos indígenas de Nueva Zelanda (Aotearoa), 
            perteneciente a la familia de lenguas polinesias""",
        "content": """Llama a la tool 'frase_maori' que recupera una frase aleatoria en maorí. La herramienta también debe
            devolver su traducción al inglés y su pronunciación""",
        "tools": [frase_maori]
    },
]

@tool
def cargar_skill(skill_name: str) -> str:
    """Carga una skill específica en el prompt.

    Devuelve el nombre de la skill y toda la información de prompt asociada a ella para cubrir su casuística 
    correctamente
    """
    
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Skill cargada: '{skill['name']}'\n{skill['content']}"
        
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' no encontrada. Skills disponibles: {available}"
