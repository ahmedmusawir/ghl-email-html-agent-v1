# Session 1: Initialization

- Initialized the project "GHL Email Template Workbench".
- Setup directory structure:
    - `progress_info/` for session logs.
    - `data/` for sample data.
- Created `requirements.txt` with dependencies:
    - streamlit
    - google-adk
    - beautifulsoup4
    - python-dotenv
- Created `tools.py` with core logic:
    - Implemented `apply_style_edit` using BeautifulSoup to safely parse and update inline CSS styles.
    - Added `update_text_content` for text replacement.
    - Replaced `insert_element` with `insert_element_relative` for precise positioning (`before`, `after`, `inside_start`, `inside_end`).
    - Added `update_inner_html` for rich text updates (parsing HTML strings into elements).
    - Added `remove_element` for deleting elements from the HTML tree.
    - Pivoted `__main__` testing strategy from Interactive CLI to JSON-based Test Harness.
    - This allows simulating AI Agent function calls via JSON payloads.
    - Verified functionality with `test_payload.json` successfully changing `h1` color.

# Session 2: Agent & UI Implementation

- **Agent Architecture (`agent.py`)**:
    - Defined `ghl_agent` using `google.adk.agents.Agent`.
    - Configured with `gemini-2.5-flash` model.
    - Registered wrapped tools from `tools.py`.
    - Implemented stateless execution pattern:
        - Agent receives full HTML context in every prompt.
        - Tool calls modify a global/session-based state in `tools.py`.
    - **ADK Runtime Integration**:
        - Implemented manual `Runner` execution loop using `google.adk.runners.Runner`.
        - Manually managed `InMemorySessionService` to handle session IDs and context.
        - Solved authentication challenges by injecting `google.genai.Client` configured with environment variables (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`) directly into the Agent.

- **Tooling Enhancements (`tools.py`)**:
    - Implemented global state management (`_active_html`, `set_active_html`, `get_active_html`) to bridge the stateless LLM and the stateful application.
    - Added robust logging (`🛠️ [TOOL EXEC]`) to visualize tool usage in the terminal.

- **Streamlit UI (`main.py`)**:
    - Built a chat interface for interacting with the agent.
    - Integrated an HTML preview pane and code view.
    - Implemented "Undo" functionality using a state stack.
    - Connected the UI to the `agent.run_agent` entry point.

- **Debugging & cleanup**:
    - Resolved Pydantic validation errors by properly injecting the Client into the Agent configuration.
    - Moved inspection scripts to `inspect_code/`.
    - Archived reference docs to `docs/`.
