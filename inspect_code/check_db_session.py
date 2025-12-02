try:
    from google.adk.sessions import DatabaseSessionService
    print("Found DatabaseSessionService")
except ImportError:
    print("DatabaseSessionService NOT found")

try:
    import sqlalchemy
    print("Found sqlalchemy")
except ImportError:
    print("sqlalchemy NOT found")
