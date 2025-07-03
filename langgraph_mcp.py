from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from utils.from_stdio import get_tools_stdio
from utils.from_http import get_tools_http
import asyncio

load_dotenv()

llm = ChatOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    model = "gpt-4.1-mini",
    temperature = 0,
)
#%%
# Method 1: Every Tool will create its own session

# tools = asyncio.run(get_tools_stdio())
# add_tool = tools[0]

# agent = create_react_agent(
#     model = llm,
#     tools = tools,
#     prompt = "You can use multiple tools in sequence to answer complex questions. Think step by step."
# )

# async def main():

#     input_message = "what's (3 + 5) x 12?"
#     async for step in agent.astream(
#         {"messages": [{"role": "user", "content": input_message}]},
#         stream_mode="values",
#     ):
#         step["messages"][-1].pretty_print()

    # res = await add_tool.ainvoke(input={"a": 3, "b": 5})
    # print(res)

# if __name__ == "__main__":
#     asyncio.run(main())

#%% 
# Method 2: Single session for all tools

# client = MultiServerMCPClient(
#     {
#         "math": {
#             "command": "python",
#             # Replace with absolute path to your math_server.py file
#             "args": ["F:/Letta/stdio_servers/math_server_stdio.py"],
#             "transport": "stdio",
#         },
#     }
# )

# async def main():

#     async with client.session('math') as session:

#         tools = await load_mcp_tools(session)

#         agent = create_react_agent(
#             model = llm,
#             tools = tools,
#             prompt = "You can use multiple tools in sequence to answer complex questions. Think step by step."
#         )

#         input_message = "what's (3 + 5) x 12?"

#         async for step in agent.astream(
#             {"messages": [{"role": "user", "content": input_message}]},
#             stream_mode="values",
#         ):
#             step["messages"][-1].pretty_print()

# if __name__ == "__main__":
#     asyncio.run(main())

#%%
# Wikipedia MCP Example

tools = asyncio.run(get_tools_http())

agent = create_react_agent(
    model = llm,
    tools = tools,
    prompt = "You can use multiple tools in sequence to answer complex questions. Think step by step."
)

async def main():

    input_message = "Find the article on the history of the Eiffel Tower in Wikipedia and summarize it."
    async for step in agent.astream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    asyncio.run(main())