from langgraph.graph import MessagesState
from typing import Optional

class GraphState(MessagesState):
    prompt: str