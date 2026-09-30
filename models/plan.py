import json

# ---------- JSON Files: Load & Save ----------

def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def load_events():
    try:
        with open("events.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def load_transport():
    try:
        with open("transportation.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def load_learning_plans():
    try:
        with open("learning_plan.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_learning_plans(plan):
    with open("learning_plan.json", "w") as file:
        json.dump(plan, file, indent=4)

# def save_events():
#     try:
#         with open(EVENT_DATA, "w", encoding="utf-8") as file:
#             json.dump(events, file, ensure_ascii=False, indent=4)
#     except Exception as e:
#         print(f"Error saving data: {e}")


users = load_users()                    # list of dicts
events = load_events()                  # list of dicts
transport_cost = load_transport()       # dict
learning_plans = load_learning_plans()  # dict keyed by national_id (as string)


def find_user_by_national_id(national_id):
    target = str(national_id)
    for user in users:
        if str(user["national_id"]) == target:
            return user
    return None


def build_events_index():
    index = {}
    for event in events:
        index[event["id"]] = event
    return index


# ---------- Plan management ----------

def add_to_plan(event_id, national_id):
    user = find_user_by_national_id(national_id)
    if user is None:
        return False, "Invalid National ID"

    key = str(national_id)
    plan = learning_plans.setdefault(key, [])

    if event_id in plan:
        return False, f"Event {event_id} is already in your plan"

    if event_id not in build_events_index():
        return False, "Invalid event ID"

    plan.append(event_id)
    save_learning_plans(learning_plans)
    return True, f"Event {event_id} added to your plan"


def remove_from_plan(event_id, national_id):
    key = str(national_id)
    plan = learning_plans.get(key, [])

    if event_id not in plan:
        return False, "Event not found in your plan"

    plan.remove(event_id)
    save_learning_plans(learning_plans)
    return True, f"Event {event_id} removed from your plan"


def view_plan(national_id):
    """Returns a list of event dicts (data only — no printing here)."""
    user = find_user_by_national_id(national_id)
    if user is None:
        return None

    index = build_events_index()
    key = str(national_id)
    return [index[eid] for eid in learning_plans.get(key, []) if eid in index]


# ---------- Final calculations — non-iterative style (sum + generator, no explicit for-loop) ----------

def calculate_total_fees(national_id):
    plan_events = view_plan(national_id)
    if plan_events is None:
        return None
    return sum(event["price"] for event in plan_events)


def calculate_total_hours(national_id):
    plan_events = view_plan(national_id)
    if plan_events is None:
        return None
    return sum(event["duration"] for event in plan_events)


def calculate_transportation(national_id):
    plan_events = view_plan(national_id)
    if plan_events is None:
        return None

    user = find_user_by_national_id(national_id)
    user_government = user["governorate"]
    costs = transport_cost.get(user_government, {})

    return sum(costs.get(event["location"], 0) for event in plan_events)


def calculate_final_cost(national_id):
    """The main total — computed fresh from current data every call.
    Never hard-coded, and never rebuilt with an explicit loop."""
    fees = calculate_total_fees(national_id)
    transport = calculate_transportation(national_id)

    if fees is None or transport is None:
        return None

    return fees + transport


# ---------- Optional: formatted display for the user-facing plan view ----------

def format_plan_display(plan_events):
    if not plan_events:
        return "Your learning plan is empty."

    lines = ["=" * 40, "YOUR LEARNING PLAN", "=" * 40]
    for i, event in enumerate(plan_events, start=1):
        lines.append(f"{i}. {event['name']}")
        lines.append(f"   Trainer: {event['trainer']}")
        lines.append(f"   Location: {event['location']}")
        lines.append(f"   Price: {event['price']} EGP")
        lines.append(f"   Duration: {event['duration']} hrs")
        lines.append("-" * 40)
    return "\n".join(lines)
