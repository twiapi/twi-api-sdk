**[English](./README.md)**

# TwiAPI – 非官方 Twitter/X 数据接口 & Python SDK

> 3 行代码获取 Twitter/X 结构化数据，无需申请官方开发者账号。

[![PyPI version](https://badge.fury.io/py/twiapi.svg)](https://pypi.org/project/twiapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

**TwiAPI** 是一个第三方 Twitter/X 数据接口服务 + Python SDK，提供 14 个接口，无需申请官方开发者账号，直接返回结构化 JSON 数据。

```
你的应用  ──►  TwiAPI  ──►  结构化 JSON
             (我们处理认证、抓取、解析)
```

支持 **任何语言** — Python SDK、或直接调用 REST API（Node.js、cURL、Go、Java 等）。

📖 完整文档：[twiapi.net/docs](https://twiapi.net/docs)

---

## 官方 API vs TwiAPI

| | 官方 Twitter API | TwiAPI |
| --- | --- | --- |
| 开发者申请 | 必须申请，等几天到几周 | 不需要，拿到 Key 立刻用 |
| 数据格式 | 嵌套原始数据，需要清洗 | 结构化 JSON，拿来就用 |
| 调用限制 | 严格，按端点限制 | 按套餐灵活使用 |
| 月费 | $100+（Basic）/ $5,000+（Pro） | $7 起 |
| 接口可用性 | 按套餐分级开放 | 14 个接口全部可用 |

---

## 快速开始

### 1. 安装

```bash
pip install twiapi
```

### 2. 无需 Key 即可体验（Demo 模式）

```python
from twiapi import TwiAPI

api = TwiAPI(demo=True)          # ← 返回模拟数据，无需 API Key
user = api.get_user("elonmusk")  # 获取任意用户的资料和粉丝数
print(user["display_name"], user["followers_count"])
# 输出: Elon Musk 195000000
```

Demo 模式为所有 14 个方法返回逼真的模拟数据——用户资料、推文、粉丝列表、热搜趋势等。无需注册、无需 Key、无需网络请求。

### 3. 使用真实 Key

获取你的 Key — 通过 [Telegram 客服](https://t.me/alex11323) 联系我们，或访问 [twiapi.net](https://twiapi.net)：

```python
api = TwiAPI("YOUR_API_KEY")     # ← 把 demo=True 换成你的真实 Key
user = api.get_user("elonmusk")
print(user["display_name"], user["followers_count"])
```

**直接调用 REST API（支持任何语言）：**

```bash
# cURL
curl -G "https://twiapi.net/api/user/info" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --data-urlencode "username=elonmusk"
```

```javascript
// Node.js
const resp = await fetch(
  "https://twiapi.net/api/user/info?username=elonmusk",
  { headers: { "Authorization": "Bearer YOUR_API_KEY" } }
);
const data = await resp.json();
```

返回示例：

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

## SDK 方法

Python SDK（`pip install twiapi`）为所有 14 个接口提供了简洁方法：

| 分类 | 方法 | 返回 |
|------|------|------|
| **用户** | `api.get_user(username)` | 用户资料、粉丝数、认证状态 |
| | `api.search_users(keyword, count?, cursor?)` | 按关键词搜索用户 |
| | `api.get_user_tweets(username, type?, count?, cursor?)` | 用户的推文、回复或点赞 |
| | `api.get_followers(username, count?, cursor?)` | 粉丝列表，支持翻页 |
| | `api.get_blue_verified_followers(username, count?, cursor?)` | 仅蓝V认证粉丝 |
| | `api.get_following(username, count?, cursor?)` | 用户关注的人 |
| **推文** | `api.search_tweets(keyword, product?, count?, cursor?)` | 搜索推文（最新/热门/媒体） |
| | `api.get_tweet(tweet_id)` | 单条推文完整详情 |
| | `api.get_tweets_batch(tweet_ids)` | 批量获取最多 20 条 |
| | `api.get_comments(tweet_id, count?, cursor?)` | 推文下的评论 |
| | `api.get_retweeters(tweet_id, count?, cursor?)` | 谁转发了 |
| | `api.get_likers(tweet_id, count?, cursor?)` | 谁点赞了 |
| **其他** | `api.get_trends()` | 当前热搜趋势 |
| | `api.get_list_tweets(list_id, count?, cursor?)` | Twitter 列表推文 |

所有方法都支持 **Demo 模式** — 构造函数传 `demo=True` 即可获取模拟数据。

---

## 全部 14 个 REST API 接口

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

所有列表接口支持游标翻页。详见 [完整 API 文档](https://twiapi.net/docs)。

---

## 示例代码

[`examples/`](./examples/) 目录下有可直接运行的 Python 脚本：

| 文件 | 功能 |
|------|------|
| [`sdk_demo.py`](./examples/sdk_demo.py) | **SDK 演示 — 14 个方法全部展示，无需 API Key** |
| [`search_tweets.py`](./examples/search_tweets.py) | 按关键词搜索推文 |
| [`get_user_info.py`](./examples/get_user_info.py) | 获取用户资料 |
| [`get_followers.py`](./examples/get_followers.py) | 翻页获取粉丝列表 |
| [`get_blue_verified_followers.py`](./examples/get_blue_verified_followers.py) | 仅获取蓝V粉丝 |
| [`get_tweet_detail.py`](./examples/get_tweet_detail.py) | 获取单条推文完整详情 |
| [`batch_tweets.py`](./examples/batch_tweets.py) | 批量获取推文 |
| [`get_trends.py`](./examples/get_trends.py) | 获取热搜趋势 |

```bash
pip install twiapi
python examples/search_tweets.py
```

---

## 认证方式

所有请求在 Header 中传入 Bearer Token：

```
Authorization: Bearer YOUR_API_KEY
```

SDK 会自动处理。获取 Key：[twiapi.net](https://twiapi.net/#contact)，支持免费试用。

---

## 返回格式

所有接口返回结构化 JSON，字段一致：

- **用户对象**：`user_id`、`username`、`display_name`、`followers_count`、`following_count`、`tweets_count`、`is_blue_verified`、`avatar_url`、`bio`
- **推文对象**：`tweet_id`、`text`、`created_at`、`user`、`reply_count`、`retweet_count`、`favorite_count`、`view_count`、`bookmark_count`、`hashtags`、`urls`、`media`
- **列表接口**：通过 `next_cursor` 实现游标翻页

无需清洗，拿来直接入库或分析。

---

## 工作原理

TwiAPI 通过自建数据管道聚合公开的 Twitter/X 数据。我们在后端处理会话管理、IP 轮换和端点监控，你不需要维护任何爬虫基础设施。

无需官方开发者账号或审批。服务已生产就绪。

请在适用法律和平台服务条款允许的范围内使用本服务。

---

## 套餐价格

灵活套餐，$7/月起。支持免费试用。所有套餐均可使用全部 14 个接口。

详见 [twiapi.net/#pricing](https://twiapi.net/#pricing)。

---

## 联系我们

- 完整文档：[twiapi.net/docs](https://twiapi.net/docs)
- MCP 接入（支持 Claude、Cursor、ChatGPT 等 AI 工具）：[twiapi.net/mcp-access](https://twiapi.net/mcp-access)
- Telegram 客服：[@alex11323](https://t.me/alex11323) — 7x24 在线
- 官网：[twiapi.net](https://twiapi.net)
- 问题反馈：[GitHub Issues](../../issues)

---

## 关键词

`推特API` `推特数据` `推特爬虫` `推特接口` `twitter数据接口` `twitter api` `twitter api python` `twitter api alternative` `twitter scraper` `x api` `twitter data api` `api wrapper` `osint twitter`

---

⭐ 觉得有用？点个 **Star** 吧！

## 开源协议

基于 [MIT 协议](./LICENSE) 开源。
