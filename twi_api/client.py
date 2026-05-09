"""TwiAPI client — thin wrapper around the TwiAPI REST endpoints."""

import requests


class TwiAPIError(Exception):
    """Raised when the API returns a non-2xx response."""

    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


# ── Demo data ────────────────────────────────────────────────

_DEMO_USER = {
    "user_id": "44196397",
    "username": "elonmusk",
    "display_name": "Elon Musk",
    "followers_count": 195000000,
    "following_count": 800,
    "tweets_count": 42000,
    "is_blue_verified": True,
    "bio": "Mars & Cars, Chips & Dips",
    "avatar_url": "https://pbs.twimg.com/profile_images/1845482317444718592/JNbuc9GS_400x400.jpg",
}

_DEMO_TWEET = {
    "tweet_id": "1864336329352397067",
    "text": "The future is exciting ✨",
    "full_text": "The future is exciting ✨",
    "lang": "en",
    "created_at": "2024-12-04T12:00:00",
    "user": {
        "user_id": "44196397",
        "username": "elonmusk",
        "display_name": "Elon Musk",
        "avatar_url": "https://pbs.twimg.com/profile_images/1845482317444718592/JNbuc9GS_400x400.jpg",
        "followers_count": 195000000,
        "is_blue_verified": True,
    },
    "reply_count": 15000,
    "retweet_count": 28000,
    "favorite_count": 192000,
    "view_count": 85000000,
    "bookmark_count": 6200,
    "hashtags": [],
    "urls": [],
    "media": None,
}


def _demo_user_item(i):
    return {
        "user_id": f"10000{i}",
        "username": f"user_{i}",
        "display_name": f"Demo User {i}",
        "followers_count": 1000 * (i + 1),
        "following_count": 200 + i,
        "tweets_count": 500 + i * 10,
        "is_blue_verified": i % 3 == 0,
        "bio": f"This is demo user {i}",
        "avatar_url": "",
    }


# ── Client ───────────────────────────────────────────────────

