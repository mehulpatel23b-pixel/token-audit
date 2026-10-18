import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from token_audit.report import human, shareable
from token_audit.github import _mask


def test_mask_hides_secret():
    assert "ghp_secretvalue123" not in _mask("ghp_secretvalue123")
    assert _mask("ghp_secretvalue123") == "ghp...1123" or _mask("ghp_secretvalue123").startswith("ghp")


def test_shareable_never_contains_token():
    result = {"valid": True, "user": "someone", "type": "classic PAT",
              "scopes": ["repo"], "rate": {"core": "4999/5000"}, "masked": "ghp...1234", "notes": []}
    s = shareable(result)
    assert "someone" not in s
    assert "ghp" not in s
