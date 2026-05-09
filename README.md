# TwiAPI – Unofficial Twitter/X Data API & Python SDK

> Get structured Twitter/X data in 3 lines of code. No developer application, no waiting.

[![PyPI version](https://badge.fury.io/py/twi-api.svg)](https://pypi.org/project/twi-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

**TwiAPI** is a Python SDK + third‑party Twitter/X data service that gives you instant access to tweets, user profiles, followers, trends, and more – without the official API's approval delays or rate limits. It returns clean, structured JSON so you can start building immediately.

```
Your App  ──►  TwiAPI  ──►  Clean JSON
             (we handle auth, scraping, parsing)
```

Works with **any language** – Python SDK, or call the REST API directly from Node.js, cURL, Go, Java, etc.

📖 Full docs: [zhdq.xyz/docs](https://zhdq.xyz/docs)

---

## Why TwiAPI?

| | Official Twitter API | TwiAPI |
| --- | --- | --- |
| Developer application | Required (days/weeks) | None – get a key instantly |
| Data format | Nested, needs cleaning | Structured JSON, ready to use |
| Rate limits | Strict, per-endpoint | Flexible per plan |
| Pricing (monthly) | $100+ (Basic) / $5,000+ (Pro) | Starting at $7 |
| Endpoints | Plan-restricted | All 14 available on every plan |

---

## Quick Start

### 1. Install

```bash
pip install twi-api
```

### 2. Try it now — no API key needed (Demo Mode)

```python
from twi_api import TwiAPI

api = TwiAPI(demo=True)          # ← returns realistic sample data
user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])
# Output: Elon Musk 195000000
```

Demo mode works for **all 14 methods**. Clone this repo and run the examples immediately — zero setup required.

### 3. Go live with a real key

Get your key at [zhdq.xyz](https://zhdq.xyz), then:

```python
api = TwiAPI("YOUR_API_KEY")     # ← swap demo=True for your real key
user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])
```

**Using the REST API directly** (Node.js, cURL, Go, etc.):

```bash
# cURL
curl -G "https://zhdq.xyz/api/user/info" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --data-urlencode "username=elonmusk"
```

```javascript
// Node.js
const resp = await fetch(
  "https://zhdq.xyz/api/user/info?username=elonmusk",
  { headers: { "Authorization": "Bearer YOUR_API_KEY" } }
);
const data = await resp.json();
```

Response:

```json
{
  "user_id": "44196397",
  "username": "elonmusk",
  "display_name": "Elon Musk",
  "followers_count": 195000000,
  "following_count": 800,
  "is_blue_verified": true,
  "bio": "...",
  "avatar_url": "..."
}
```

---

## SDK Methods

The Python SDK (`pip install twi-api`) provides simple methods for all 14 endpoints:

| Category | Method | Returns |
|----------|--------|---------|
| **Users** | `api.get_user(username)` | Profile, follower count, verification status |
| | `api.search_users(keyword, count?, cursor?)` | Users matching keyword |
| | `api.get_user_tweets(username, type?, count?, cursor?)` | User's tweets, replies, or likes |
| | `api.get_followers(username, count?, cursor?)` | Follower list with pagination |
| | `api.get_blue_verified_followers(username, count?, cursor?)` | Only blue-verified followers |
| | `api.get_following(username, count?, cursor?)` | Accounts a user follows |
| **Tweets** | `api.search_tweets(keyword, product?, count?, cursor?)` | Search tweets (Top/Latest/Media) |
| | `api.get_tweet(tweet_id)` | Full tweet + author + media |
| | `api.get_tweets_batch(tweet_ids)` | Up to 20 tweets at once |
| | `api.get_comments(tweet_id, count?, cursor?)` | Replies under a tweet |
| | `api.get_retweeters(tweet_id, count?, cursor?)` | Who retweeted |
| | `api.get_likers(tweet_id, count?, cursor?)` | Who liked |
| **Other** | `api.get_trends()` | Current trending topics |
| | `api.get_list_tweets(list_id, count?, cursor?)` | Tweets from a Twitter List |

All methods support **demo mode** — pass `demo=True` to the constructor to get sample data without an API key.

---

## All 14 Endpoints (REST API)

*Cost = the number of requests deducted from your monthly quota per call.*

| Category | Endpoint | Path | Cost | Description |
|----------|----------|------|------|-------------|
| **Users** | User Info | `GET /api/user/info` | 1 | Profile, follower count, verification status |
| | User Search | `GET /api/user/search` | 1 | Find users by keyword |
| | User Tweets | `GET /api/user/tweets` | 1 | User's tweets, replies, or likes |
| | Followers | `GET /api/user/followers` | 3 | Follower list with pagination |
| | Blue Verified Followers | `GET /api/user/blue_verified_followers` | 3 | Only blue-verified followers |
| | Following | `GET /api/user/following` | 3 | Accounts a user follows |
| **Tweets** | Tweet Search | `GET /api/tweet/search` | 2 | Search tweets by keyword (Top/Latest/Media) |
| | Tweet Detail | `GET /api/tweet/detail` | 1 | Full tweet + author + media + engagement |
| | Tweet Batch | `GET /api/tweet/batch` | 5~20 | Up to 20 tweets in one call |
| | Comments | `GET /api/tweet/comments` | 3 | Replies under a tweet |
| | Retweeters | `GET /api/tweet/retweeters` | 2 | Who retweeted a tweet |
| | Likers | `GET /api/tweet/favoriters` | 2 | Who liked a tweet |
| **Other** | Trends | `GET /api/trends` | 1 | Current trending topics |
| | List Tweets | `GET /api/list/tweets` | 2 | Tweets from a Twitter List |

All list endpoints support cursor-based pagination. See [full API reference](https://zhdq.xyz/docs).

---

## Code Examples

Ready-to-run Python scripts in the [`examples/`](./examples/) directory:

| File | What it demonstrates |
|------|---------------------|
| [`examples/search_tweets.py`](./examples/search_tweets.py) | Search tweets and filter by type |
| [`examples/get_user_info.py`](./examples/get_user_info.py) | Fetch any user's profile |
| [`examples/get_followers.py`](./examples/get_followers.py) | Paginated follower retrieval |
| [`examples/get_blue_verified_followers.py`](./examples/get_blue_verified_followers.py) | Filter only verified followers |
| [`examples/get_tweet_detail.py`](./examples/get_tweet_detail.py) | Single tweet with full details |
| [`examples/batch_tweets.py`](./examples/batch_tweets.py) | Retrieve multiple tweets in one call |
| [`examples/get_trends.py`](./examples/get_trends.py) | Current trending topics |

Run any example:

```bash
pip install twi-api
python examples/search_tweets.py
```

---

## Authentication

All live requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

The SDK handles this automatically. Get your key at [zhdq.xyz](https://zhdq.xyz/#contact). Free trials available.

---

## Response Format

All endpoints return structured JSON with consistent fields:

- **User objects**: `user_id`, `username`, `display_name`, `followers_count`, `following_count`, `tweets_count`, `is_blue_verified`, `avatar_url`, `bio`
- **Tweet objects**: `tweet_id`, `text`, `created_at`, `user`, `reply_count`, `retweet_count`, `favorite_count`, `view_count`, `bookmark_count`, `hashtags`, `urls`, `media`
- **List endpoints**: cursor-based pagination via `next_cursor`

No cleaning needed – the data is ready to store or analyze directly.

---

## How It Works

TwiAPI uses a proprietary data pipeline that aggregates publicly available Twitter/X information. We handle session management, IP rotation, and endpoint monitoring behind the scenes so you don't have to maintain any scraping infrastructure.

No official developer account or approval is required on your end. The service is production‑ready.

Please use the service responsibly and in compliance with applicable laws and platform terms of service.

---

## Pricing

Flexible plans starting at $7/month. Free trials are available. All plans include access to all 14 endpoints.

See full pricing at [zhdq.xyz/#pricing](https://zhdq.xyz/#pricing).

---

## Support & Resources

- **Full API docs**: [zhdq.xyz/docs](https://zhdq.xyz/docs)
- **MCP integration** (for AI agents like Claude, Cursor, ChatGPT): [zhdq.xyz/mcp-access](https://zhdq.xyz/mcp-access)
- **Telegram support**: [@alex11323](https://t.me/alex11323) — 7×24 online
- **Website**: [zhdq.xyz](https://zhdq.xyz)
- **Bug reports**: [GitHub Issues](../../issues)

---

## 中文说明

TwiAPI 是一个第三方 Twitter/X 数据接口服务 + Python SDK，提供 14 个接口，无需申请官方开发者账号，直接返回结构化 JSON 数据。

📖 完整文档：[zhdq.xyz/docs](https://zhdq.xyz/docs)

### 官方 API vs TwiAPI

| | 官方 Twitter API | TwiAPI |
| --- | --- | --- |
| 开发者申请 | 必须申请，等几天到几周 | 不需要，拿到 Key 立刻用 |
| 数据格式 | 嵌套原始数据，需要清洗 | 结构化 JSON，拿来就用 |
| 调用限制 | 严格，按端点限制 | 按套餐灵活使用 |
| 月费 | $100+（Basic）/ $5,000+（Pro） | $7 起 |
| 接口可用性 | 按套餐分级开放 | 14 个接口全部可用 |

### 快速开始

**安装 SDK：**
```bash
pip install twi-api
```

**无需 Key 即可体验（Demo 模式）：**
```python
from twi_api import TwiAPI

api = TwiAPI(demo=True)          # 返回模拟数据，无需 API Key
user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])
# 输出: Elon Musk 195000000
```

**使用真实 Key：**
```python
api = TwiAPI("YOUR_API_KEY")
user = api.get_user("elonmusk")
```

**也可直接调用 REST API（支持任何语言）：**

```bash
curl -G "https://zhdq.xyz/api/user/info" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --data-urlencode "username=elonmusk"
```

### 全部 14 个接口

*消耗 = 每次调用从月度配额中扣除的请求次数。*

| 分类 | 接口 | 路径 | 消耗 | 说明 |
|------|------|------|------|------|
| **用户** | 用户信息 | `GET /api/user/info` | 1 | 用户资料、粉丝数、认证状态 |
| | 用户搜索 | `GET /api/user/search` | 1 | 按关键词搜索用户 |
| | 用户推文 | `GET /api/user/tweets` | 1 | 用户的推文、回复或点赞 |
| | 粉丝列表 | `GET /api/user/followers` | 3 | 粉丝列表，支持翻页 |
| | 蓝V粉丝 | `GET /api/user/blue_verified_followers` | 3 | 仅蓝V认证粉丝 |
| | 关注列表 | `GET /api/user/following` | 3 | 用户关注的人 |
| **推文** | 推文搜索 | `GET /api/tweet/search` | 2 | 按关键词搜索，支持最新/热门/媒体筛选 |
| | 推文详情 | `GET /api/tweet/detail` | 1 | 完整推文 + 作者 + 媒体 + 互动数据 |
| | 批量推文 | `GET /api/tweet/batch` | 5~20 | 一次获取最多 20 条推文 |
| | 推文评论 | `GET /api/tweet/comments` | 3 | 推文下的回复和评论 |
| | 转发者 | `GET /api/tweet/retweeters` | 2 | 查看谁转发了推文 |
| | 点赞者 | `GET /api/tweet/favoriters` | 2 | 查看谁点赞了推文 |
| **其他** | 热搜趋势 | `GET /api/trends` | 1 | 当前热门趋势话题 |
| | 列表推文 | `GET /api/list/tweets` | 2 | 获取 Twitter 列表内的推文 |

所有列表接口支持游标翻页。

### 示例代码

[`examples/`](./examples/) 目录下有可直接运行的 Python 脚本：

| 文件 | 功能 |
|------|------|
| [`search_tweets.py`](./examples/search_tweets.py) | 按关键词搜索推文 |
| [`get_user_info.py`](./examples/get_user_info.py) | 获取用户资料 |
| [`get_followers.py`](./examples/get_followers.py) | 翻页获取粉丝列表 |
| [`get_blue_verified_followers.py`](./examples/get_blue_verified_followers.py) | 仅获取蓝V粉丝 |
| [`get_tweet_detail.py`](./examples/get_tweet_detail.py) | 获取单条推文完整详情 |
| [`batch_tweets.py`](./examples/batch_tweets.py) | 批量获取推文 |
| [`get_trends.py`](./examples/get_trends.py) | 获取热搜趋势 |

```bash
pip install twi-api
python examples/search_tweets.py
```

### 联系我们

- 完整文档：[zhdq.xyz/docs](https://zhdq.xyz/docs)
- MCP 接入（支持 Claude、Cursor、ChatGPT 等 AI 工具）：[zhdq.xyz/mcp-access](https://zhdq.xyz/mcp-access)
- Telegram 客服：[@alex11323](https://t.me/alex11323) — 7x24 在线
- 官网：[zhdq.xyz](https://zhdq.xyz)

---

## Keywords

`twitter api` `twitter api python` `twitter api alternative` `twitter scraper` `twitter data api` `twitter api wrapper` `x api` `tweet search api` `twitter followers api` `twitter user info api` `scrape tweets` `twitter scraping` `get twitter data` `twitter api free` `twitter api cheap` `social media api` `osint twitter` `python twitter` `twitter unofficial api` `twitter api without developer account` `推特API` `推特数据` `推特爬虫` `推特接口` `twitter数据接口`

---

⭐ **Star this repo** if you find it useful!

## License

Released under the [MIT License](./LICENSE).
