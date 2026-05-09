"""
TwiAPI Example: Get Trends

Fetch current trending topics on Twitter/X.
"""

import requests

API_BASE = "https://twiapi.net"
API_KEY = "YOUR_API_KEY"  # Replace with your key from twiapi.net


def get_trends():
    """Get current trending topics."""
    resp = requests.get(
        f"{API_BASE}/api/trends",
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    data = get_trends()

    trends = data.get("trends", [])
    print(f"Current trending topics ({len(trends)}):\n")

    for i, trend in enumerate(trends[:20], 1):
        name = trend.get("name", "")
        tweet_count = trend.get("tweet_count")
        count_str = f" ({tweet_count:,} tweets)" if tweet_count else ""
        print(f"  {i:>2}. {name}{count_str}")
