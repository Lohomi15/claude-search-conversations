#!/usr/bin/env python3
"""Search past Claude Code conversations for a keyword and return surrounding context."""

import json
import sys
import os
import glob
import argparse
from datetime import datetime


PROJECTS_DIR = os.path.expanduser("~/.claude/projects")


def extract_text(msg):
    """Pull readable text out of a message entry (user or assistant)."""
    if not isinstance(msg, dict):
        return ""
    message = msg.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "text":
                parts.append(c.get("text", ""))
            elif c.get("type") == "tool_use":
                cmd = (c.get("input") or {}).get("command", "")
                parts.append(f"[tool_use {c.get('name','')}] {cmd}")
            elif c.get("type") == "tool_result":
                r = c.get("content", "")
                if isinstance(r, list):
                    r = " ".join(x.get("text", "") for x in r if isinstance(x, dict))
                parts.append(f"[tool_result] {r}")
        return "\n".join(parts)
    return ""


def load_session(path):
    """Load jsonl file into a list of entries."""
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return entries


def search(query, context=1, max_hits=None, snippet_chars=400):
    q = query.lower()
    files = sorted(glob.glob(os.path.join(PROJECTS_DIR, "*/*.jsonl")))
    results = []

    for path in files:
        entries = load_session(path)
        # index of turn-bearing entries (user/assistant with text)
        turns = [(i, e) for i, e in enumerate(entries)
                 if e.get("type") in ("user", "assistant")]

        for idx, (i, entry) in enumerate(turns):
            text = extract_text(entry)
            if not text or q not in text.lower():
                continue

            # grab surrounding turns for context
            start = max(0, idx - context)
            end = min(len(turns), idx + context + 1)
            window = turns[start:end]

            ts = entry.get("timestamp", "")
            session_id = entry.get("sessionId", os.path.basename(path).replace(".jsonl", ""))
            project = os.path.basename(os.path.dirname(path))

            snippet_lines = []
            for _, t in window:
                role = t.get("type", "?")
                txt = extract_text(t).strip().replace("\n", " ")
                if len(txt) > snippet_chars:
                    txt = txt[:snippet_chars] + "…"
                snippet_lines.append(f"  [{role}] {txt}")

            results.append({
                "session_id": session_id,
                "project": project,
                "path": path,
                "timestamp": ts,
                "snippet": "\n".join(snippet_lines),
            })

            if max_hits and len(results) >= max_hits:
                return results

    return results


def main():
    p = argparse.ArgumentParser(description="Search past Claude Code conversations.")
    p.add_argument("query", help="Keyword or phrase to search for (case-insensitive).")
    p.add_argument("-c", "--context", type=int, default=1,
                   help="Turns of context before/after each hit (default: 1).")
    p.add_argument("-n", "--max", type=int, default=20,
                   help="Max hits to return (default: 20).")
    p.add_argument("--chars", type=int, default=400,
                   help="Max chars per snippet line (default: 400).")
    args = p.parse_args()

    hits = search(args.query, context=args.context, max_hits=args.max,
                  snippet_chars=args.chars)

    if not hits:
        print(f"No matches for '{args.query}'.")
        return

    # sort newest first
    hits.sort(key=lambda h: h["timestamp"], reverse=True)

    print(f"Found {len(hits)} match(es) for '{args.query}':\n")
    for h in hits:
        ts = h["timestamp"]
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
        except ValueError:
            pass
        print(f"── {ts} | session {h['session_id'][:8]} | {h['project']}")
        print(h["snippet"])
        print(f"  → {h['path']}")
        print()


if __name__ == "__main__":
    main()
