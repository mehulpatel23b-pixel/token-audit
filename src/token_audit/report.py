"""Output rendering — human and shareable-safe formats."""


def human(result):
    lines = [
        "GitHub Token Audit",
        "=" * 40,
        f"Token       : {result['masked']}",
        f"Valid       : {result['valid']}",
        f"User        : {result['user'] or '-'}",
        f"Type        : {result['type']}",
        f"Scopes      : {', '.join(result['scopes']) or '(none / fine-grained)'}",
        f"Rate core   : {result['rate'].get('core', '-')}",
        f"Rate search : {result['rate'].get('search', '-')}",
    ]
    if result["notes"]:
        lines.append("")
        lines.extend(f"  ! {n}" for n in result["notes"])
    return "\n".join(lines)


def shareable(result):
    """A report safe to paste publicly: no token material, no identity."""
    lines = [
        "Token permission profile (safe to share)",
        "=" * 40,
        f"Valid  : {result['valid']}",
        f"Type   : {result['type']}",
        f"Scopes : {', '.join(result['scopes']) or '(fine-grained)'}",
    ]
    return "\n".join(lines)
