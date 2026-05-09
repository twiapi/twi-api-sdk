"""
TwiAPI Example: Search Tweets

Search for tweets by keyword. Supports filtering by type (Latest, Top, Media).
"""

import requests

API_BASE = "https://zhdq.xyz"
API_KEY = "YOUR_API_KEY"  # Replace with your key from zhdq.xyz


def search_tweets(keyword, product="Latest", count=10, cursor=None):
    """Search tweets by keyword.

    Args:
        keyword: Search query string
        product: "Latest", "Top", or "Media"
        count: Number of results per page (max 40)
        cursor: Pagination cursor from previous response
    """
    params = {"keyword": keyword, "product": product, "count": count}
    if cursor:
        params["cursor"] = cursor

    resp = requests.get(
        f"{API_BASE}/api/tweet/search",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    data = search_tweets("AI", product="Latest", count=5)

    print(f"Found {data.get('total', 0)} tweets\n")

    for tweet in data.get("items", []):
        user = tweet.get("user", {})
        print(f"@{user.get('username', '?')} ({user.get('display_name', '')})")
        print(f"  {tweet.get('text', '')[:100]}")
        print(f"  ❤️ {tweet.get('favorite_count', 0)}  🔁 {tweet.get('retweet_count', 0)}  👁 {tweet.get('view_count', 0)}")
        print()

    if data.get("next_cursor"):
        print(f"Next page cursor: {data['next_cursor']}")
