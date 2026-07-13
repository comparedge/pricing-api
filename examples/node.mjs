// ComparEdge pricing API — Node.js example (Node 18+, no deps). No key required.
//   node examples/node.mjs
const BASE = "https://comparedge.com/api/v2";

async function getPricing(slug, depth = "summary") {
  const res = await fetch(`${BASE}/pricing/${slug}?depth=${depth}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function compare(...slugs) {
  const res = await fetch(`${BASE}/compare?slugs=${slugs.join(",")}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

const data = await getPricing("supabase");
console.log(`${data.name} — ${data.priceRange.display}`);
for (const t of data.tiers) {
  console.log(`  ${t.name}: $${t.price}/${t.period}${t.isFree ? " (free)" : ""}`);
}
console.log("Source:", data.links.page);
console.log(data.attribution);

const cmp = await compare("notion", "coda");
console.log(`\nCompared ${cmp.products?.length ?? 0} products`);
