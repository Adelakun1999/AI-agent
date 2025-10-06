# 🤖 AI Assistant for RAG Cookbooks

An AI-powered assistant that helps students quickly find answers to the rag cookbook repo from [RAG-COOKBOOKS](https://github.com/athina-ai/rag-cookbooks).
Built as a project for the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/).


## Overview

When working with RAG systems and cookbooks, developers often struggle to quickly find relevant examples, patterns, or nuance in the documentation. Searching through large docs or codebases is slow, error-prone, and contextually shallow.:
- Searches the **rag-cookbooks** repository  
- Retrieves the most relevant content  
- Generates helpful answers with references to the original materials

  

Why it's useful:

- Retrieve relevant cookbook sections or code snippets  
- Understand developer intent and disambiguate queries  
- Provide concise, context-aware answers  
- Speed up the developer workflow and reduce cognitive load 


## Installation

Requirements:

- Python 3.9+  
- [uv](https://github.com/astral-sh/uv) 

```bash
# Make sure you have uv
pip install uv

# Clone this repo
git clone https://github.com/Adelakun1999/AI-agent.git
cd project

# Install dependencies
uv sync
```

For API key management, we recommend using [direnv](https://direnv.net/) (see [`.envrc_template`](.envrc_template)).


## Usage

### API key

Set up your OpenAI API key:

```bash
export OPENAI_API_KEY="your-key"
```

### CLI mode  

```bash
uv run main.py
```

This opens an interactive CLI environment. You can ask the conversational agent any question about the course.

<img src="images/cli.gif" />

Type `stop` to exit.  

### Web UI mode  

```bash
uv run streamlit run app.py
```

<img src="images/streamlit.gif" />

This launches a Streamlit app. You can chat with the assistant in your browser.  

The app is available at [http://localhost:8501](http://localhost:8501).


## Features

- 🔎 Search over FAQ Markdown files with `minsearch`  
- 🤖 AI-generated answers powered by `pydantic-ai` + OpenAI (`gpt-4o-mini`)  
- 📂 Direct GitHub references in answers
- 🖥️ Two interfaces: CLI (`main.py`) and Streamlit (`app.py`)  
- 📝 Automatic logging of conversations into JSON files (`logs/`)  


## Evaluations

We evaluate the agent using the following criteria:

- `instructions_follow`: The agent followed the user's instructions
- `instructions_avoid`: The agent avoided doing things it was told not to do  
- `answer_relevant`: The response directly addresses the user's question  
- `answer_clear`: The answer is clear and correct  
- `answer_citations`: The response includes proper citations or sources when required  
- `completeness`: The response is complete and covers all key aspects of the request
- `tool_call_search`: Is the search tool invoked? 




## Project file overview

`main.py`: Entry point for the CLI version of the assistant  
- Loads and indexes FAQ data  
- Initializes the search agent  
- Provides an interactive loop where users can type questions and get answers  
- Logs each interaction to a JSON file

`app.py`: Streamlit-based web UI for the assistant  
- Provides a chat-like interface in the browser  
- Streams assistant responses in real time  
- Logs all interactions into JSON files

`ingest.py`: Handles data ingestion and indexing from the GitHub FAQ repository
- Downloads the repository ZIP archive  
- Extracts `.md` and `.mdx` files  
- Optionally chunks documents into smaller windows  
- Builds a `minsearch` index for fast text-based retrieval

`search_tools.py`: Defines the search tool used by the agent  
- Wraps the `minsearch` index into a simple API  
- Provides a `search(query)` tool that retrieves up to 5 results

`search_agent.py`: Defines and configures the AI Agent  
- Uses `pydantic-ai` to build the agent  
- Loads a system prompt template that instructs the assistant on how to answer FAQ questions  
- Attaches the search tool so the agent can query the FAQ index  
- Configured with the `gpt-4o-mini` model

`logs.py`: Utility for logging all interactions  
- Serializes messages, prompts, and model metadata  
- Stores logs in JSON files in the `logs/` directory (configurable via `LOGS_DIRECTORY`)  
- Ensures each log has a timestamp and unique filename


## Tests

TODO: add tests

```bash
uv run pytest
```

(Currently minimal test coverage; contributions welcome.)  


## Deployment

To deploy the app on Streamlit Cloud:

Generate a `requirements.txt` file from your `uv` environment:

```bash
uv export > requirements.txt
```

Make sure it's pushed along with the latest changes.

Next, run the application locally:

```bash
uv run streamlit run app.py
```

Click "deploy", connect your GitHub repo, and configure deployment settings.

In the settings, make sure you configure `OPENAI_API_KEY`.

Once configured, Streamlit Cloud will automatically detect changes. It will redeploy your app whenever you push updates.


## Credits / Acknowledgments

- [RAG-Cookbooks](https://github.com/Adelakun1999/AI-agent.git) for open-source course materials  
- [Alexey Grigorev](https://www.linkedin.com/in/agrigorev) for the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/)  
- Main libraries: `pydantic-ai` for AI, `minsearch` for search
