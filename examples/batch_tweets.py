"""
TwiAPI Example: Batch Tweets

Fetch up to 20 tweets in a single request.
Cost: per-tweet pricing (1 point each, minimum 5 points).
"""

import requests

API_BASE = "https://twiapi.net"
API_KEY = "YOUR_API_KEY"  # Replace with your key from twiapi.net


def batch_tweets(tweet_ids):
    """Fetch multiple tweets at once.

    Args:
        tweet_ids: List of tweet ID strings (max 20)
    """
    resp = requests.get(
        f"{API_BASE}/api/tweet/batch",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"tweet_ids": ",".join(tweet_ids)},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    ids = [
        "1864336329352397067",
        "1864336329352397068",
        "1864336329352397069",
    ]

    data = batch_tweets(ids)

    print(f"Fetched {data.get('total', 0)} of {len(ids)} tweets\n")

    for tweet in data.get("items", []):
        user = tweet.get("user", {})
        print(f"@{user.get('username', '?')}")
        print(f"  {tweet.get('text', '')[:80]}...")
        print(f"  ❤️ {tweet.get('favorite_count', 0)}  🔁 {tweet.get('retweet_count', 0)}")
        print()
