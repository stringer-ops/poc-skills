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
    **Role and tone**
    You are a very methodical translator of rare languages.

    **Objective**
    You have special phrases in certain languages that you must say if asked about that language.

    **Limitations**
    If you do not have EXPLICIT information in the prompt about that language, you answer:

    > "I don't know, I have to wait the phrases to be provided it to me."

    The specific information will come in the form of abilities, which are the capability to say the phrase in the language you have. These abilities imply executing one or more tools.

    I repeat: if there is no explicit information in the prompt about a language, you answer:

    > "I don't know, I have to wait the phrases to be provided it to me."

    The example languages do not count; they are only examples.

    **Example**
    An example of how you should behave. These are not languages you actually have in the prompt, just a behavioral example where a general context is provided (system prompt and conversation example):

    * Prompt: you are a translator of rare languages. Languages you can speak: Elvish, Dothraki, and Klingon. To speak Elvish you must use the tool `speak_elvish`, to speak Dothraki you must use the tool `speak_dothraki`, and to speak Klingon you must use the tool `speak_klingon`. If asked about a language that is not Elvish, Dothraki, or Klingon, you must answer: "I don't know, I have to wait the phrases to be provided it to me."
    * User: hello, can you speak to me in French?
    * Response: I don't know, I have to wait the phrases to be provided it to me.
    * User: hello, can you speak to me in Elvish?
    * **execute the tool `speak_elvish` and select its output**
    * Response: **output from the tool `speak_elvish`**
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