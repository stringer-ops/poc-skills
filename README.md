# POC Skills

Proof of concept chatbot built with Streamlit + LangChain that demonstrates skill-based behavior injection using agent middleware.

The assistant is configured as a translator of rare languages. It can load skill instructions at runtime and its related language tools associated with those skills.

## Quick Start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment

Set your Mistral API key using one of these options:

```bash
export MISTRAL_API_KEY="your-api-key"
```

Or create a `.env` file:

```env
MISTRAL_API_KEY=your-api-key
```

### 3) Run the app

```bash
streamlit run main.py
```

## Project Structure

- `main.py`: Streamlit UI, chat loop, and agent construction.
- `src/skills.py`: Skill catalog (`SKILLS`) and `load_skill` tool.
- `src/tools.py`: Phrase tools for Cherokee, Inuktitut, and Maori.
- `src/middleware.py`: Middleware that injects available skills and manages dynamic tool visibility.
- `requirements.txt`: Runtime dependencies.

## How It Works

1. User sends a message in the Streamlit chat UI.
2. The app creates a LangChain agent with:
	- Model: `mistral-small-latest`
	- Tools: `load_skill`, `cherokee_phrase`, `inuktitut_phrase`, `maori_phrase`
	- Middleware pipeline from `src/middleware.py`
3. Middleware appends a list of available skills to the system prompt.
4. The agent can call `load_skill(<skill_name>)` to load detailed instructions for a skill.
5. Loaded skills are tracked in state and intended to unlock skill-specific tools.

## Available Skills

- `speak_cherokee`: Uses `cherokee_phrase`.
- `speak_inuktitut`: Uses `inuktitut_phrase`.
- `speak_maori`: Uses `maori_phrase`.

Each phrase tool currently returns a dictionary with:
- `phrase`
- `translation`
- `pronunciation`

## Example Interaction

```text
User: Can you speak in Cherokee?
Assistant: I need to load the skill first.
Assistant tool call: load_skill("speak_cherokee")
Assistant: (skill loaded)
Assistant tool call: cherokee_phrase()
Assistant: ᎣᏍᏓ ᏑᎾᎴᎢ (Good morning) - pronunciation: Osda sunalei
```

## Limitations (Current State)

- This is a proof of concept, not a full translation engine.
- Phrase tools are currently fixed examples (not actually random).
- Chat history is only session-based in Streamlit state.
- Tool filtering middleware currently reverts to only the loader tool due loop/else behavior in `DynamicSkillToolFilterMiddleware`.