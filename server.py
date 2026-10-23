
from fastmcp import FastMCP

mcp = FastMCP("SSB-MCP-POC")


@mcp.tool()
def create_account_request(
    customer_id: str,
    account_type: str,
) -> dict:
    """Call the local mock account API."""
    import httpx

    response = httpx.post(
        "http://127.0.0.1:8000/acctservice/acctmgmt/accounts",
        json={
            "customer_id": customer_id,
            "account_type": account_type,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_account(customer_id: str) -> dict:
    """Fetch account details for a customer ID."""
    import httpx

    response = httpx.get(
        f"http://127.0.0.1:8000/acctservice/acctmgmt/accounts/{customer_id}",
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    mcp.run(transport="streamable-http",port=8001)
