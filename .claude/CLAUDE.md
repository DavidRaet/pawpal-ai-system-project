# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**PawPal+** is an AI110 capstone project — a Streamlit app for daily pet care task scheduling, extended with an AI health advisor feature ("PawPal Preston") powered by the Gemini API.

## Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in GEMINI_API_KEY

# Run Streamlit UI
streamlit run app.py

# Run CLI demo (no UI, exercises the full backend)
python main.py

# Run tests
pytest -v

# Run a single test file
pytest tests/test_pawpal.py -v
```

## Architecture

Core backend lives entirely in `pawpal_system.py`. Key classes:

- **`Preferences`** — `reminder_time: str` for daily notifications
- **`Pet`** — `name`, `age`, `breed`, `species` (`Species` enum: `CAT/DOG/OTHER`)
- **`Owner`** — `name`, `preferences`, `pets: list[Pet]`; `add_pet()` appends
- **`Task`** — `title`, `duration_minutes`, `priority` (`Priority` enum), `status` (`Status` enum, default `PENDING`), `pet`, optional `time: datetime`
- **`Schedule`** — `tasks: list[Task]`, `description: str`
- **`PetCareService`** — singleton; `add_task`, `remove_task`, `update_task`, `get_tasks_for_pet`, `filter_tasks_by_status`, `filter_tasks_by_priority`, `generate_schedule`

**`generate_schedule()`** sorts all tasks by priority (`HIGH→MEDIUM→LOW`) and excludes `Status.COMPLETED` tasks. It does **not** assign times or check for time conflicts — that's a known limitation documented in `reflection.md`.

**`update_task()`** matches by object identity first, then falls back to matching by `title`.

**`GeminiClient`** (`geminiClient.py`) is a thin wrapper around `google-genai`. It reads `GEMINI_API_KEY` from the environment (via `.env`), merges system + user prompts into one string, and returns `""` on any error so callers can fall back to heuristic logic.

## Capstone Extension

`SPRINT.md` tracks the sprint (due 2026-04-27). The two outstanding deliverables are:

1. **AI feature** — implement "PawPal Preston" (pet health advisor) in `pawpal_system.py` using `GeminiClient`, wire into `app.py` and `main.py`
2. **Reliability / guardrail** — input validation, output guardrails, or a self-critique loop; add at least one test demonstrating it catching a bad case

Architecture diagram at `pawpalDiagrams/PawpalClassDiagram.mmd` needs updating once the AI components are added.

## Testing

Tests live in `tests/test_pawpal.py`. The `autouse` fixture resets the singleton (`PetCareService._instance = None`) before and after every test — always do this when adding new tests to avoid state bleed between test cases.
