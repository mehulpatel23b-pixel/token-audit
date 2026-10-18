"""GitHub API inspection for a token. Read-only. The secret never leaves this module."""
import requests


def _mask(token):
    if not token:
        return "(none)"
    return f"{token[:4]}...{token[-4:]}" if len(token) > 8 else "(too short to be a token)"


def audit(token):
    """Return a dict describing the token. Never returns the token itself."""
    result = {
        "valid": False,
        "user": None,
        "type": "unknown",
        "scopes": [],
        "rate": {},
        "masked": _mask(token),
        "notes": [],
    }
    if not token:
        result["notes"].append("No token provided. Set GITHUB_TOKEN or pass --token.")
        return result

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    resp = requests.get("https://api.github.com/user", headers=headers, timeout=30)
    scopes_header = resp.headers.get("X-OAuth-Scopes", "")

    if resp.status_code == 401:
        result["notes"].append("Token is INVALID or revoked (401).")
        return result

    scopes = [s.strip() for s in scopes_header.split(",") if s.strip()]
    if resp.status_code == 403 and not scopes_header:
        # fine-grained PATs and app tokens do not expose X-OAuth-Scopes
        result["type"] = "fine-grained PAT or installation token"
        result["notes"].append("No classic scopes header: likely a fine-grained PAT (permissions are per-resource).")
    elif scopes:
        result["type"] = "classic PAT"
        result["scopes"] = scopes

    if resp.status_code == 200:
        result["valid"] = True
        result["user"] = resp.json().get("login")

    # rate limits per resource
    rl = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=30)
    if rl.status_code == 200:
        core = rl.json().get("resources", {}).get("core", {})
        search = rl.json().get("resources", {}).get("search", {})
        result["rate"] = {
            "core": f"{core.get('remaining')}/{core.get('limit')}",
            "search": f"{search.get('remaining')}/{search.get('limit')}",
        }
        # 5000 = authenticated, 60 = unauthenticated
        if core.get("limit") and core["limit"] <= 60:
            result["notes"].append("Core limit of 60/hr means this token is NOT authenticating API calls.")

    if "repo" in scopes and "workflow" not in scopes:
        result["notes"].append("Has repo scope but not workflow: cannot write .github/workflows files.")
    if "delete_repo" in scopes:
        result["notes"].append("WARNING: delete_repo scope present — this token can permanently delete repos.")
    if scopes == ["repo", "read:user"] or not scopes:
        result["notes"].append("Principle of least privilege: request only the scopes each tool needs.")

    return result
