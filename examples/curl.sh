#!/usr/bin/env bash
# ComparEdge pricing API — curl examples. No key required.
set -euo pipefail

BASE="https://comparedge.com/api/v2"

echo "== One product (summary) =="
curl -s "$BASE/pricing/notion?depth=summary" | python3 -m json.tool

echo "== Full record =="
curl -s "$BASE/pricing/supabase?depth=full" | python3 -m json.tool | head -40

echo "== Batch (up to 20 slugs) =="
curl -s "$BASE/pricing?slugs=notion,coda,airtable" | python3 -m json.tool | head -20

echo "== Compare 2-4 products =="
curl -s "$BASE/compare?slugs=notion,coda" | python3 -m json.tool | head -30

echo "== Discover by criteria =="
curl -s "$BASE/discover?category=databases&hasFreeTier=true&limit=5" | python3 -m json.tool

echo "== LLM usage rate card + estimate =="
curl -s "$BASE/usage/openai-api?inputTokens=1000000&outputTokens=500000" | python3 -m json.tool | head -30

echo "== Team TCO (POST) =="
curl -s -X POST "$BASE/tco" \
  -H "Content-Type: application/json" \
  -d '{"slug":"notion","seats":25,"billing":"annual"}' | python3 -m json.tool | head -30
