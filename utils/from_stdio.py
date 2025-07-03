from langchain_mcp_adapters.client import MultiServerMCPClient, ClientSession

async def get_tools_stdio():
    
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Replace with absolute path to your math_server.py file
                "args": ["F:/Letta/stdio_servers/math_server_stdio.py"],
                "transport": "stdio",
            },
        }
    )

    # "1. client = MultiServerMCPClient(...)\n"
    # "   tools = await client.get_tools()\n"
    # "2. client = MultiServerMCPClient(...)\n"
    # "   async with client.session(server_name) as session:\n"
    # "       tools = await load_mcp_tools(session)"

    return await client.get_tools()