
from typing import TypedDict


class AgentState(TypedDict):
    user_input: str
    plan: str
    requires_approval: bool
    approved: bool
    response: str
