from langchain_core.tools import tool

@tool
def frase_cherokee() -> dict:
    """Devuelve una frase aleatoria en cherokee"""
    
    return {
        "frase": "ᎣᏍᏓ ᏑᎾᎴᎢ",
        "traducción": "Buenos días",
        "pronunciación": "Osda sunalei"
    }

@tool
def frase_inuktitut() -> dict:
    """Devuelve una frase aleatoria en inuit"""
    
    return {
        "frase": "ᐅᓪᓛᓴᒃᑯᑦ",
        "traducción": "Buenos días",
        "pronunciación": "Ublaahatkut"
    }  

@tool
def frase_maori() -> dict:
    """Devuelve una frase aleatoria en maorí"""
    
    return {
        "frase": "Ata mārie",
        "traducción": "Buenos días",
        "pronunciación": "Ata marie"
    }
