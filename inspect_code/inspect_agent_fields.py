from google.adk.agents import Agent
from pydantic import BaseModel

print("Agent fields:")
for name, field in Agent.model_fields.items():
    print(f"{name}: {field.annotation}")
