# Simple LangChain Agent

A simple but production-oriented LangChain chat agent with automatic tool selection, continuous terminal interaction, short-term conversation memory, PostgreSQL persistence, Docker Compose, and basic error handling.

This project demonstrates the core logic behind a larger Agentic AI system without adding unnecessary complexity.

## Project Overview

The agent can:

- communicate with an OpenAI model through LangChain
- automatically select and execute tools
- maintain conversation context during a running session
- store user and assistant messages in PostgreSQL
- reload previous conversation history after restarting the application
- limit the amount of history sent to the model
- handle empty input, keyboard interruption, and unexpected application errors

## Architecture

```text
User
  ↓
Terminal application
  ↓
Load conversation history from PostgreSQL
  ↓
Trim old messages
  ↓
LangChain agent
  ↓
OpenAI model
  ↓
Tool selection
  ├── Multiply numbers
  ├── Get current time
  └── Get project information
  ↓
Final response
  ↓
Save user and assistant messages in PostgreSQL
```

## Main Learning Objectives

This project demonstrates:

- LangChain model integration
- system prompts
- user and assistant messages
- LangChain tools
- automatic tool selection
- agent execution loops
- session memory
- persistent conversation memory
- PostgreSQL integration
- Docker Compose
- environment variable management
- conversation-history trimming
- basic error handling

## Technology Stack

- Python 3.12
- LangChain
- LangChain OpenAI integration
- OpenAI API
- PostgreSQL
- Psycopg 3
- Docker
- Docker Compose
- python-dotenv

## Project Structure

```text
simple-langchain-agent/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── agent.py
├── app.py
├── database.py
├── docker-compose.yml
├── llm.py
├── requirements.txt
└── tools.py
```

### File Responsibilities

```text
app.py
→ terminal chat loop, message handling, history trimming, and error handling

agent.py
→ LangChain agent configuration and registered tools

llm.py
→ OpenAI model configuration

tools.py
→ LangChain-compatible Python tools

database.py
→ PostgreSQL connection, table initialization, message saving, and message loading

docker-compose.yml
→ local PostgreSQL container configuration

.env
→ private environment variables and credentials

.env.example
→ example environment configuration without real secrets

requirements.txt
→ direct Python dependencies
```

## Current Tools

### Multiply Numbers

Multiplies two numbers.

Example:

```text
You: What is 30 multiplied by 12?
Agent: 30 multiplied by 12 is 360.
```

### Current Time

Returns the current local date and time.

Example:

```text
You: What is the current time?
Agent: The current local date and time is ...
```

### Project Information

Returns a short description of the project.

Example:

```text
You: Tell me about this project.
Agent: This project is a simple LangChain agent project...
```

The agent can also answer normal questions without using a tool.

## Prerequisites

Install the following:

- Python 3.10 or newer
- Docker
- Docker Compose
- Git
- an OpenAI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/simple-langchain-agent.git
cd simple-langchain-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create the local environment file:

```bash
cp .env.example .env
```

Update `.env`:

```env
OPENAI_API_KEY=your_openai_api_key

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=langchain_agent
POSTGRES_USER=langchain_user
POSTGRES_PASSWORD=your_secure_postgres_password
```

Do not commit `.env` to GitHub.

## PostgreSQL Setup

Start PostgreSQL with Docker Compose:

```bash
docker compose up -d
```

Check the container:

```bash
docker compose ps
```

Verify PostgreSQL readiness:

```bash
docker exec simple-langchain-postgres \
  pg_isready -U langchain_user -d langchain_agent
```

Expected output:

```text
/var/run/postgresql:5432 - accepting connections
```

## Initialize the Database

Run:

```bash
python database.py
```

Expected output:

```text
Database table initialized successfully.
```

The application creates the following table:

```text
chat_messages
├── id
├── session_id
├── role
├── content
└── created_at
```

## Run the Agent

```bash
python app.py
```

Example:

```text
Simple LangChain Agent
Type 'exit' to stop.
Loaded 0 saved messages.

You: My name is Chathuranga.
Agent: Hello Chathuranga!

You: What is my name?
Agent: Your name is Chathuranga.

You: What is 20 multiplied by 15?
Agent: 20 multiplied by 15 is 300.

You: exit
Agent: Goodbye!
```

## Persistent Memory Test

Run the application:

```bash
python app.py
```

Enter:

```text
You: My name is Chathuranga.
You: exit
```

Start the application again:

```bash
python app.py
```

Ask:

```text
You: What is my name?
```

The agent should load the previous conversation from PostgreSQL and answer correctly.

## Conversation Memory

The project uses two memory levels.

### Session Memory

During execution, messages are stored in a Python list in RAM.

```text
messages = [
    user message,
    assistant message,
    tool message,
    ...
]
```

### Persistent Memory

User and assistant messages are stored in PostgreSQL.

```text
Application stops
→ RAM memory is cleared
→ PostgreSQL history remains
→ history is loaded when the application starts again
```

## Conversation History Trimming

The application limits the amount of conversation history sent to the model.

```text
Full retained history
→ remove older messages
→ keep recent messages
→ send shorter context to the agent
```

This helps reduce:

- token usage
- API cost
- response latency
- context-window growth

The current implementation uses message-count-based trimming for learning purposes.

## Error Handling

The application handles:

- empty user input
- `Ctrl+C`
- end-of-file input
- unexpected agent errors
- failed requests without terminating the entire chat loop

Example:

```text
Agent error: <error details>
Please try again.
```

## Security

The following files and values must not be committed:

```text
.env
OpenAI API keys
database passwords
local virtual environments
Python cache files
```

Recommended `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

## Docker Commands

Start PostgreSQL:

```bash
docker compose up -d
```

Stop PostgreSQL:

```bash
docker compose stop
```

Stop and remove the container:

```bash
docker compose down
```

Stop and remove the container and stored database volume:

```bash
docker compose down -v
```

Warning: the final command deletes the persisted PostgreSQL data.

## Current Limitations

- one fixed session ID is used
- no user authentication
- tool-call metadata is not persisted
- conversation history uses a simple message-count limit
- no streaming responses
- no automated tests yet
- no tracing or observability
- no web API
- PostgreSQL credentials are intended for local development
- no semantic long-term memory
- no vector search

## Planned Improvements

- support multiple conversation sessions
- generate or accept unique session IDs
- persist tool-call metadata
- add PostgreSQL connection pooling
- add structured logging
- add retry and timeout handling
- use real token-based history trimming
- add LangSmith tracing
- add unit and integration tests
- add Pytest agent evaluation
- add FastAPI endpoints
- add streaming responses
- add Docker support for the Python application
- add PostgreSQL with pgvector
- add semantic long-term memory
- add Retrieval-Augmented Generation
- rebuild the workflow with LangGraph
- add human approval for sensitive tools

## Why This Project Matters

The project is intentionally small, but it demonstrates the main execution flow used by larger Agentic AI systems:

```text
User input
→ conversation context
→ model reasoning
→ automatic tool selection
→ tool execution
→ final response
→ persistent memory
```

Production Agentic AI systems use the same foundation and add stronger reliability, evaluation, security, observability, deployment, and workflow control.

## License

This project is available under the MIT License.