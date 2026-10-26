import asyncio
import os
import sys

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

MODEL = os.getenv("AGENT_MODEL", "gemini-3.5-flash-lite")
EXIT_WORDS = {"exit", "quit"}

SYSTEM_PROMPT = (
    "You are the assistant for the SSB Bank proof of concept. All account and "
    "transaction data is fictional mock data. Use the available tools to answer "
    "questions about demo accounts, balances, and transactions. Transfer requests "
    "can only be simulated; never claim that money was moved. Never ask for "
    "passwords, PINs, one-time codes, or full payment credentials. If a tool "
    "doesn't have the information, say so instead of guessing."
)


def as_text(content):
    """Gemini returns a list of blocks; this pulls out just the text."""
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content
                   if isinstance(b, dict) and b.get("type") == "text")


def show_new_messages(messages):
    """Print the tool calls, MCP results and final answer for this turn."""
    for m in messages:
        if m.type == "ai" and getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                print(f"  [AI -> tool] {tc['name']}  args={tc['args']}")
        elif m.type == "tool":
            print(f"  [MCP RESULT] {m.name}: {as_text(m.content)[:300]}")
        elif m.type == "ai":
            print(f"\nAssistant: {as_text(m.content)}\n")


async def main():
    client = MultiServerMCPClient({
        "mcp_poc": {"url": "http://127.0.0.1:8001/mcp", "transport": "streamable_http"}})
    tools = await client.get_tools()
    print("Connected to SSB Bank MCP Server. Tools:", [t.name for t in tools])

    llm = ChatGoogleGenerativeAI(model=MODEL)
    agent = create_agent(llm, tools=tools, system_prompt=SYSTEM_PROMPT)

    print("\nSSB Bank POC chat ready. Type your question, or 'exit' / 'quit' to stop.\n")
    history = []  # keeps the conversation so follow-up questions work

    while True:
        try:
            user_input = (await asyncio.to_thread(input, "You: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in EXIT_WORDS:
            print("Bye!")
            break

        history.append(("user", user_input))
        try:
            result = await agent.ainvoke({"messages": history})
        except Exception as e:
            print(f"\n[Error] {e}\n")
            history.pop()  # drop the failed question so the chat can continue
            continue

        show_new_messages(result["messages"][len(history):])
        history = result["messages"]


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())