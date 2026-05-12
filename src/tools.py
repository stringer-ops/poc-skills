from langchain_core.tools import tool
from skills import SKILLS

# ============================================ Tools ============================================
# ===============================================================================================

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

@tool
def frase_cherokee() -> str:
    """Devuelve una frase aleatoria en cherokee"""
    
    return {
        "frase": "ᎣᏍᏓ ᏑᎾᎴᎢ",
        "traducción": "Buenos días",
        "pronunciación": "Osda sunalei"
    }

@tool
def frase_inuktitut() -> str:
    """Devuelve una frase aleatoria en inuit"""
    
    return {
        "frase": "ᐅᓪᓛᓴᒃᑯᑦ",
        "traducción": "Buenos días",
        "pronunciación": "Ublaahatkut"
    }  

@tool
def frase_maori() -> str:
    """Devuelve una frase aleatoria en maorí"""
    
    return {
        "frase": "Ata mārie",
        "traducción": "Buenos días",
        "pronunciación": "Ata marie"
    }
