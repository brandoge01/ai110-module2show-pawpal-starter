# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling Features

- Time-Based Sorting: Sort tasks chronologically by their scheduled time (HH:MM format) for better visualization and planning
- Smart Filtering: Filter tasks by completion status (done/pending) and/or by pet name for targeted task management
- Recurring Task Management: Daily and weekly tasks automatically generate new occurrences when completed, with accurate date calculations using Python's `timedelta`
- Conflict Detection: Lightweight conflict detection identifies when multiple tasks overlap in time (same-pet or cross-pet), generating clear warnings instead of crashing
- Priority-Based Scheduling: Greedy algorithm that prioritizes high-importance tasks first while fitting as many as possible into the available time budget
- Detailed Explanations: Schedule generation includes reasoning for why tasks were included or skipped, helping owners understand the system's decisions

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
