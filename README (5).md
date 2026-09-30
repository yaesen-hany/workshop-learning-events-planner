# Workshops & Learning Events Planner

A Python console application that helps users discover workshops, bootcamps, and learning events, and build a personal learning plan with a live cost calculation.

## Features

- **Login & Registration** — Normal user and Administrator accounts, with a fixed admin login (`admin@gmail.com` / `admin123`).
- **Browse by Category** — Programming, AI, Data, Entrepreneurship, Design, Soft Skills.
- **Search** — find an event by name using binary search (O(log n)).
- **Sort** — sort events by price or duration, ascending or descending, using merge sort.
- **My Learning Plan** — add or remove events, view the full plan at any time.
- **Final Summary** — calculates total event fees, transportation cost, total learning hours, and the final plan cost, recalculated live whenever the plan changes.
- **Admin Panel** — add, update, delete events; update price and available seats.
- **Back Navigation** — a stack-based back button lets the user retrace their steps through the app.

## Project Structure

```
Workshops-Learning-Events-Planner/
│
├── main.py              # Entry point — runs the app and connects all modules
├── auth.py               # Login, registration, User class, navigation Stack
├── events_manager.py      # Event data, category browsing, admin CRUD
├── algorithm.py          # binary_search, merge_sort, sort_by_price, sort_by_duration
├── plan.py               # Learning plan management and final cost calculations
│
├── users.json            # Registered user accounts
├── events.json            # Event catalog
├── transportation.json    # Transportation cost matrix (per governorate → per event location)
└── learning_plan.json     # Each user's saved learning plan (keyed by national ID)
```

## How to Run

```bash
python main.py
```

You'll land on the Login page first. From there you can log in, register a new account, or exit.

**Admin login:**
```
Email: admin@gmail.com
Password: admin123
```

## Data Structures Used

| Structure | Used for |
|---|---|
| List of dicts | `events`, `users` |
| Dictionary | `learning_plan` (keyed by national ID), `transport_cost` (keyed by governorate) |
| Stack (list-based) | Back navigation between pages |

## Known Data Issues to Fix Before Submission

- `transportation.json` has both `"Cairo"` and `"cairo"` as separate keys (should be one, capitalized consistently) — same for `"fayoum"` vs `"Fayoum"`.
- `users.json` has a user with `"governorate": ""` (empty) — transportation cost will always be 0 for this user until it's filled in.
- Two users share the email `mai@gmail.com` with different passwords/national IDs — login will always match whichever one appears first in the file.
- Governorate names should stay consistent in capitalization across `users.json` and `transportation.json`, since lookups are case-sensitive.

## Team

Built as a team project — Project C: SkillQuest (Workshops & Learning Events Planner).
