"""CLI: audit a GitHub token without ever printing the secret."""
import argparse
import os
import sys

from .github import audit
from .report import human, shareable


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="token-audit",
        description="Inspect a GitHub token's validity, scopes and rate limits. The secret is never printed.",
    )
    parser.add_argument("--token", default=None, help="Token (prefer GITHUB_TOKEN env var instead)")
    parser.add_argument("--shareable", action="store_true", help="Print a report safe to paste publicly")
    args = parser.parse_args(argv)

    token = args.token or os.environ.get("GITHUB_TOKEN")
    result = audit(token)
    out = shareable(result) if args.shareable else human(result)
    print(out)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
