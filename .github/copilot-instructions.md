# Copilot Instructions for AI Agentic Engineering Course

## Project Overview

This is a comprehensive AI agents learning repository with 6 progressive modules teaching different agentic frameworks: Foundations (1_foundations), OpenAI Agents SDK (2_openai), CrewAI (3_crew), LangGraph (4_langgraph), AutoGen (5_autogen), and Model Context Protocol (6_mcp). Each module contains Jupyter notebooks, Python applications, and community contributions.

## Development Environment

- **Python Version**: 3.12+ (enforced in pyproject.toml)
- **Package Manager**: uv (primary), with fallback pip support
- **Environment**: Windows-first development (PowerShell), with Linux/Mac support
- **Notebooks**: Jupyter notebooks are the primary learning format

### Essential Setup Patterns

Always use `load_dotenv(override=True)` at the top of Python files - this is a universal pattern across all modules:

```python
from dotenv import load_dotenv
load_dotenv(override=True)
```

The `.env` file must be in the project root (`agents/`) with API keys:
- `OPENAI_API_KEY` (required for most modules)
- `PUSHOVER_TOKEN` and `PUSHOVER_USER` (for notifications)
- `GOOGLE_API_KEY` (for Gemini models)
- Various framework-specific keys

## Module Architecture

### 1_foundations/
- Entry point with `app.py` using Gradio UI pattern
- Tool functions with OpenAI function calling JSON schemas
- Push notification integration via Pushover API
- Pattern: Gradio apps with OpenAI client and custom tools

### 2_openai/
- Uses OpenAI Agents SDK (`openai-agents` package)
- Async patterns with `AsyncOpenAI` clients
- Complex agent workflows with function tools
- Pattern: Agent/Runner architecture with tracing

### 3_crew/
- CrewAI framework with crew/agent separation
- Use `crewai run` command for execution (not Python directly)
- Crew projects in subdirectories (debate/, coder/, etc.)
- Pattern: crews.py with agents and tasks definition

### 4_langgraph/
- LangGraph state machines with TypedDict states
- SQLite persistence with `langgraph-checkpoint-sqlite`
- Tool integration via `@tool` decorators
- Pattern: StateGraph with nodes and conditional edges

### 5_autogen/
- AutoGen Core with RoutedAgent base classes
- Message-based communication between agents
- Distributed agent patterns
- Pattern: Agent classes with message handlers

### 6_mcp/
- Model Context Protocol server implementations
- FastMCP for server creation
- Trading simulation with database persistence
- Pattern: MCP servers with tool definitions

## Common Development Patterns

### UI Applications
All modules use **Gradio** for web interfaces:
```python
import gradio as gr
with gr.Blocks() as ui:
    # UI components
ui.launch()
```

### Database Patterns
- SQLite databases for persistence (memory.db, tickets.db)
- Simple schema with manual SQL queries
- Database files typically in module root

### Tool Definition Pattern
OpenAI function calling tools follow this schema:
```python
tool_json = {
    "name": "function_name",
    "description": "Clear description",
    "parameters": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"],
        "additionalProperties": False
    }
}
```

### Error Handling
Minimal error handling - focus on educational clarity over production robustness. Use try/except mainly for external API calls.

## Framework-Specific Commands

### CrewAI
```bash
# Install CrewAI CLI tool
uv tool install crewai

# Create new crew project
crewai create crew <project_name>

# Run crew from project directory
crewai run
```

### LangGraph
```python
# Memory setup pattern
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("memory.db")
```

### MCP Servers
```python
# Server definition pattern
from mcp import FastMCP
server = FastMCP("server_name")

@server.tool()
def tool_function(args: ModelArgs):
    """Tool description"""
    return result
```

## File Structure Conventions

- `app.py` - Main Gradio application entry point
- Jupyter notebooks numbered by lab sequence (1_lab1.ipynb, 2_lab2.ipynb, etc.)
- `community_contributions/` - Student submissions and variations
- `sandbox/` - Experimental/testing area
- Output files typically in `output/` subdirectories

## Development Workflow

1. Always start with `load_dotenv(override=True)`
2. Use Jupyter notebooks for exploration and learning
3. Create Gradio UIs for interactive applications
4. Follow existing naming patterns in each module
5. Test with `uv run <script>` or Jupyter notebook execution
6. CrewAI projects use `crewai run` not direct Python execution

## Key Dependencies

Core packages across modules:
- `openai` - OpenAI API client
- `gradio` - Web UI framework
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests (often for Pushover notifications)
- Framework-specific: `crewai`, `langgraph`, `autogen-agentchat`, `mcp`

## Testing Patterns

Limited formal testing - use Jupyter notebooks and Gradio interfaces for manual testing. Focus on educational examples rather than comprehensive test coverage.