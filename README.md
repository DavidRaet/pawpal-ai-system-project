# PawPal+

A Streamlit app for daily pet care task scheduling.

## Overview

- Lets an owner register pets, add care tasks (walks, feeding, meds, etc.), and generate a prioritized daily schedule.
- All task management and scheduling logic is handled by a single `PetCareService` singleton.
- Features PawPal Preston: an AI petcare assistant that can answer user's questions on their pet's health, behavior, or diet.
- Stack: Python · Streamlit · pytest



## Architecture

### Enums

| Enum | Values |
|------|--------|
| `Species` | `CAT`, `DOG`, `OTHER` |
| `Priority` | `HIGH`, `MEDIUM`, `LOW` |
| `Status` | `PENDING`, `COMPLETED`, `SKIPPED` |

### Classes

| Class | Attributes | Key Methods | Role |
|-------|-----------|-------------|------|
| `Preferences` | `reminder_time` | — | Owner-level scheduling settings |
| `Pet` | `name`, `age`, `breed`, `species` | — | Represents a single pet |
| `Owner` | `name`, `preferences`, `pets[]` | `add_pet()` | Links an owner to their pets |
| `Task` | `title`, `duration_minutes`, `priority`, `pet`, `time`, `status` | — | A schedulable pet-care activity |
| `Schedule` | `tasks[]`, `description` | — | Output of the scheduling algorithm |
| `PetCareService` | `tasks[]` (singleton) | `add_task()`, `remove_task()`, `update_task()`, `get_tasks_for_pet()`, `filter_tasks_by_status()`, `filter_tasks_by_priority()`, `generate_schedule()` | Singleton; manages all tasks and produces schedules |
| `PrestonAdvisor` | `_client (GeminiClient)`, `MAX_QUESTION_LENGTH` | `ask(question, pet)` | AI pet-care advisor for cats and dogs; includes input/output guardrails and appends a disclaimer |

---

## Scheduling Algorithm

`PetCareService.generate_schedule()`:

1. Filters out any tasks with `Status.COMPLETED`.
2. Sorts remaining tasks by priority: `HIGH` → `MEDIUM` → `LOW`.
3. Returns a `Schedule` containing the ordered task list and a summary description string.

---


## NEW FEATURE: PawPal Preston 

`class PrestonAdvisor`:

1. Accepts health, behavior, or diet questions about a registered pet — cats and dogs only.
2. Validates input before calling the model: rejects empty questions, questions over 500 characters, and questions about `Species.OTHER` pets (returns a polite redirect to a specialist veterinarian instead).
3. Builds a system prompt grounded in trusted veterinary sources (VCA, AVMA, Cornell, AKC, PetMD) and a user prompt that includes the pet's name, age, breed, and species.
4. Sends the combined prompt to `GeminiClient` (`gemma-3-27b-it`, temperature `0.2`) and receives the model's response.
5. Validates the response before returning it: if the reply is empty or fewer than 20 characters, returns a fallback message directing the user to their veterinarian.
6. Appends a standard disclaimer to every valid response reminding users to consult a licensed veterinarian for personalized advice.



---

## Sample Input / Output

### Schedule generation

Running `python main.py` with owner John Doe, pets Buddy (Golden Retriever, 5 y/o) and Mittens (Siamese, 3 y/o), and six tasks (one of which is already `COMPLETED`):

```
Generated Schedule:
  - Vet appointment for Buddy — HIGH priority · 45 min · pending
  - Walk Buddy                — MEDIUM priority · 60 min · pending
  - Feed Mittens              — MEDIUM priority · 20 min · pending
  - Play with Mittens         — LOW priority · 40 min · pending
  - Groom Mittens             — LOW priority · 30 min · pending
```

> "Feed Buddy" was added with `Status.COMPLETED` and is excluded from the schedule.

---

### PawPal Preston — valid question

**Input**
> Pet: Buddy (Golden Retriever, 5 y/o, DOG)
> Question: *"Buddy has been scratching his ears a lot. What could be causing this?"*

**Output (truncated)**
> Ear scratching in dogs is most commonly caused by ear infections (bacterial or yeast), ear mites, allergies (environmental or food-related), or a foreign object in the ear canal. Golden Retrievers are prone to ear infections due to their floppy ears, which reduce airflow. Signs of infection include redness, odor, or dark discharge — if you notice any of these, a vet visit is recommended.
>
> *Sources: VCA Animal Hospitals, AKC Health*
>
> ---
> *PawPal Preston covers general health, behavior, and diet information for dogs and cats only. For personalized advice, always consult a licensed veterinarian.*

---

### PawPal Preston — guardrail triggered

**Input**
> Pet: Whiskers (Hamster, `Species.OTHER`)
> Question: *"What vegetables can my hamster eat?"*

**Output**
> Preston specializes in dogs and cats. For Whiskers, please consult a veterinarian who specializes in exotic or small animals.

---

<div>
    <a href="https://www.loom.com/share/1993bba5a3ef4a09a146e94bc1055f80">
      <h2>PawPal Preston Demo - Watch Video</h2>
    </a>
    <a href="https://www.loom.com/share/1993bba5a3ef4a09a146e94bc1055f80">
      <img style="max-width:600;" src="https://cdn.loom.com/sessions/thumbnails/1993bba5a3ef4a09a146e94bc1055f80-f14462d944bdb600-full-play.gif#t=0.1">
    </a>
  </div>


## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```


## Running with Gemini

### 1. Set up your API key

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_real_key_here
```

### 3. Run the app

**Streamlit UI:**
```bash
streamlit run app.py
```

**CLI demo (no UI — exercises the full backend including PawPal Preston):**
```bash
python main.py
```




## Running Tests

Tests focus on **reliability logic** and **agent behavior**, not the UI.

```bash
pytest
```
Tests live in `tests/test_pawpal.py` and cover: singleton behavior, task add/remove, priority ordering, completed-task exclusion, and per-pet filtering.
