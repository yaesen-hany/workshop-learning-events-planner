# Workshops & Learning Events Planner

A modular Python command-line application for discovering workshops, bootcamps, and learning events, and for building a personal learning plan with live cost calculation. Developed as **Project C (SkillQuest)** of the Samsung Innovation Campus program.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Sample Session](#sample-session)
- [Application Flow](#application-flow)
- [Design Notes](#design-notes)
- [Known Issues](#known-issues)
- [Roadmap](#roadmap)
- [Team](#team)

## Overview

Users browse events by category, search and sort them with custom-implemented algorithms, and add selected events to a personal plan. Each time the plan changes, the application recalculates:

- Total event fees
- Transportation cost (based on the user's governorate and the event location)
- Total learning hours
- Final plan cost

Administrators use a separate panel to manage the event catalog.

## Features

| Area | Description |
|---|---|
| Authentication | Registration and login for standard users and administrators |
| Browsing | Six categories: Programming, AI, Data, Entrepreneurship, Design, Soft Skills |
| Search | Find an event by name using binary search, O(log n) |
| Sorting | Sort by price or duration, ascending or descending, using merge sort, O(n log n) |
| Event details | Trainer, location, price, duration, rating, and available seats |
| Learning plan | Add and remove events; view the full plan at any time |
| Final summary | Fees, transportation, hours, and total cost, recalculated on every change |
| Administration | Add, update, and delete events; update price and available seats |
| Navigation | Stack-based back button that retraces the user's path |

## Project Structure

```
workshop-learning-events-planner/
├── main.py        # Entry point: page router and user-facing pages
├── models/        # Core modules: auth, events_manager, algorithm, plan
├── data/          # JSON data files
├── .gitignore
└── .gitattributes
```

### Modules

| Module | Responsibility |
|---|---|
| `auth` | Login, registration, `User` class, navigation `Stack` |
| `events_manager` | Event catalog, categories, administrator CRUD operations |
| `algorithm` | `binary_search`, `merge_sort`, `sort_by_price`, `sort_by_duration` |
| `plan` | Learning plan management and cost calculations |

### Data Files

| File | Content |
|---|---|
| `users.json` | Registered user accounts |
| `events.json` | Event catalog |
| `transportation.json` | Transportation cost matrix (user governorate to event location) |
| `learning_plan.json` | Saved plans, keyed by national ID |

## Getting Started

### Requirements

- Python 3.8 or later
- No third-party packages

### Installation and Usage

```bash
git clone https://github.com/yaesen-hany/workshop-learning-events-planner.git
cd workshop-learning-events-planner
python main.py
```

The application opens on the login page, where you can log in, register, or exit.

### Demo Administrator Account

For testing purposes only:

| Field | Value |
|---|---|
| Email | `admin@gmail.com` |
| Password | `admin123` |

> **Security note:** hard-coded credentials are acceptable in a learning project but must not be used in production. See the [Roadmap](#roadmap).

## Sample Session

The excerpt below shows the console output format. Event names, prices, and totals are illustrative.

```
==========================================
 HOME / CATEGORIES
==========================================
1. Programming
2. AI
3. Data
4. Entrepreneurship
5. Design
6. Soft Skills
7. My Learning Plan
0. Logout
Select an option: 1

==========================================
 Programming EVENTS
==========================================
1. View Default Order
2. Sort by Price
3. Sort by Duration
4. Search by Name
0. Back
Select an option: 2
Ascending or Descending (a/d): a
------------------------------------------
ID: 3 | Python Basics | Trainer: Sara Ali | Location: Cairo | Price: 500 EGP | Duration: 12h | Rating: 4.6 | Seats: 20
ID: 1 | Web Bootcamp | Trainer: Omar Nabil | Location: Giza | Price: 1200 EGP | Duration: 40h | Rating: 4.8 | Seats: 15
------------------------------------------

==========================================
 MY LEARNING PLAN SUMMARY
==========================================
Total Event Fees: 1700 EGP
Total Transportation Cost: 120 EGP
Total Learning Hours: 52 hours
Final Learning Plan Cost: 1820 EGP
```

## Application Flow

```
Login ─┬─> Home (Categories) ─┬─> Category List ──> Event Details
       │                      └─> My Learning Plan ──> Final Summary
       ├─> Register
       └─> Admin Panel (administrators only)
```

Each page pushes the previous page onto a stack. Selecting `0. Back` pops the stack and returns the user to where they came from.

## Design Notes

### Data Structures

| Structure | Used for |
|---|---|
| List of dictionaries | Events and users |
| Dictionary | Learning plans (keyed by national ID); transportation costs (keyed by governorate) |
| Stack (list-based) | Back navigation |

### Algorithms

- **Binary search** requires input sorted by name, so the event list is sorted by name before each search.
- **Merge sort** is stable: events with equal price or duration retain their original relative order.

## Known Issues

The following data problems should be resolved before submission:

1. `transportation.json` contains both `"Cairo"` and `"cairo"`, and both `"fayoum"` and `"Fayoum"`, as separate keys. Merge each pair into a single, consistently capitalized key.
2. One user in `users.json` has an empty `governorate`, so their transportation cost is always 0. Populate the value and validate it at registration.
3. Two users share the email `mai@gmail.com` with different passwords and national IDs. Login matches the first entry in the file. Enforce unique emails at registration.
4. Governorate lookups are case-sensitive. Keep capitalization consistent across `users.json` and `transportation.json`, or normalize values with `.strip().title()` at lookup time.

## Roadmap

- Store passwords as salted hashes (`hashlib` or `bcrypt`) instead of plain text.
- Validate input: 14-digit national ID, email format, non-empty governorate.
- Prevent duplicate events in a plan and verify seat availability before adding.
- Decrement available seats when a plan is confirmed.
- Move administrator credentials out of `main.py` into configuration or the user data.

## Team

Developed as a team project for Samsung Innovation Campus, Project C: SkillQuest (Workshops & Learning Events Planner).

## License

Created for educational purposes.
