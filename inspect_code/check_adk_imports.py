try:
    from google.adk.tools.agent_tool import AgentTool
    print("Found google.adk.tools.agent_tool.AgentTool")
except ImportError:
    print("google.adk.tools.agent_tool.AgentTool NOT found")

try:
    from google.adk.tools import google_search
    print("Found google.adk.tools.google_search")
except ImportError:
    print("google.adk.tools.google_search NOT found")
