from langchain_core.tools import tool

@tool
def cherokee_phrase() -> dict:
    """Returns a random phrase in Cherokee"""
    
    return {
        "phrase": "ᎣᏍᏓ ᏑᎾᎴᎢ",
        "translation": "Good morning",
        "pronunciation": "Osda sunalei"
    }

@tool
def inuktitut_phrase() -> dict:
    """Returns a random phrase in Inuktitut"""
    
    return {
        "phrase": "ᐅᓪᓛᓴᒃᑯᑦ",
        "translation": "Good morning",
        "pronunciation": "Ublaahatkut"
    }  

@tool
def maori_phrase() -> dict:
    """Returns a random phrase in Maori"""
    
    return {
        "phrase": "Ata mārie",
        "translation": "Good morning",
        "pronunciation": "Ata marie"
    }
