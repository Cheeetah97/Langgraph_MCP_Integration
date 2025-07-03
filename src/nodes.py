import asyncio
from langgraph.types import Command
from langchain_core.messages import AIMessage
from typing import Literal
from langgraph.prebuilt import create_react_agent
from utils.utilities import _get_model
from utils.from_http import get_tools_http

def prompt_node(state) -> Command[Literal["agent"]]:

    return Command(
            goto = "agent", 
            update = {
                "prompt": state['messages'][-1]
            }
        )

def agent_node(state) -> Command[Literal["__end__"]]:

    llm = _get_model(name = 'openai', 
                         temp = 0)

    tools = asyncio.run(get_tools_http())

    schema = {
        "title": "article_info",
        "type": "object",
        "properties": {
            "date": {
                "type": "object",
                "type": "string",
                "description": "A list of 2 to 4 Unordered Bullet points for the Slide"
            },
            "bullets": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of 2 to 4 Unordered Bullet points for the Slide"
            }
        },
        "required": ["bullets"]
    }

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = "You can use multiple tools in sequence to answer complex questions. Think step by step."
    )

    return Command(
            goto = "__end__", 
            update = {
                "messages": state['messages'][-1]
            }
        )