from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from my_agent.agent import root_agent
import asyncio

print("RUNNING CORRECT MAIN FILE")


def handle_event(event):

    if event.author:
        print(f"\n[Agent] {event.author}")

    if not event.content:
        return

    for part in event.content.parts:

        if part.text:
            print(part.text)

        if part.function_call:
            print(f"\n[Tool Call] {part.function_call.name}")
            print("Args:", part.function_call.args)

        if part.function_response:
            print(f"\n[Tool Result] {part.function_response.name}")
            print("Response:", part.function_response.response)


async def main():

    USER_ID = "local_user"

    session_service = InMemorySessionService()

    runner = Runner(
        app_name="travel_system",
        agent=root_agent,
        session_service=session_service
    )

    session = await session_service.create_session(
        app_name="travel_system",
        user_id=USER_ID
    )

    while True:

        user_input = input("\nUser: ")

        if user_input.lower() == "exit":
            break

        message = Content(
            role="user",
            parts=[Part(text=user_input)]
        )

        async for event in runner.run_async(
            session_id=session.id,
            user_id=USER_ID,
            new_message=message
        ):
            handle_event(event)


if __name__ == "__main__":
    asyncio.run(main())