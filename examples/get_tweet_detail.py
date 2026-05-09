"""
TwiAPI Example: Get Tweet Detail

Fetch a single tweet with full details including author, engagement metrics, and media.
"""

import requests

API_BASE = "https://twiapi.net"
API_KEY = "YOUR_API_KEY"  # Replace with your key from twiapi.net


def get_tweet_detail(tweet_id):
    """Get a tweet's complete details.

    Args:
        tweet_id: The tweet ID
    """
    resp = requests.get(
        f"{API_BASE}/api/tweet/detail",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"tweet_id": tweet_id},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Example tweet ID
    tweet = get_tweet_detail("1864336329352397067")

    user = tweet.get("user", {})
    print(f"Tweet by @{user.get('username', '?')} ({user.get('display_name', '')})")
    print(f"{'─' * 50}")
    print(tweet.get("text", ""))
    print(f"{'─' * 50}")
    print(f"❤️  {tweet.get('favorite_count', 0):,}  likes")
    print(f"🔁  {tweet.get('retweet_count', 0):,}  retweets")
    print(f"💬  {tweet.get('reply_count', 0):,}  replies")
    print(f"👁  {tweet.get('view_count', 0):,}  views")
    print(f"📅  {tweet.get('created_at', '')}")

    media = tweet.get("media", [])
    if media:
        print(f"\n📎 Media ({len(media)}):")
        for m in media:
            print(f"   [{m.get('type', '?')}] {m.get('media_url', '')}")
