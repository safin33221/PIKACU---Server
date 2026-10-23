
from personal_agentic_assistant.agents.nodes import approval_node
from personal_agentic_assistant.agents.nodes import planner_node
from personal_agentic_assistant.agents.state import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph




def route_after_planning(state: AgentState) -> str:
    if state["requires_approval"]:
        return "approval"
    return END


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("approval", approval_node)

    workflow.add_edge(START, "planner")

    workflow.add_conditional_edges(
        "planner",
        route_after_planning,
        {
            "approval": "approval",
            END: END,
        },
    )

    workflow.add_edge("approval", END)

    checkpointer = InMemorySaver()

    return workflow.compile(checkpointer=checkpointer)


agent = build_graph()
