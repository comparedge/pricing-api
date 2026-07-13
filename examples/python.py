"""ComparEdge pricing API — Python example. No key required.

    pip install requests
    python examples/python.py
"""
import requests

BASE = "https://comparedge.com/api/v2"


def get_pricing(slug: str, depth: str = "summary") -> dict:
    r = requests.get(f"{BASE}/pricing/{slug}", params={"depth": depth}, timeout=20)
    r.raise_for_status()
    return r.json()


def discover(category: str, has_free_tier: bool = False, limit: int = 10) -> dict:
    r = requests.get(
        f"{BASE}/discover",
        params={"category": category, "hasFreeTier": str(has_free_tier).lower(), "limit": limit},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    data = get_pricing("supabase")
    print(f'{data["name"]} — {data["priceRange"]["display"]}')
    for tier in data["tiers"]:
        free = " (free)" if tier["isFree"] else ""
        print(f'  {tier["name"]}: ${tier["price"]}/{tier["period"]}{free}')

    print("\nHidden costs:")
    for hc in data.get("hiddenCosts", []):
        print(f'  - {hc["label"]}: {hc["cost"]}')

    # Attribution comes back ready to paste. Link to links.page when you show a number.
    print("\n" + data["attribution"])

    print("\nDatabases with a free tier:")
    for row in discover("databases", has_free_tier=True, limit=5)["results"]:
        print(f'  {row["name"]} -> {row["links"]["page"]}')
