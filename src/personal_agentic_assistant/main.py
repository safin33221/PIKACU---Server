
from langchain_core.messages import HumanMessage, SystemMessage

from personal_agentic_assistant.llm.provider import get_llm


SYSTEM_PROMPT = """
You are Pikachu, a personal AI assistant.

Your responsibilities:
- Help the user with programming, learning, planning, and daily tasks.
- Communicate naturally, politely, and clearly.
- Respond in Bangla when the user writes in Bangla.
- Be honest when you do not know something.
- Never claim to have executed an action unless it actually happened.
- Ask for explicit approval before performing consequential actions.
- Never expose API keys, passwords, or other secrets.

You are an assistant, not the account owner.
"""


def main() -> None:
    print("=" * 45)
    print("Pikachu Personal AI Assistant")
    print("Type 'exit' to quit.")
    print("=" * 45)

    try:
        llm = get_llm()
    except ValueError as error:
        print(f"Configuration error: {error}")
        return

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nPikachu: Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Pikachu: Goodbye!")
            break

        messages.append(HumanMessage(content=user_input))

        try:
            response = llm.invoke(messages)
            answer = response.content

            if isinstance(answer, str):
                print(f"\nPikachu: {answer}")
            else:
                print(f"\nPikachu: {answer}")

            messages.append(response)

        except Exception as error:
            # Remove the unanswered user message so the conversation
            # history remains valid for the next attempt.
            messages.pop()
            print(f"\nRequest failed: {error}")
            print("Check your API key, model name, and internet connection.")


if __name__ == "__main__":
    main()
