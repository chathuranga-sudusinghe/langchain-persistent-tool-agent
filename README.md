# LangChain Persistent Tool Agent

A focused LangChain agent project demonstrating automatic tool selection, continuous terminal interaction, multi-session conversation handling, PostgreSQL-backed persistent memory, Docker Compose, and basic automated tests.

The project is intentionally compact. Its purpose is to show the core execution and memory logic used in larger Agentic AI systems without introducing unnecessary infrastructure.

## Key Features

- OpenAI model integration through LangChain
- Automatic tool selection and execution
- Continuous terminal chat loop
- Multiple conversation sessions using session IDs
- In-memory conversation context during runtime
- PostgreSQL-backed persistent chat history
- Conversation restoration after application restart
- `/clear` command for deleting the active session history
- Message-history trimming before model invocation
- Basic input and runtime error handling
- Pytest coverage for the calculator tool
- Docker Compose setup for local PostgreSQL

## Architecture

```text
User
  ↓
Terminal chat application
  ↓
Load selected session history from PostgreSQL
  ↓
Append current user message
  ↓
Trim retained conversation context
  ↓
LangChain agent
  ↓
OpenAI model
  ↓
Automatic tool selection
  ├── Multiply numbers
  ├── Get current local time
  └── Get project information
  ↓
Final response
  ↓
Save user and assistant messages to PostgreSQL
```

## Technology Stack

- Python 3.12
- LangChain
- LangChain OpenAI integration
- OpenAI API
- PostgreSQL 17
- Psycopg 3
- Docker and Docker Compose
- python-dotenv
- Pytest

## Project Structure

```text
langchain-persistent-tool-agent/
├── .env.example
├── .gitignore
├── README.md
├── agent.py
├── app.py
├── database.py
├── docker-compose.yml
├── llm.py
├── requirements.txt
├── tools.py
└── tests/
    └── test_tools.py
```

## File Responsibilities

- `app.py` — terminal chat loop, session selection, history trimming, persistence flow, `/clear`, and error handling
- `agent.py` — LangChain agent configuration and tool registration
- `llm.py` — OpenAI model configuration
- `tools.py` — LangChain-compatible tools
- `database.py` — PostgreSQL connection, table initialization, save/load, and session-history deletion
- `docker-compose.yml` — local PostgreSQL service and persistent volume
- `tests/test_tools.py` — calculator tool tests
- `.env.example` — safe environment-variable template

## Available Tools

### Multiply Numbers

```text
You: What is 30 multiplied by 12?
Agent: 30 multiplied by 12 is 360.
```

### Current Time

```text
You: What is the current time?
Agent: The current local date and time is ...
```

### Project Information

```text
You: Tell me about this project.
Agent: This project demonstrates LangChain model integration, automatic tool selection, and persistent conversation memory.
```

The agent can also answer general questions without calling a tool.

## Prerequisites

- Python 3.10 or newer
- Docker
- Docker Compose
- Git
- OpenAI API key

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/chathuranga-sudusinghe/langchain-persistent-tool-agent.git
cd langchain-persistent-tool-agent
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

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

Never commit `.env`.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

Verify the service:

```bash
docker compose ps
```

### 6. Initialize the database

```bash
python database.py
```

Expected output:

```text
Database table initialized successfully.
```

### 7. Run the agent

```bash
python app.py
```

Example:

```text
Enter session ID: learning
Simple LangChain Agent
Type 'exit' to stop or '/clear' to clear this session.
Session: learning
Loaded 0 saved messages.

You: My name is Chathuranga.
Agent: Hello Chathuranga!

You: What is my name?
Agent: Your name is Chathuranga.
```

## Persistent Memory

Each conversation is identified by a `session_id`.

```text
Session: learning
Session: interview
Session: project-notes
```

Messages are stored in PostgreSQL with:

```text
chat_messages
├── id
├── session_id
├── role
├── content
└── created_at
```

When the application restarts, it reloads only the selected session history.

## Clear the Active Session

Inside the chat, run:

```text
/clear
```

This deletes only the active session from PostgreSQL and clears its in-memory history. Other sessions remain unchanged.

## Conversation Trimming

Before each model request, the application trims older retained messages and sends the latest context to the agent.

This reduces:

- token usage
- API cost
- response latency
- context-window growth

The current implementation uses message-count-based trimming for learning clarity.

## Testing

Run:

```bash
python -m pytest -v
```

Current tests cover:

- positive-number multiplication
- negative-number multiplication
- multiplication by zero

## Security

The repository excludes:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

Do not commit API keys, database passwords, or local environment files.

## Useful Docker Commands

Start PostgreSQL:

```bash
docker compose up -d
```

Stop PostgreSQL:

```bash
docker compose stop
```

Remove the container while retaining the database volume:

```bash
docker compose down
```

Remove the container and stored database data:

```bash
docker compose down -v
```

The final command permanently removes the local PostgreSQL volume.

## Current Scope and Limitations

- terminal interface only
- PostgreSQL connections are created per operation; no connection pool
- tool-call metadata is not persisted
- message-count-based trimming rather than model-token counting
- no streaming responses
- no tracing or observability integration
- no web API or authentication
- no semantic memory or vector search

These limitations are intentional to preserve the project’s focused learning scope.

## Why This Project Matters

This repository demonstrates the essential lifecycle of a tool-using agent with persistent conversation state:

```text
User input
→ retained context
→ model reasoning
→ automatic tool selection
→ tool execution
→ final response
→ PostgreSQL persistence
```

The same foundation can later be extended with LangGraph, structured evaluation, streaming, tracing, semantic memory, and production deployment.

## License

MIT License.
