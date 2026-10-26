"""No-LLM smoke test: call each SSB banking MCP tool directly."""
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8001/mcp") as c:
        tools = await c.list_tools()
        print("tools:", [tool.name for tool in tools])
        print(await c.call_tool("get_account", {"account_id": "SSB-1001"}))
        print(await c.call_tool("get_account_balance", {"account_id": "SSB-1001"}))
        print(await c.call_tool("list_account_transactions", {"account_id": "SSB-1001", "limit": 5}))
        print(await c.call_tool("simulate_transfer", {
            "source_account_id": "SSB-1001",
            "destination_account_id": "SSB-2001",
            "amount": 1000,
        }))

asyncio.run(main())
