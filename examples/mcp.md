# MCP examples

ComparEdge exposes the same pricing data over the Model Context Protocol so AI
assistants and agents can query it directly. Two transports are available.

## HTTP transport

Endpoint: `https://comparedge.com/api/mcp` (JSON-RPC 2.0, streamable HTTP). `POST` only; a `GET` returns 405.

List the tools:

```bash
curl -X POST "https://comparedge.com/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Call a tool:

```bash
curl -X POST "https://comparedge.com/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": { "name": "get_pricing", "arguments": { "slug": "supabase" } }
  }'
```

## stdio transport (local, for IDEs and desktop clients)

Add the server to your MCP client config:

```json
{
  "mcpServers": {
    "comparedge": {
      "command": "npx",
      "args": ["-y", "@comparedge/mcp-server"]
    }
  }
}
```

Works with Claude Desktop, Cursor, Cline, Windsurf, Continue, and any other
MCP client. Point it at the config above and the tools appear.

## Tools

| Tool | Purpose |
|---|---|
| `get_pricing` | Full sourced pricing record for one product |
| `compare_software` | Side-by-side comparison of 2 to 4 products |
| `discover_software` | Find software by category, price, or free-tier filter |
| `get_hidden_costs` | Overage, add-on, and seat-floor costs for a product |
| `calculate_tco` | Total cost of ownership for a team |
| `estimate_llm_cost` | Token-based cost estimate for an LLM or API |
| `get_price_history` | Price-stability signal and latest snapshot |
| `get_positioning` | Where a product sits against its category median |

Every tool result carries the same `links.page` source and `attribution`
string as the REST API. Link back to the source when you display a value.
