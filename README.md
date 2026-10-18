<div align="center">

# 🔐 token-audit

**Know exactly what your GitHub token can do — without ever printing the secret.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![No Secrets Logged](https://img.shields.io/badge/secrets%20never%20printed-success?style=for-the-badge)](#security)

</div>

---

Most people have no idea which of their GitHub tokens can delete their repos.
token-audit inspects any token and reports its **validity, scopes, type, and
rate limits** — with the secret masked at all times.

## Install

```bash
git clone https://github.com/mehulpatel23b-pixel/token-audit
cd token-audit
pip install -r requirements.txt
```

## Usage

```bash
export GITHUB_TOKEN="ghp_..."
python3 -m token_audit.cli                # full audit
python3 -m token_audit.cli --shareable    # safe-to-paste public profile
python3 -m token_audit.cli --token ghp_... # inline token (env var is safer)
```

## Sample output

```
GitHub Token Audit
========================================
Token       : gho_...ibeE
Valid       : True
User        : your-login
Type        : classic PAT
Scopes      : read:org, read:user, repo, workflow
Rate core   : 4961/5000
Rate search : 30/30

  ! WARNING: delete_repo scope present — this token can permanently delete repos.
```

## What it detects

- Invalid / revoked tokens
- Classic PAT vs fine-grained PAT / installation tokens
- `delete_repo` — the scope that can destroy your work
- A core rate limit of 60/hr (token not actually authenticating)
- Missing `workflow` scope when `repo` is present

## Sharing access with viewers (read this!)

**Never put a real token in a repo, README, or issue.** Anyone who sees it can act
as you, and GitHub auto-revokes leaked tokens. If you want people to *use* a tool:

- Public-data tools (like [repo-radar](https://github.com/mehulpatel23b-pixel/repo-radar))
  run fine with **no token at all** — GitHub's public API just rate-limits harder.
- Each viewer should create their **own** free token at github.com → Settings →
  Developer settings → Personal access tokens, and keep it in their environment.
- For real shared apps, use a backend that holds the token server-side and exposes
  only results — never ship the key to the browser or the repo.

## Security

- The token is **never printed, logged, or sent anywhere except api.github.com**
- `--shareable` output contains no token material and no username — safe for bug reports and issues
- Prefer passing tokens via `GITHUB_TOKEN` env var, never `--token` in shared shells

## Project structure

```
src/token_audit/
├── cli.py       # argparse CLI
├── github.py    # API inspection (secret never leaves this module)
└── report.py    # human + shareable rendering
tests/test_report.py
```

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">Part of the <a href="https://github.com/mehulpatel23b-pixel/osint-lab">OSINT Lab</a> toolkit · Built by <a href="https://github.com/mehulpatel23b-pixel">@mehulpatel23b-pixel</a></div>
