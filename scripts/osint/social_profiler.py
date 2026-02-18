"""
Script: Social Profiler - Username OSINT Cross-Platform
Created: 2026-02-18
Last Updated: 2026-02-18

Correlation de username cross-platform (style Sherlock).
Identifie la presence d'un username sur les principales plateformes.
"""

import sys
import json
import time

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# Plateformes a verifier avec leur pattern d'URL
PLATFORMS = {
    "github": {"url": "https://github.com/{}", "check": 200},
    "gitlab": {"url": "https://gitlab.com/{}", "check": 200},
    "twitter": {"url": "https://x.com/{}", "check": 200},
    "linkedin": {"url": "https://www.linkedin.com/in/{}", "check": 200},
    "instagram": {"url": "https://www.instagram.com/{}/", "check": 200},
    "reddit": {"url": "https://www.reddit.com/user/{}", "check": 200},
    "medium": {"url": "https://medium.com/@{}", "check": 200},
    "devto": {"url": "https://dev.to/{}", "check": 200},
    "hackernews": {"url": "https://news.ycombinator.com/user?id={}", "check": 200},
    "keybase": {"url": "https://keybase.io/{}", "check": 200},
    "telegram": {"url": "https://t.me/{}", "check": 200},
    "pinterest": {"url": "https://www.pinterest.com/{}/", "check": 200},
    "tiktok": {"url": "https://www.tiktok.com/@{}", "check": 200},
    "youtube": {"url": "https://www.youtube.com/@{}", "check": 200},
    "twitch": {"url": "https://www.twitch.tv/{}", "check": 200},
    "stackoverflow": {"url": "https://stackoverflow.com/users/?q={}", "check": 200},
    "npm": {"url": "https://www.npmjs.com/~{}", "check": 200},
    "pypi": {"url": "https://pypi.org/user/{}/", "check": 200},
    "dockerhub": {"url": "https://hub.docker.com/u/{}", "check": 200},
    "hackerone": {"url": "https://hackerone.com/{}", "check": 200},
    "bugcrowd": {"url": "https://bugcrowd.com/{}", "check": 200},
    "bitbucket": {"url": "https://bitbucket.org/{}/", "check": 200},
    "mastodon": {"url": "https://mastodon.social/@{}", "check": 200},
    "codeberg": {"url": "https://codeberg.org/{}", "check": 200},
}


def check_platform(username, platform_name, platform_config):
    """
    Verifie la presence d'un username sur une plateforme.

    Args:
        username: Username a chercher
        platform_name: Nom de la plateforme
        platform_config: Configuration de la plateforme

    Returns:
        dict: Resultat du check
    """
    url = platform_config["url"].format(username)
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; OSINT-Toolkit/1.0)"},
            timeout=10,
            allow_redirects=False,
        )
        found = resp.status_code == platform_config["check"]
        return {
            "platform": platform_name,
            "url": url,
            "found": found,
            "status_code": resp.status_code,
        }
    except requests.RequestException:
        return {
            "platform": platform_name,
            "url": url,
            "found": False,
            "status_code": 0,
            "error": "timeout_or_blocked",
        }


def profile_username(username):
    """
    Profile un username sur toutes les plateformes.

    Args:
        username: Username a profiler

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Social Profiler: {username}...", file=sys.stderr)

    if not HAS_REQUESTS:
        return {"error": "requests not installed"}

    results = []
    found_on = []

    for platform_name, config in PLATFORMS.items():
        result = check_platform(username, platform_name, config)
        results.append(result)
        if result["found"]:
            found_on.append({"platform": platform_name, "url": result["url"]})
            print(f"  [FOUND] {platform_name}: {result['url']}", file=sys.stderr)
        time.sleep(0.5)  # Rate limiting

    return {
        "username": username,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "platforms_checked": len(PLATFORMS),
        "found_on": found_on,
        "found_count": len(found_on),
        "all_results": results,
        "stats": {
            "checked": len(results),
            "found": len(found_on),
            "errors": len([r for r in results if r.get("error")]),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 social_profiler.py <username>"}))
        sys.exit(1)
    data = profile_username(sys.argv[1])
    print(json.dumps(data, indent=2))
