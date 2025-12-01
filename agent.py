from google.adk.agents import Agent
from google.adk.runners import Runner, InMemoryRunner
from google.genai import types, Client
import tools
import asyncio
import uuid
import os

# Force Vertex AI usage via environment variable if not set
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"

# Define the Agent
ghl_agent = Agent(
    name="ghl_email_architect",
    model="gemini-2.5-flash", # As requested
    description="GHL Email Architect Agent",
    instruction="""You are a GHL Email Architect. Your mission is to surgically modify HTML templates.

PROTOCOL:
1. ANALYZE: Identify the specific elements the user wants to change (e.g., "the red button" -> `a[style*='red']`).
2. EXECUTE: Call the appropriate tool.
   - Use `apply_style_edit` for CSS changes.
   - Use `update_text_content` for simple text.
   - Use `update_inner_html` for rich text (bold, colors inside text).
   - Use `insert_element_relative` to add new items.
   - Use `remove_element` to delete items.
3. CHAINING: If the user asks for multiple changes, call multiple tools in sequence.
4. ERROR HANDLING: If a tool fails (returns "ERROR"), try a different selector or strategy.
5. CONFIRM: Briefly state what you changed (e.g., "Updated header color to blue.").

CRITICAL: Do NOT output raw HTML in your text response unless asked to explain. The tools handle the HTML updates.""",
    tools=[
        tools.apply_style_edit, 
        tools.update_text_content, 
        tools.update_inner_html, 
        tools.insert_element_relative, 
        tools.remove_element
    ]
)

from google.adk.sessions import InMemorySessionService

async def _run_async(user_input: str, html_context: str):
    # 1. Setup Session Service
    session_service = InMemorySessionService()
    
    # 2. Define Constants
    APP_NAME = "ghl_app"
    USER_ID = "user"
    SESSION_ID = str(uuid.uuid4())

    # 3. Create Session manually
    # Documentation says create_session is async
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # 4. Create Runner with app_name and session_service injected
    # Use base Runner class as per documentation pattern
    local_runner = Runner(
        agent=ghl_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # 5. Construct Prompt with HTML Context
    full_prompt = f"""
CONTEXT:
You are editing the following HTML file.
```html
{html_context}
```

USER REQUEST:
{user_input}
"""

    # 6. Run Async
    events = local_runner.run_async(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])
    )
    
    # Collect text response from events
    response_text = ""
    async for event in events:
        if hasattr(event, 'content') and event.content and event.content.parts:
             for part in event.content.parts:
                 if part.text:
                     response_text += part.text
    
    return response_text

def run_agent(user_input: str, current_html: str):
    # Step 1: Set active HTML context
    tools.set_active_html(current_html)
    
    # Step 2: Run the agent asynchronously
    response_text = asyncio.run(_run_async(user_input, current_html))
    
    # Step 3: Get the modified HTML
    new_html = tools.get_active_html()
    
    # Step 4: Return result
    return response_text, new_html
