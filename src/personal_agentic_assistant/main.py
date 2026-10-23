
from personal_agentic_assistant.agents.graph import agent
from uuid import uuid4

from langgraph.types import Command




def main() -> None:
    print("=" * 45)
    print("Pikachu Personal AI Assistant")
    print("Type 'exit' to quit.")
    print("=" * 45)

    # One thread per terminal session.
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

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

        initial_state = {
            "user_input": user_input,
            "plan": "",
            "requires_approval": False,
            "approved": False,
            "response": "",
        }

        try:
            result = agent.invoke(initial_state, config=config)

            if result.get("__interrupt__"):
                interrupt_data = result["__interrupt__"][0].value

                print("\nPikachu's proposed plan:")
                print(interrupt_data["plan"])

                choice = input(
                    "\nApprove? (yes/no): "
                ).strip().lower()

                approved = choice in {"yes", "y"}

                result = agent.invoke(
                    Command(resume={"approved": approved}),
                    config=config,
                )

            print(f"\nPikachu: {result['response']}")

        except Exception as error:
            print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
