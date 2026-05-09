"""
TwiAPI SDK Demo — try all 14 endpoints without an API key.

Usage:
    pip install twi-api
    python examples/sdk_demo.py
"""

from twi_api import TwiAPI

# ── Demo mode: no API key needed ──────────────────────────
print("=" * 50)
print("Demo Mode (no API key)")
print("=" * 50)

api = TwiAPI(demo=True)

user = api.get_user("elonmusk")
print(f"\n1. get_user('elonmusk')")
print(f"   {user['display_name']} | {user['followers_count']:,} followers | Verified: {user['is_blue_verified']}")

data = api.search_users("AI", count=3)
print(f"\n2. search_users('AI')")
for u in data["items"]:
    print(f"   @{u['username']} — {u['display_name']}")

data = api.get_user_tweets("elonmusk", count=3)
print(f"\n3. get_user_tweets('elonmusk')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

data = api.search_tweets("AI", product="Latest", count=3)
print(f"\n4. search_tweets('AI')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

tweet = api.get_tweet("1864336329352397067")
print(f"\n5. get_tweet('1864336329352397067')")
print(f"   {tweet['text'][:60]}... | ❤️ {tweet['favorite_count']:,} | 👁 {tweet['view_count']:,}")

data = api.get_tweets_batch(["123", "456", "789"])
print(f"\n6. get_tweets_batch(['123','456','789'])")
print(f"   Got {data['total']} tweets")

data = api.get_comments("1864336329352397067", count=3)
print(f"\n7. get_comments('...')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

data = api.get_followers("elonmusk", count=5)
print(f"\n8. get_followers('elonmusk')")
for u in data["items"]:
    verified = "🔵" if u["is_blue_verified"] else "  "
    print(f"   {verified} @{u['username']} — {u['followers_count']:,} followers")

data = api.get_blue_verified_followers("elonmusk", count=3)
print(f"\n9. get_blue_verified_followers('elonmusk')")
for u in data["items"]:
    print(f"   🔵 @{u['username']} — {u['display_name']}")

data = api.get_following("elonmusk", count=3)
print(f"\n10. get_following('elonmusk')")
for u in data["items"]:
    print(f"   @{u['username']}")

data = api.get_retweeters("1864336329352397067", count=3)
print(f"\n11. get_retweeters('...')")
for u in data["items"]:
    print(f"   @{u['username']}")

data = api.get_likers("1864336329352397067", count=3)
print(f"\n12. get_likers('...')")
for u in data["items"]:
    print(f"   @{u['username']}")

trends = api.get_trends()
print(f"\n13. get_trends()")
for t in trends["trends"]:
    print(f"   {t['name']} — {t['tweet_count']:,} tweets")

data = api.get_list_tweets("123456", count=3)
print(f"\n14. get_list_tweets('123456')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

# ── Live mode: with real API key ──────────────────────────
print("\n" + "=" * 50)
print("Live Mode (with API key)")
print("=" * 50)
print("""
# Replace demo=True with your real key:
api = TwiAPI("YOUR_API_KEY")

user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])

# Get your key at: https://zhdq.xyz
""")
