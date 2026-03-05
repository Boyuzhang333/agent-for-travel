from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from my_agent.agent import root_agent

def main():
    runner = Runner(
        agent=root_agent,
        session_service=InMemorySessionService()
    )

    print("Travel agent ready.")

if __name__ == "__main__":
    main()