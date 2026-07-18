from langchain_core.messages import trim_messages

from agent import agent
from database import (
    clear_messages,
    initialize_database,
    load_messages,
    save_message,
)


def main() -> None:
    initialize_database()

    session_id = input("Enter session ID: ").strip()

    if not session_id:
        session_id = "default-session"

    messages = load_messages(session_id)

    print("Simple LangChain Agent")
    print("Type 'exit' to stop or '/clear' to clear this session.")
    print(f"Session: {session_id}")
    print(f"Loaded {len(messages)} saved messages.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAgent: Goodbye!")
            break

        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break

        if user_input.lower() == "/clear":
            clear_messages(session_id)
            messages = []

            print("Agent: Current session history cleared.\n")
            continue

        if not user_input:
            print("Agent: Please enter a message.\n")
            continue

        user_message = {
            "role": "user",
            "content": user_input,
        }

        messages.append(user_message)

        try:
            trimmed_messages = trim_messages(
                messages,
                strategy="last",
                token_counter=len,
                max_tokens=20,
                start_on="human",
                include_system=True,
            )

            result = agent.invoke(
                {
                    "messages": trimmed_messages,
                }
            )

            final_message = result["messages"][-1]
            assistant_content = str(final_message.content)

            save_message(
                session_id,
                "user",
                user_input,
            )

            save_message(
                session_id,
                "assistant",
                assistant_content,
            )

            messages = load_messages(session_id)

            print(f"Agent: {assistant_content}\n")

        except Exception as error:
            messages.pop()

            print(f"Agent error: {error}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()