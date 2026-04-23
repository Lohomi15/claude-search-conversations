# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-04-23

### Added
- Initial release.
- `search.py` — case-insensitive substring search across all Claude Code conversations in `~/.claude/projects/`.
- `SKILL.md` — skill definition so Claude Code invokes the script on natural-language prompts like "where did we talk about X".
- Resume guidance: skill surfaces full session UUIDs with a `/resume <uuid>` hint.
- `--since` and `--until` date-range filters (YYYY-MM-DD) for scoping search to a time window.
- `update.sh` — helper that pulls the latest repo and syncs the skill into `~/.claude/skills/`, handling symlinked, copied, and fresh-install cases.
- Claude Code plugin manifest at `.claude-plugin/plugin.json` so the repo is installable via `/plugin install Lohomi15/claude-search-conversations`.
