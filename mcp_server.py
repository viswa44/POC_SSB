"""SSB Bank POC MCP server: converts the banking FastAPI app into MCP tools.
Transport: streamable HTTP at http://127.0.0.1:8001/mcp (no stdio)."""
import logging, time
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware
from starlette.responses import PlainTextResponse
from POC_SSB.api_app import app as banking_api

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("mcp")


class ToolLogger(Middleware):
    """Logs each tool call so you can watch the agent hitting the server."""
    async def on_call_tool(self, context, call_next):
        name, args = context.message.name, context.message.arguments
        start = time.perf_counter()
        log.info("CALL  %s args=%s", name, args)
        try:
            result = await call_next(context)
            log.info("OK    %s (%.0f ms)", name, (time.perf_counter() - start) * 1000)
            return result
        except Exception as e:
            log.error("FAIL  %s: %s", name, e)
            raise


mcp = FastMCP.from_fastapi(app=banking_api, name="SSB Bank MCP Server")
mcp.add_middleware(ToolLogger())


@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    return PlainTextResponse("ok")


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)