class TwiAPI:
    """TwiAPI client.

    Args:
        api_key: Your TwiAPI key (get one at https://twiapi.net).
            Pass ``demo=True`` instead to use demo mode (no key needed).
        demo: If True, return realistic sample data without calling the API.
        base_url: API base URL. Change this only for testing.
    """

    def __init__(self, api_key: str = "", demo: bool = False, base_url: str = "https://twiapi.net"):
        self.demo = demo
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        if api_key:
            self._session.headers["Authorization"] = f"Bearer {api_key}"

    # ── internal ────────────────────────────────────────────

    def _get(self, path: str, **params) -> dict:
        resp = self._session.get(f"{self.base_url}{path}", params=params)
        if not resp.ok:
            detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise TwiAPIError(resp.status_code, detail)
        return resp.json()

    def _demo_items(self, count=5):
        return [_demo_user_item(i) for i in range(count)]

    def _demo_tweets(self, count=5):
        items = []
        for i in range(count):
            t = dict(_DEMO_TWEET)
            t["tweet_id"] = f"18643363293523970{6 + i}"
            t["text"] = f"Demo tweet #{i + 1} — this is sample data."
            t["favorite_count"] = 1000 * (i + 1)
            items.append(t)
        return items

    def _check_demo(self, fn):
        if self.demo:
            return fn()
        return None

    # ── users ───────────────────────────────────────────────

    def get_user(self, username: str) -> dict:
        """Get a user's profile (followers, bio, verification status)."""
        r = self._check_demo(lambda: dict(_DEMO_USER, username=username))
        return r or self._get("/api/user/info", username=username)

    def search_users(self, keyword: str, count: int = 20, cursor: str | None = None) -> dict:
        """Search for users by keyword."""
        r = self._check_demo(lambda: {"items": self._demo_items(count), "total": count})
        return r or self._get("/api/user/search", keyword=keyword, count=count, **({"cursor": cursor} if cursor else {}))

    def get_user_tweets(self, username: str, tweet_type: str = "tweets", count: int = 20, cursor: str | None = None) -> dict:
        """Get a user's tweets, replies, or likes."""
        r = self._check_demo(lambda: {"items": self._demo_tweets(count), "total": count})
        return r or self._get("/api/user/tweets", username=username, type=tweet_type, count=count, **({"cursor": cursor} if cursor else {}))

    def get_followers(self, username: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get a user's followers."""
        r = self._check_demo(lambda: {"items": self._demo_items(count), "total": count, "next_cursor": None})
        return r or self._get("/api/user/followers", username=username, count=count, **({"cursor": cursor} if cursor else {}))

    def get_blue_verified_followers(self, username: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get only blue-verified followers of a user."""
        r = self._check_demo(lambda: {"items": [u for u in self._demo_items(count) if u["is_blue_verified"]], "total": count, "next_cursor": None})
        return r or self._get("/api/user/blue_verified_followers", username=username, count=count, **({"cursor": cursor} if cursor else {}))

    def get_following(self, username: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get accounts a user follows."""
        r = self._check_demo(lambda: {"items": self._demo_items(count), "total": count, "next_cursor": None})
        return r or self._get("/api/user/following", username=username, count=count, **({"cursor": cursor} if cursor else {}))

    # ── tweets ──────────────────────────────────────────────

    def search_tweets(self, keyword: str, product: str = "Latest", count: int = 10, cursor: str | None = None) -> dict:
        """Search tweets by keyword. product: 'Latest', 'Top', or 'Media'."""
        r = self._check_demo(lambda: {"items": self._demo_tweets(count), "total": count, "next_cursor": None})
        return r or self._get("/api/tweet/search", keyword=keyword, product=product, count=count, **({"cursor": cursor} if cursor else {}))

    def get_tweet(self, tweet_id: str) -> dict:
        """Get a single tweet with full details."""
        r = self._check_demo(lambda: dict(_DEMO_TWEET, tweet_id=tweet_id))
        return r or self._get("/api/tweet/detail", tweet_id=tweet_id)

    def get_tweets_batch(self, tweet_ids: list[str]) -> dict:
        """Get up to 20 tweets at once. tweet_ids: list of tweet ID strings."""
        r = self._check_demo(lambda: {"items": self._demo_tweets(len(tweet_ids)), "total": len(tweet_ids)})
        return r or self._get("/api/tweet/batch", tweet_ids=",".join(tweet_ids))

    def get_comments(self, tweet_id: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get replies under a tweet."""
        r = self._check_demo(lambda: {"items": self._demo_tweets(count), "total": count, "next_cursor": None})
        return r or self._get("/api/tweet/comments", tweet_id=tweet_id, count=count, **({"cursor": cursor} if cursor else {}))

    def get_retweeters(self, tweet_id: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get users who retweeted a tweet."""
        r = self._check_demo(lambda: {"items": self._demo_items(count), "total": count, "next_cursor": None})
        return r or self._get("/api/tweet/retweeters", tweet_id=tweet_id, count=count, **({"cursor": cursor} if cursor else {}))

    def get_likers(self, tweet_id: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get users who liked a tweet."""
        r = self._check_demo(lambda: {"items": self._demo_items(count), "total": count, "next_cursor": None})
        return r or self._get("/api/tweet/favoriters", tweet_id=tweet_id, count=count, **({"cursor": cursor} if cursor else {}))

    # ── trends & lists ──────────────────────────────────────

    def get_trends(self) -> dict:
        """Get current trending topics."""
        r = self._check_demo(lambda: {"trends": [{"name": "#AI", "tweet_count": 125000}, {"name": "#Python", "tweet_count": 89000}, {"name": "#OpenSource", "tweet_count": 45000}]})
        return r or self._get("/api/trends")

    def get_list_tweets(self, list_id: str, count: int = 20, cursor: str | None = None) -> dict:
        """Get tweets from a Twitter List."""
        r = self._check_demo(lambda: {"items": self._demo_tweets(count), "total": count, "next_cursor": None})
        return r or self._get("/api/list/tweets", list_id=list_id, count=count, **({"cursor": cursor} if cursor else {}))
