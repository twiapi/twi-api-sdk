"""
TwiAPI SDK Demo — try all 14 endpoints without an API key.
TwiAPI SDK 演示 — 无需 API Key 即可体验全部 14 个接口。

Usage / 使用方法:
    pip install twi-api
    python examples/sdk_demo.py
"""

from twi_api import TwiAPI

# ── Demo mode: no API key needed / 演示模式：无需 API Key ──
print("=" * 50)
print("Demo Mode / 演示模式 (no API key / 无需 Key)")
print("=" * 50)

api = TwiAPI(demo=True)

# 1. get_user — Get a user's profile and follower count
#    获取用户资料和粉丝数
user = api.get_user("elonmusk")
print(f"\n1. get_user('elonmusk')")
print(f"   {user['display_name']} | {user['followers_count']:,} followers | Verified: {user['is_blue_verified']}")

# 2. search_users — Search for users by keyword
#    按关键词搜索用户
data = api.search_users("AI", count=3)
print(f"\n2. search_users('AI')")
for u in data["items"]:
    print(f"   @{u['username']} — {u['display_name']}")

# 3. get_user_tweets — Get a user's tweets, replies, or likes
#    获取用户的推文、回复或点赞
data = api.get_user_tweets("elonmusk", count=3)
print(f"\n3. get_user_tweets('elonmusk')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

# 4. search_tweets — Search tweets by keyword, filter by type (Top/Latest/Media)
#    按关键词搜索推文，支持按类型筛选（热门/最新/媒体）
data = api.search_tweets("AI", product="Latest", count=3)
print(f"\n4. search_tweets('AI', product='Latest')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

# 5. get_tweet — Get a single tweet with full details (author, engagement, media)
#    获取单条推文的完整详情（作者、互动数据、媒体）
tweet = api.get_tweet("1864336329352397067")
print(f"\n5. get_tweet('1864336329352397067')")
print(f"   {tweet['text'][:60]}... | ❤️ {tweet['favorite_count']:,} | 👁 {tweet['view_count']:,}")

# 6. get_tweets_batch — Get up to 20 tweets in one request
#    一次请求获取最多 20 条推文
data = api.get_tweets_batch(["123", "456", "789"])
print(f"\n6. get_tweets_batch(['123','456','789'])")
print(f"   Got {data['total']} tweets")

# 7. get_comments — Get replies under a tweet
#    获取推文下的评论和回复
data = api.get_comments("1864336329352397067", count=3)
print(f"\n7. get_comments('...')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

# 8. get_followers — Get a user's follower list with pagination
#    获取用户的粉丝列表，支持翻页
data = api.get_followers("elonmusk", count=5)
print(f"\n8. get_followers('elonmusk')")
for u in data["items"]:
    verified = "🔵" if u["is_blue_verified"] else "  "
    print(f"   {verified} @{u['username']} — {u['followers_count']:,} followers")

# 9. get_blue_verified_followers — Get only blue-verified followers of a user
#    仅获取用户的蓝V认证粉丝
data = api.get_blue_verified_followers("elonmusk", count=3)
print(f"\n9. get_blue_verified_followers('elonmusk')")
for u in data["items"]:
    print(f"   🔵 @{u['username']} — {u['display_name']}")

# 10. get_following — Get accounts a user follows
#     获取用户关注的人
data = api.get_following("elonmusk", count=3)
print(f"\n10. get_following('elonmusk')")
for u in data["items"]:
    print(f"   @{u['username']}")

# 11. get_retweeters — Get users who retweeted a tweet
#     获取转发某条推文的用户列表
data = api.get_retweeters("1864336329352397067", count=3)
print(f"\n11. get_retweeters('...')")
for u in data["items"]:
    print(f"   @{u['username']}")

# 12. get_likers — Get users who liked a tweet
#     获取点赞某条推文的用户列表
data = api.get_likers("1864336329352397067", count=3)
print(f"\n12. get_likers('...')")
for u in data["items"]:
    print(f"   @{u['username']}")

# 13. get_trends — Get current trending topics
#     获取当前热搜趋势话题
trends = api.get_trends()
print(f"\n13. get_trends()")
for t in trends["trends"]:
    print(f"   {t['name']} — {t['tweet_count']:,} tweets")

# 14. get_list_tweets — Get tweets from a Twitter List
#     获取 Twitter 列表内的推文
data = api.get_list_tweets("123456", count=3)
print(f"\n14. get_list_tweets('123456')")
for t in data["items"]:
    print(f"   {t['text'][:60]}...")

# ── Live mode: with real API key / 真实模式：使用 API Key ──
print("\n" + "=" * 50)
print("Live Mode / 真实模式 (with API key / 使用 Key)")
print("=" * 50)
print("""
# Replace demo=True with your real key / 把 demo=True 换成你的真实 Key:
api = TwiAPI("YOUR_API_KEY")

user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])

# Get your key / 获取 Key:
#   Telegram: https://t.me/alex11323
#   Website:  https://zhdq.xyz
""")
