import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import create_agent
from src.middleware import InjectSkillsPromptMiddleware, ActiveSkillsMiddleware, DynamicSkillToolFilterMiddleware
from src.skills import cargar_skill
from src.tools import frase_cherokee, frase_inuktitut, frase_maori

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

SYSTEM_PROMPT = """
    **Rol y tono**
    Eres un un traductor de idiomas raros muy metódico.

    **Objetivo**
    Tienes frases especiales en ciertos idiomas que tienes que decir si te preguntan por ese idioma.

    **Limitaciones**
    Si no tienes información ÉXPLÍCITA en el prompt sobre ese idioma, contestas "No lo sé, tengo que esperara a que me 
    la proporcionen". La información específica vendrá en forma de habilidades, que son el poder decir la frase en el idioma que tienes. Estas habiliades implican ejecutar una o varias tools.
    Repito, si no hay información explícita en el prompt sobre un idioma, contestas "No lo sé, tengo que esperara a que me la proporcionen". Los idiomas del ejemplo no cuentan,
    son un ejemplo

    **Ejemplo**
    Un ejemplo de como habría que comportarse. Esto no son idiomas que tengas en el prompt, solo un ejemplo de comportamiento donde se pone un contexto general (prompt del sistema y ejemplo de conversación):
    - Prompt: eres un traductor de idiomas raros. Idiomas que puedes hablar: élfico, dothraki y klingon. Para hablar en elfico tienes que utilizar la tool hablar_elfico, para hablar en dothraki tienes que utilizar la tool hablar_dothraki y para hablar en klingon tienes que utilizar la tool hablar_klingon. Si te preguntan por un idioma que no es élfico, dothraki o klingon, tienes que contestar "No lo sé, tengo que esperara a que me la proporcionen".
    - Usuario: hola, puedes hablarme en francés?
    - Respuesta: No lo sé, tengo que esperara a que me la proporcionen.
    - Usuario: hola, puedes hablarme en élfico?
    **ejecutar la tool hablar_elfico y seleccionas la salida**
    - Respuesta: **respuesta de la tool hablar_elfico**
"""

def generate_agent():

    tools = [
        cargar_skill, frase_cherokee, frase_inuktitut, frase_maori
    ]
    
    agent = create_agent(
        system_prompt=SYSTEM_PROMPT,
        model="mistral-small-latest",
        tools=tools,
        middleware=[
            InjectSkillsPromptMiddleware(),
            ActiveSkillsMiddleware(),
            DynamicSkillToolFilterMiddleware()
        ],
        debug=True
    )

    return agent

def main():

    st.set_page_config(page_title="POC Skills", layout="centered")
    st.title("Chatbot POC Skills")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_prompt = st.chat_input("Escribe tu mensaje...")
    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))

        for message in st.session_state.messages:
            if not isinstance(message, SystemMessage):
                if isinstance(message, AIMessage):
                    render_type = "assistant"
                elif isinstance(message, HumanMessage):
                    render_type = "user"
                
                with st.chat_message(render_type):
                    st.markdown(message.content)
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()

            agent = generate_agent()

            result = agent.invoke(
                {
                    "messages": st.session_state.messages,
                },
            )
            last_message = result['messages'][-1]
            response_placeholder.markdown(last_message.content)

        st.session_state.messages.append(AIMessage(content=last_message.content))

if __name__ == "__main__":
    main()