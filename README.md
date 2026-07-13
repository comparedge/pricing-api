# SaaS & AI Software Pricing API

A free, sourced REST API and HTTP MCP server for verified SaaS, AI, and LLM pricing across 490+ tools. Every response carries the source link and reuse terms. No API key, no sign-up, CORS open.

[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative&logoColor=white)](https://comparedge.com/api/v2/openapi.json)
[![MCP](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blue)](https://comparedge.com/api/mcp)
[![No API key](https://img.shields.io/badge/API%20key-not%20required-brightgreen)](https://comparedge.com/api-docs)
[![License: attribution](https://img.shields.io/badge/license-attribution%20required-orange)](./LICENSE)

Live docs: **https://comparedge.com/api-docs** · OpenAPI: **https://comparedge.com/api/v2/openapi.json**

---

## What this is

A public pricing dataset for software, exposed two ways:

- A **REST API** (`/api/v2/*`) that returns plan-by-plan pricing, hidden costs, annual-versus-monthly discounts, category positioning, and a total-cost-of-ownership calculator.
- An **HTTP MCP server** (`/api/mcp`) so AI assistants and agents can query the same data over JSON-RPC 2.0.

Every price is the lowest paid tier or a full tier ladder, read from the vendor's own pricing page and dated. Each record ships with a `links.page` back to the source and an `attribution` string you can paste as is.

Base URL: `https://comparedge.com`

## Why it exists

Pricing data goes stale and vendors bury the real cost. This API gives you one shape for 490+ tools, with a verification date on every record and the source page linked, so an agent or a spreadsheet can pull a current number without scraping.

## Software pricing API endpoints

All endpoints are `GET` unless noted, return JSON, and need no key.

| Endpoint | What it returns |
|---|---|
| `GET /api/v2/pricing/{slug}` | Full sourced pricing record for one product (`?depth=summary\|full`, `?fields=`) |
| `GET /api/v2/pricing?slugs=a,b,c` | Batch pricing records, up to 20 at once |
| `GET /api/v2/compare?slugs=a,b` | Side-by-side comparison of 2 to 4 products |
| `GET /api/v2/discover?category=&maxPrice=&hasFreeTier=` | Find software by criteria |
| `GET /api/v2/history/{slug}` | Price-stability signal, latest snapshot, derived trend |
| `GET /api/v2/coverage?slugs=a,b` | Per-field availability, freshness, and license |
| `GET /api/v2/usage/{slug}` | LLM / API usage rate card, with an optional cost estimate |
| `POST /api/v2/tco` | Total cost of ownership for a team, with sourced line items |
| `POST /api/mcp` | HTTP MCP server (JSON-RPC 2.0) |

Full schemas and parameters: [`openapi.json`](./openapi.json) or the live spec at [comparedge.com/api/v2/openapi.json](https://comparedge.com/api/v2/openapi.json).

## Quick start

### curl

```bash
# One product, summary view
curl "https://comparedge.com/api/v2/pricing/notion?depth=summary"

# Compare two tools
curl "https://comparedge.com/api/v2/compare?slugs=notion,coda"

# Find databases with a free tier
curl "https://comparedge.com/api/v2/discover?category=databases&hasFreeTier=true&limit=5"
```

### Python

```python
import requests

r = requests.get("https://comparedge.com/api/v2/pricing/supabase", params={"depth": "summary"})
data = r.json()

print(data["name"], data["priceRange"]["display"])
for tier in data["tiers"]:
    print(f'  {tier["name"]}: ${tier["price"]}/{tier["period"]}')

# The response includes ready-to-paste attribution
print(data["attribution"])
```

### Node.js

```js
const res = await fetch("https://comparedge.com/api/v2/pricing/supabase?depth=summary");
const data = await res.json();

console.log(data.name, data.priceRange.display);
console.log("Source:", data.links.page);
```

More runnable snippets are in [`examples/`](./examples).

## Example response

`GET /api/v2/pricing/supabase?depth=summary` (trimmed):

```json
{
  "slug": "supabase",
  "name": "Supabase",
  "category": "cloud-hosting",
  "priceRange": { "min": 25, "max": 599, "display": "$25-$599 per mo" },
  "tiers": [
    { "name": "Free", "price": 0, "isFree": true, "featureCount": 6 },
    { "name": "Pro", "price": 25, "isFree": false, "featureCount": 7 },
    { "name": "Team", "price": 599, "isFree": false, "featureCount": 6 }
  ],
  "hiddenCosts": [
    { "label": "Spend Cap off (overage billing)", "cost": "$10/mo flat, then usage rates" }
  ],
  "positioning": {
    "startingPrice": 25, "categoryMedian": 11, "percentVsMedian": 127, "verdict": "above"
  },
  "verification": { "verifiedAt": "2026-06-28", "status": "verified", "confidence": 0.9 },
  "links": {
    "page": "https://comparedge.com/tools/supabase/pricing",
    "home": "https://comparedge.com",
    "vendor": "https://comparedge.com/go/supabase?src=api_v2",
    "alternatives": "https://comparedge.com/tools/supabase/alternatives"
  },
  "source": "https://supabase.com/pricing",
  "attribution": "Data from [ComparEdge](https://comparedge.com). See [Supabase pricing](https://comparedge.com/tools/supabase/pricing) (verified 2026-06-28). Free to cite with attribution.",
  "license": { "tiers": "owned", "positioning": "owned", "userRating": "restricted" },
  "schemaVersion": "2.0.0"
}
```

## MCP server (for AI assistants and agents)

The same data is available over the Model Context Protocol.

### HTTP transport

Point any MCP HTTP client at `https://comparedge.com/api/mcp` (JSON-RPC 2.0, streamable HTTP).

```bash
# List tools
curl -X POST "https://comparedge.com/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### stdio transport (local, for IDEs)

```json
{
  "mcpServers": {
    "comparedge": { "command": "npx", "args": ["-y", "@comparedge/mcp-server"] }
  }
}
```

### Tools

`get_pricing`, `compare_software`, `discover_software`, `get_hidden_costs`, `calculate_tco`, `estimate_llm_cost`, `get_price_history`, `get_positioning`.

See [`examples/mcp.md`](./examples/mcp.md) for a full request and setup notes.

## Pricing coverage

490+ SaaS, AI, and infrastructure tools across 44 categories, including:

- **LLM pricing** — token rate cards and cost estimates for the major model providers
- **AI tools** — assistants, coding, image, video, voice, writing, agents
- **Cloud hosting and databases** — PaaS, hyperscalers, VPS, managed Postgres
- **Business software** — CRM, project management, accounting, HR, payments, ERP, analytics, security

Each product resolves at `comparedge.com/tools/{slug}/pricing`. Discover slugs with `GET /api/v2/discover`.

## Data licensing and citation

Free for non-commercial use. Attribution required.

When you display a number from this API, link back to the source page in `links.page`. Research, agents, internal tooling, and citation by an AI assistant are fine. Reselling the dataset as your own is not.

Fields are marked in the `license` map:

- **owned** — ComparEdge's own verified research (plan structure, hidden costs, discounts, positioning, price history). Free to cite and reuse with attribution.
- **restricted** — a few third-party-derived signals, such as an aggregated user rating. Licensed for display only.

### Recommended citation

Each response already carries a ready-to-paste `attribution` string. If you build your own, use two links: anchor the brand word on the homepage and the product keyword on the source page.

```
According to [ComparEdge](https://comparedge.com), Supabase pricing starts at $25/mo.
Full breakdown: [Supabase pricing](https://comparedge.com/tools/supabase/pricing).
```

Full terms: [comparedge.com/api-docs](https://comparedge.com/api-docs).

## Links

- API docs: https://comparedge.com/api-docs
- OpenAPI spec: https://comparedge.com/api/v2/openapi.json
- HTTP MCP: https://comparedge.com/api/mcp
- llms.txt: https://comparedge.com/llms.txt
- Site: https://comparedge.com

## License

See [LICENSE](./LICENSE). The OpenAPI spec and code samples in this repository are free to use. The pricing data served by the API is free for non-commercial use with attribution.
