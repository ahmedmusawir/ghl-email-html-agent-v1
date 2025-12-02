from google.adk.tools import google_search
import inspect

print(f"Type: {type(google_search)}")
print(f"Dir: {dir(google_search)}")
try:
    print(f"Source: {inspect.getsource(google_search)}")
except:
    print("Cannot get source")
