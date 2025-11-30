import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types


try:
    from Travel_assistant_agent.agent import root_agent
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure you are running from the project root and that the 'Travel_assistant_agent' folder contains an __init__.py")
    sys.exit(1)

async def main():
    """Run the agent and simulate a user query flow."""
    
    print("🚀 Initializing travel planning agent test...")

    
    session_service = InMemorySessionService()
    app_name = "travel_app"
    user_id = "test_traveler"
    session_id = "session_001"
      
    await session_service.create_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id
    )

 
    runner = Runner(
        agent=root_agent, 
        app_name=app_name, 
        session_service=session_service
    )

   
 
    queries = [
        "Please plan a 7-day trip from downtown Seattle to Salem, Massachusetts, with a budget of $5,000. I want to visit historical sites related to the witch trials, and I also love seafood.",
        # "Looks great, thanks for the plan!" # Optional second-round dialogue
    ]

    print(f"✅ Agent loaded: {root_agent.name}")
    print("----------------------------------------------------------------")

  
    for query in queries:
        print(f"\n🔵 [User]: {query}")
        print("⚪ [System]: Agent is thinking and calling tools... (this may take a few seconds)")
        

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=genai_types.Content(
                role="user", 
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):


            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text
                print(f"\n🟢 [Agent]:\n{response_text}")

if __name__ == "__main__":


    asyncio.run(main())