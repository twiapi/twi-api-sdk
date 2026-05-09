"""
TwiAPI Example: Get Followers

Fetch a user's followers with cursor-based pagination.
"""

import requests

API_BASE = "https://zhdq.xyz"
API_KEY = "YOUR_API_KEY"  # Replace with your key from zhdq.xyz


def get_followers(username, count=20, cursor=None):
    """Get a user's followers.

    Args:
        username: Twitter username (without @)
        count: Number of results per page (max 40)
        cursor: Pagination cursor from previous response
    """
    params = {"username": username, "count": count}
    if cursor:
        params["cursor"] = cursor

    resp = requests.get(
        f"{API_BASE}/api/user/followers",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    username = "elonmusk"
    data = get_followers(username, count=10)

    print(f"Followers of @{username}:\n")

    for user in data.get("items", []):
        verified = "🔵" if user.get("is_blue_verified") else "  "
        print(f"{verified} @{user.get('username', '?'):>20}  |  "
              f"{user.get('display_name', '')}  |  "
              f"followers: {user.get('followers_count', 0):,}")

    if data.get("next_cursor"):
        print(f"\nNext page cursor: {data['next_cursor']}")
        print("Pass this cursor to get_followers() to fetch the next page.")
