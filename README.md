# SSB Bank MCP POC

Flow: Mock SSB banking APIs (4 endpoints) -> FastMCP (streamable HTTP) -> LangGraph agent

This POC uses fictional demo accounts and transactions only. It is not connected
to SSB or any production banking system. The transfer tool only checks a simulated
transfer; it never moves money.

Available tools:

- `get_account`: account type, currency, and status
- `get_account_balance`: current mock balance
- `list_account_transactions`: recent mock transactions
- `simulate_transfer`: validate a transfer without executing it

Demo account IDs: `SSB-1001`, `SSB-1002`, `SSB-2001`.

    pip install -r requirements.txt

Create a `.env` file with your Google AI API key:

    GOOGLE_API_KEY=your-google-api-key

The agent uses Gemini `gemini-3.5-flash-lite` by default. To select a different
Gemini model, optionally add `AGENT_MODEL=your-gemini-model` to `.env`.

    python mcp_server.py               # terminal 1  (http://127.0.0.1:8001/mcp)
    python test_mcp.py                 # terminal 2  quick check, no LLM
    python agent.py                    # terminal 2  full agent run

Watch terminal 1: each tool call from the agent is logged.
In the agent output, [MCP RESULT] lines are what the MCP server returned.

Optional: `uvicorn api_app:app --port 8000` then open /docs to see the mock banking APIs.
