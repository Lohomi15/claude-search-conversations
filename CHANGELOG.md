# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Candidate improvements (not yet implemented)
- **SQLite FTS5 index** — replace the full-scan substring search with an indexed store for faster queries on large archives. Would use Python stdlib `sqlite3`, no new deps.
- **BM25 ranking + recency boost** — rank results by relevance and decay older matches so "the recent chat where X was mentioned once" surfaces correctly.
- **Stemming** — "running" should match "run", "deploys" should match "deploy".
- **Codex session support** — extend the glob to include `~/.codex/sessions/**/*.jsonl` for users on both agents.
- **Incremental indexing** — mtime-based so re-queries don't re-scan unchanged sessions.
- **Regex mode** — optional `--regex` flag for power users.
- **Semantic search (`--semantic` flag)** — embed the query with a small local model (e.g., `sentence-transformers`) and rank by cosine similarity to find conceptually related turns, not just literal keyword matches. Adds a real dependency, so would stay opt-in.

## [1.0.1] - 2026-04-24

### Fixed
- `marketplace.json` — corrected `plugins[].source` to `{"source": "url", "url": "...git"}` format matching the actual Claude Code marketplace schema. Previous formats (`"./"` string and `{"type": "git", ...}` object) both caused parse errors.
- `marketplace.json` — added required top-level `name`, `description`, and `owner` fields.
- `plugin.json` — added explicit `skills` array with `name` + `path` fields.
- README install instructions updated to reflect two-step flow: `/plugin marketplace add` then `/plugin install search-conversations@claude-search-conversations`.

## [1.0.0] - 2026-04-23

### Added
- Initial release.
- `search.py` — case-insensitive substring search across all Claude Code conversations in `~/.claude/projects/`.
- `SKILL.md` — skill definition so Claude Code invokes the script on natural-language prompts like "where did we talk about X".
- Resume guidance: skill surfaces full session UUIDs with a `/resume <uuid>` hint.
- `--since` and `--until` date-range filters (YYYY-MM-DD) for scoping search to a time window.
- `update.sh` — helper that pulls the latest repo and syncs the skill into `~/.claude/skills/`, handling symlinked, copied, and fresh-install cases.
- Claude Code plugin manifest at `.claude-plugin/plugin.json` and marketplace declaration at `.claude-plugin/marketplace.json`.
