"""
TwiAPI Example: Get User Info

Fetch any user's profile including follower count, bio, and verification status.
"""

import requests

API_BASE = "https://zhdq.xyz"
API_KEY = "YOUR_API_KEY"  # Replace with your key from zhdq.xyz


def get_user_info(username):
    """Get a user's complete profile.

    Args:
        username: Twitter username (without @)
    """
    resp = requests.get(
        f"{API_BASE}/api/user/info",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"username": username},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    user = get_user_info("elonmusk")

    print(f"Username: @{user.get('username')}")
    print(f"Display Name: {user.get('display_name')}")
    print(f"Followers: {user.get('followers_count', 0):,}")
    print(f"Following: {user.get('following_count', 0):,}")
    print(f"Tweets: {user.get('tweets_count', 0):,}")
    print(f"Blue Verified: {'Yes' if user.get('is_blue_verified') else 'No'}")
    print(f"Bio: {user.get('bio', '')[:200]}")
    print(f"Avatar: {user.get('avatar_url', '')}")
