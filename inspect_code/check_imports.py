try:
    from google.tools import google_search
    print("Found google.tools.google_search")
except ImportError:
    print("google.tools.google_search NOT found")

try:
    from google.adk.tools import google_search
    print("Found google.adk.tools.google_search")
except ImportError:
    print("google.adk.tools.google_search NOT found")
