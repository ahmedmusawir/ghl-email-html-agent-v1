from google.adk.models import Gemini
from pydantic import BaseModel

print("Gemini fields:")
for name, field in Gemini.model_fields.items():
    print(f"{name}: {field.annotation}")
