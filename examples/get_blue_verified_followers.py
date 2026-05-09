"""
TwiAPI Example: Get Blue Verified Followers

Fetch only the blue-verified followers of a user.
Useful for finding influential followers, KOL analysis, and audience quality checks.
"""

import requests

API_BASE = "https://zhdq.xyz"
API_KEY = "YOUR_API_KEY"  # Replace with your key from zhdq.xyz


def get_blue_verified_followers(username, count=20, cursor=None):
    """Get a user's blue-verified followers only.

    Args:
        username: Twitter username (without @)
        count: Number of results per page (max 40)
        cursor: Pagination cursor from previous response
    """
    params = {"username": username, "count": count}
    if cursor:
        params["cursor"] = cursor

    resp = requests.get(
        f"{API_BASE}/api/user/blue_verified_followers",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    username = "elonmusk"
    data = get_blue_verified_followers(username, count=10)

    print(f"Blue-verified followers of @{username}:\n")

    for user in data.get("items", []):
        print(f"🔵 @{user.get('username', '?'):>20}  |  "
              f"{user.get('display_name', '')}  |  "
              f"followers: {user.get('followers_count', 0):,}")

    if data.get("next_cursor"):
        print(f"\nNext page cursor: {data['next_cursor']}")
