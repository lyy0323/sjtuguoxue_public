#!/usr/bin/env python3
"""Batch submit poems via /api/submit/. Reads JSON array from stdin or file."""
import json
import sys
import time
import requests

DEFAULT_BASE = "https://sjtuguoxue.space"
LOCAL_BASE = "http://localhost:5052"


def submit_poems(poems: list[dict], base_url: str, api_key: str, dry_run: bool = False):
    results = []
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    # Track sequence groups: group_name -> last submitted uuid
    seq_prev: dict[str, str] = {}

    for i, poem in enumerate(poems):
        poem = dict(poem)  # don't mutate original
        seq_group = poem.pop("_sequence_group", None)

        # Auto-inject sequence relation from previous poem in same group
        if seq_group and seq_group in seq_prev:
            rels = list(poem.get("relations", []))
            rels.append({"id": seq_prev[seq_group], "type": "sequence"})
            poem["relations"] = rels

        label = f"[{i+1}/{len(poems)}] {poem.get('author','?')}·{poem.get('title','?')}"

        if dry_run:
            extra = f" (seq:{seq_group})" if seq_group else ""
            print(f"  {label}{extra} — dry run, skipped")
            results.append({"index": i, "ok": True, "dry_run": True, **poem})
            if seq_group:
                seq_prev[seq_group] = f"dry-run-{i}"
            continue

        try:
            resp = requests.post(f"{base_url}/api/submit/", json=poem, headers=headers, timeout=30)
            body = resp.json()
            ok = body.get("ok", False)
            symbol = "+" if ok else "!"
            detail = body.get("uuid", "") if ok else body.get("error", resp.text[:120])
            print(f"  {symbol} {label} — {detail}")
            results.append({"index": i, **body})
            if ok and seq_group:
                seq_prev[seq_group] = body["uuid"]
        except Exception as e:
            print(f"  ! {label} — {e}")
            results.append({"index": i, "ok": False, "error": str(e)})

        if not dry_run and i < len(poems) - 1:
            time.sleep(0.3)

    ok_count = sum(1 for r in results if r.get("ok"))
    print(f"\nDone: {ok_count}/{len(poems)} succeeded")
    return results


def main():
    import argparse
    p = argparse.ArgumentParser(description="Batch submit poems")
    p.add_argument("file", nargs="?", help="JSON file (omit for stdin)")
    p.add_argument("--base", default=DEFAULT_BASE, help=f"API base URL (default: {DEFAULT_BASE})")
    p.add_argument("--local", action="store_true", help=f"Use {LOCAL_BASE}")
    p.add_argument("--key", required=True, help="API key (sk-nyyy-...)")
    p.add_argument("--dry-run", action="store_true", help="Parse only, don't submit")
    args = p.parse_args()

    base = LOCAL_BASE if args.local else args.base

    if args.file:
        with open(args.file) as f:
            poems = json.load(f)
    else:
        poems = json.load(sys.stdin)

    if isinstance(poems, dict):
        poems = [poems]

    print(f"Submitting {len(poems)} poem(s) to {base}")
    if args.dry_run:
        print("(dry run)")

    results = submit_poems(poems, base, args.key, args.dry_run)
    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
