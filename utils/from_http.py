from langchain_mcp_adapters.client import MultiServerMCPClient, ClientSession
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

async def get_tools_http():

    config = {}
    
    config_b64 = base64.b64encode(json.dumps(config).encode())
    url = f"https://server.smithery.ai/@Rudra-ravi/wikipedia-mcp/mcp?config={config_b64}&api_key={os.getenv('SMITHERY_API_KEY')}"

    client = MultiServerMCPClient(
        {
            "wikipedia-mcp": {
                "url": url,
                "transport": "streamable_http",
            },
        }
    )

    # "1. client = MultiServerMCPClient(...)\n"
    # "   tools = await client.get_tools()\n"
    # "2. client = MultiServerMCPClient(...)\n"
    # "   async with client.session(server_name) as session:\n"
    # "       tools = await load_mcp_tools(session)"

    return await client.get_tools()