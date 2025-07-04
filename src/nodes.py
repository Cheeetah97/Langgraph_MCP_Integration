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
                "prompt": state['messages'][-1].content
            }
        )

async def agent_node(state) -> Command[Literal["__end__"]]:

    llm = _get_model(name = 'openai', 
                     temp = 0)

    tools = await get_tools_http()

    schema = {
        "title": "article_info",
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date on which the article was published."
            },
            "title": {
                "type": "string",
                "description": "A concise title in 7 to 8 words highlighting the crux of the article"
            },
            "summary": {
                "type": "string",
                "description": "A short paragraph summarizing the article in 2–3 sentences"
            },
            "url": {
                "type": "string",
                "description": "The direct URL to the original article"
            },
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Important keywords or phrases relevant to the article content"
            }
        },
        "required": ["date", "title", "summary", "url", "keywords"]
    }

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = "Use the tools provided to assist the User research on their topic",
        response_format = schema
    )

    async for step in agent.astream(
        {"messages": [{"role": "user", "content": state['prompt']}]},
        stream_mode = "values",
    ):
        # step["messages"][-1].pretty_print()
        if step.get("structured_response", None) is not None:
            structured_output = step.get("structured_response", None)

    return Command(
            goto = "__end__", 
            update = {
                "messages": AIMessage(content = f'Output = {structured_output}')
            }
        )