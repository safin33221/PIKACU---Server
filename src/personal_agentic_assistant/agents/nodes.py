
from personal_agentic_assistant.agents.state import AgentState
from langgraph.types import interrupt


from personal_agentic_assistant.llm.provider import get_llm


PLANNER_PROMPT = """
You are Pikachu, a personal AI assistant.

Classify the user's request.

For normal questions and conversation, respond:
TYPE: CHAT
CONTENT: your answer

For requests to perform an action, such as creating or modifying
files, sending messages, deleting data, or running commands, respond:
TYPE: ACTION
CONTENT: a short plan describing the intended action

Do not claim that an action has been executed.
Use Bangla when the user writes in Bangla.
Return the TYPE and CONTENT lines clearly.
"""


def planner_node(state: AgentState) -> dict:
    llm = get_llm()
    result = llm.invoke(
        f"{PLANNER_PROMPT}\n\nUser request:\n{state['user_input']}"
    )

    content = str(result.content).strip()
    lines = content.splitlines()

    type_line = next(
        (line.strip().upper() for line in lines
         if line.strip().upper().startswith("TYPE:")),
        "",
    )

    requires_approval = type_line == "TYPE: ACTION"

    content_index = next(
        (i for i, line in enumerate(lines)
         if line.strip().upper().startswith("CONTENT:")),
        None,
    )

    if content_index is not None:
        first_content = lines[content_index].split(":", 1)[1].strip()
        plan = "\n".join(
            [first_content] + lines[content_index + 1:]
        ).strip()
    else:
        plan = content

    return {
        "plan": plan,
        "requires_approval": requires_approval,
        "approved": False,
        "response": plan,
    }


def approval_node(state: AgentState) -> dict:
    decision = interrupt({
        "type": "approval_required",
        "plan": state["plan"],
        "message": "Approve this plan before execution?",
    })

    approved = (
        isinstance(decision, dict)
        and decision.get("approved") is True
    )

    if approved:
        response = (
            "Plan approved. No external action has been executed yet."
        )
    else:
        response = "Plan rejected. No action was performed."

    return {
        "approved": approved,
        "response": response,
    }
