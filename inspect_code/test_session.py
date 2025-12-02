import asyncio
import uuid
import os
from google.adk.sessions import InMemorySessionService

# Mock environment
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"

async def test_session_logic():
    print("--- Testing Session Logic ---")
    session_service = InMemorySessionService()
    app_name = "ghl_app"
    user_id = "user"
    session_id = str(uuid.uuid4())
    
    print(f"1. Trying to get non-existent session: {session_id}")
    try:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print(f"   SUCCESS: Found session: {session}")
        if session is None:
            print("   WARNING: Session is None")
    except Exception as e:
        print(f"   CAUGHT EXPECTED ERROR: {e}")
        
    print(f"2. Creating session: {session_id}")
    try:
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print("   SUCCESS: Created session")
    except Exception as e:
        print(f"   ERROR Creating Session: {e}")
        
    print(f"3. Getting created session: {session_id}")
    try:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print(f"   SUCCESS: Found session object: {session}")
    except Exception as e:
        print(f"   ERROR Getting Session: {e}")

if __name__ == "__main__":
    asyncio.run(test_session_logic())
