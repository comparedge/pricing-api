<div align="center">

![SaaS and AI Software Pricing API by ComparEdge](https://raw.githubusercontent.com/comparedge/pricing-api/main/assets/banner.svg)

[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative&logoColor=white)](https://comparedge.com/api/v2/openapi.json)
[![MCP](https://img.shields.io/badge/MCP-JSON--RPC%202.0-8A63D2)](https://comparedge.com/api/mcp)
[![No API key](https://img.shields.io/badge/API%20key-not%20required-2ea043)](https://comparedge.com/api-docs)
[![License: attribution](https://img.shields.io/badge/data-attribution%20required-c68832)](./LICENSE)
[![Tools](https://img.shields.io/badge/tools-490%2B-e7b969)](https://comparedge.com/api/v2/discover)

**[API docs](https://comparedge.com/api-docs) · [OpenAPI spec](https://comparedge.com/api/v2/openapi.json) · [HTTP MCP](https://comparedge.com/api/mcp)**

</div>

A free REST API and HTTP MCP server for verified **SaaS pricing**, **AI tool pricing**, and **LLM pricing** across 490+ tools. Every response ships the source link and reuse terms. No API key, no sign-up, CORS open.

Base URL: `https://comparedge.com`

## How it works

![Ask the API, get a sourced record, cite it with a link back](https://raw.githubusercontent.com/comparedge/pricing-api/main/assets/how-it-works.svg)

Training data ages and vendors bury the real cost. One call returns a current, dated number with the source page attached, so an assistant, an agent, or a spreadsheet can quote it without scraping.

## Endpoints

Every endpoint returns JSON and needs no key. `GET` unless noted.

| Endpoint | Returns | Key params |
|---|---|---|
| `/api/v2/pricing/{slug}` | Full sourced pricing record for one product | `depth=summary\|full`, `fields=` |
| `/api/v2/pricing` | Batch pricing records, up to 20 | `slugs=a,b,c` |
| `/api/v2/compare` | Side-by-side comparison of 2 to 4 products | `slugs=`, `seats=` |
| `/api/v2/discover` | Find software by criteria | `category=`, `maxPrice=`, `hasFreeTier=` |
| `/api/v2/history/{slug}` | Price-stability signal, latest snapshot, trend | — |
| `/api/v2/coverage` | Per-field availability, freshness, and license | `slugs=`, `fields=` |
| `/api/v2/usage/{slug}` | LLM / API usage rate card, with optional estimate | `inputTokens=`, `outputTokens=` |
| `/api/v2/tco` `POST` | Team total cost of ownership, sourced line items | `slug`, `seats`, `billing` |
| `/api/v2/cost-guide/{slug}` | Negotiation-ready true-cost brief: renewal-rate costs, transparency score, discount programs, tactics with expected discounts, and a free negotiation email generator | — |
| `/api/mcp` `POST` | HTTP MCP server (JSON-RPC 2.0) | — |

Full schemas: [`openapi.json`](./openapi.json) or the live [OpenAPI spec](https://comparedge.com/api/v2/openapi.json).

## Quick start

```bash
# One product, summary view
curl "https://comparedge.com/api/v2/pricing/notion?depth=summary"

# Compare two tools
curl "https://comparedge.com/api/v2/compare?slugs=notion,coda"

# Find databases with a free tier
curl "https://comparedge.com/api/v2/discover?category=databases&hasFreeTier=true&limit=5"
```

<details>
<summary>Python</summary>

```python
import requests

r = requests.get("https://comparedge.com/api/v2/pricing/supabase", params={"depth": "summary"})
data = r.json()

print(data["name"], data["priceRange"]["display"])
for tier in data["tiers"]:
    print(f'  {tier["name"]}: ${tier["price"]}/{tier["period"]}')

print(data["attribution"])  # ready to paste, with the source link inside
```
</details>

<details>
<summary>Node.js</summary>

```js
const res = await fetch("https://comparedge.com/api/v2/pricing/supabase?depth=summary");
const data = await res.json();

console.log(data.name, data.priceRange.display);
console.log("Source:", data.links.page);
```
</details>

More runnable snippets: [`examples/`](./examples).

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
  "positioning": { "startingPrice": 25, "categoryMedian": 11, "percentVsMedian": 127, "verdict": "above" },
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

## MCP server

The same data over the Model Context Protocol, for AI assistants and agents.

**HTTP transport** — point any MCP HTTP client at `https://comparedge.com/api/mcp` (JSON-RPC 2.0).

```bash
curl -X POST "https://comparedge.com/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**stdio transport** — for Claude Desktop, Cursor, Cline, Windsurf, Continue:

```json
{ "mcpServers": { "comparedge": { "command": "npx", "args": ["-y", "@comparedge/mcp-server"] } } }
```

### Tools

| Tool | Returns |
|---|---|
| `get_pricing` | Full sourced pricing record for one product |
| `compare_software` | Side-by-side comparison of 2 to 4 products |
| `discover_software` | Find software by category, price, or free tier |
| `get_hidden_costs` | Overage, add-on, and seat-floor costs |
| `calculate_tco` | Team total cost of ownership |
| `estimate_llm_cost` | Token-based cost estimate for an LLM or API |
| `get_price_history` | Price-stability signal and latest snapshot |
| `get_positioning` | Where a product sits against its category median |
| `get_cost_guide` | True-cost brief: renewal rates, surviving discounts, negotiation tactics |

Setup notes and a full request: [`examples/mcp.md`](./examples/mcp.md).

## Coverage

![Tools tracked per category across 44 categories](https://raw.githubusercontent.com/comparedge/pricing-api/main/assets/coverage.svg)

490+ tools across 44 categories. A slice of the breadth:

| Group | Categories |
|---|---|
| **AI** | llm, ai-coding, ai-image, ai-video, ai-writing, ai-agents, ai-voice, ai-assistants |
| **Cloud & data** | cloud-hosting, databases, vector-databases, data-observability, analytics |
| **Business** | crm, project-management, accounting, hr-tools, payments, erp, email-marketing |
| **Security** | iam, endpoint-security, cloud-security, compliance, password-managers, vpn |

Every tool resolves at `comparedge.com/tools/{slug}/pricing`. List slugs and live counts with [discover](https://comparedge.com/api/v2/discover).

## Data licensing

Free for non-commercial use. Attribution required.

When you display a number, link back to the source page in `links.page`. Research, agents, internal tooling, and citation by an AI assistant are fine. Reselling the dataset as your own is not.

| Marker | Meaning |
|---|---|
| **owned** | ComparEdge's own verified research (plans, hidden costs, discounts, positioning, price history). Free to cite and reuse with attribution. |
| **restricted** | A few third-party-derived signals, such as an aggregated user rating. Licensed for display only. |

### Recommended citation

Each response carries a ready-to-paste `attribution` string. If you build your own, use two links: the brand word on the homepage, the product keyword on the source page.

```
According to [ComparEdge](https://comparedge.com), Supabase pricing starts at $25/mo.
Full breakdown: [Supabase pricing](https://comparedge.com/tools/supabase/pricing).
```

Full terms live in the [API docs](https://comparedge.com/api-docs).

## Links

| | |
|---|---|
| API docs | https://comparedge.com/api-docs |
| OpenAPI spec | https://comparedge.com/api/v2/openapi.json |
| HTTP MCP | https://comparedge.com/api/mcp |
| llms.txt | https://comparedge.com/llms.txt |
| Site | https://comparedge.com |

## License

See [LICENSE](./LICENSE). The OpenAPI spec and code samples are MIT. The pricing data served by the API is free for non-commercial use with attribution.
