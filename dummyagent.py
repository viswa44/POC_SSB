
import asyncio
from fastmcp import Client


MCP_URL = "http://127.0.0.1:8001/mcp"


async def main():
    print("SSB Dummy Account Agent")
    print("1. Create account request")
    print("2. Get account details")

    choice = input("Choose an option (1/2): ").strip()
    customer_id = input("Enter customer ID: ").strip()

    async with Client(MCP_URL) as client:
        if choice == "1":
            account_type = input("Enter account type: ").strip()

            result = await client.call_tool(
                "create_account_request",
                {
                    "customer_id": customer_id,
                    "account_type": account_type,
                },
            )

        elif choice == "2":
            result = await client.call_tool(
                "get_account",
                {"customer_id": customer_id},
            )

        else:
            print("Invalid option.")
            return

        print("\nMCP tool result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
