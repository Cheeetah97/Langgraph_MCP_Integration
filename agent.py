from langgraph.graph import StateGraph
from src.state import GraphState
from src.nodes import prompt_node, agent_node

# Agent
workflow = StateGraph(GraphState)
workflow.add_node("prompt_understanding",prompt_node)
workflow.add_node("agent",agent_node)
workflow.set_entry_point("prompt_understanding")
agent = workflow.compile()