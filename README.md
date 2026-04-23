# search-conversations

A Claude Code skill that searches your past conversations by keyword and helps you jump back into any matched session.

Every Claude Code chat is stored locally as JSONL in `~/.claude/projects/`. This skill searches across all of them, shows you matching snippets with context, and tells you exactly which session to `/resume`.

## Install

### As a Claude plugin (recommended)

Inside Claude Code:

```
/plugin install Lohomi15/claude-search-conversations
```

### Manual install

```bash
git clone https://github.com/Lohomi15/claude-search-conversations ~/.claude-search-conversations
mkdir -p ~/.claude/skills
cp -r ~/.claude-search-conversations/skills/search-conversations ~/.claude/skills/
```

## Usage

Just ask Claude Code naturally:

- "Where did we talk about the Postgres migration?"
- "Find the chat about the Coorg trip"
- "Which session did we design the auth flow in?"

Claude will invoke the skill, show matching conversations, and offer to resume the most relevant one.

You can also run the search script directly:

```bash
python3 ~/.claude/skills/search-conversations/search.py "postgres migration"
python3 ~/.claude/skills/search-conversations/search.py "auth flow" -c 2 -n 10
```

Flags:

- `-c N` — include N turns of context before/after each hit (default: 1)
- `-n N` — cap number of hits (default: 20)
- `--chars N` — truncate each snippet line to N chars (default: 400)

## Sample output

```
Found 3 match(es) for 'postgres migration':

── 2026-04-18 14:22 UTC | session 7a3f19cc | -Users-you-project
  [user] can you help me plan the postgres migration from rds to supabase
  [assistant] Sure — let's start by inventorying the tables that hold user data...
  → /Users/you/.claude/projects/-Users-you-project/7a3f19cc-....jsonl

── 2026-04-17 09:05 UTC | session 2b88a041 | -Users-you-project
  [assistant] The postgres migration plan we wrote yesterday is still the plan of record
  [user] great, let's run it
  → /Users/you/.claude/projects/-Users-you-project/2b88a041-....jsonl
```

To jump back into a matched session, copy its full UUID and run:

```
/resume 7a3f19cc-....
```

## How it works

1. Globs `~/.claude/projects/*/*.jsonl` — every Claude Code session you've ever had.
2. Extracts text from user and assistant turns (including tool use / tool result bodies).
3. Does a case-insensitive substring match.
4. Returns ranked snippets with session IDs, timestamps, and file paths.

It's all local. No network calls, no external dependencies.

## Requirements

- Claude Code
- Python 3.8+
- macOS or Linux

## License

MIT — see [LICENSE](./LICENSE).
