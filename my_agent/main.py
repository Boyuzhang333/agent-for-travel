from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .agent import root_agent


def main():
    runner = Runner(
        agent=root_agent,
        session_service=InMemorySessionService()
    )


if __name__ == "__main__":
    main()

