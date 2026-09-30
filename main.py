import auth
import events_manager as em
import algorithm as algo
import plan
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"
def refresh_plan_data():
    plan.users = plan.load_users()
    plan.events = plan.load_events()
    plan.transport_cost = plan.load_transport()
    plan.learning_plans = plan.load_learning_plans()
def find_user_by_email(email, password):
    data = auth.load_data(auth.USERS_DATA)
    for user in data:
        if user["email"] == email and user["password"] == password:
            return user
    return None
def display_events(events_list):
    if not events_list:
        print("No events found.")
        return
    print("------------------------------------------")
    for event in events_list:
        print(
            f"ID: {event['id']} | {event['name']} | Trainer: {event['trainer']} | "
            f"Location: {event['location']} | Price: {event['price']} EGP | "
            f"Duration: {event['duration']}h | Rating: {event['rating']} | "
            f"Seats: {event['available_seats']}"
        )
    print("------------------------------------------")
def login_page(nav_stack):
    print("==========================================")
    print("                LOGIN PAGE")
    print("==========================================")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    choice = input("Select an option: ").strip()
    if choice == "1":
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            return "admin_panel", {"name": "Administrator", "role": "admin"}
        user = find_user_by_email(email, password)
        if user is None:
            print("Invalid email or password.")
            return "login", None
        if user.get("role") == "admin":
            return "admin_panel", user
        return "home", user
    if choice == "2":
        return "register", None
    if choice == "3":
        return "end", None
    print("Invalid option.")
    return "login", None
def register_page():
    print("==========================================")
    print("              REGISTRATION PAGE")
    print("==========================================")
    auth.register_user()
    print("Registration completed. Please login now.")
    return "login"
def home_page(nav_stack, state):
    user = state["user"]
    print("==========================================")
    print(f"Welcome {user['name']}")
    print("            HOME / CATEGORIES")
    print("==========================================")
    for index, category in enumerate(em.CATEGORIES, start=1):
        print(f"{index}. {category}")
    plan_option = len(em.CATEGORIES) + 1
    print(f"{plan_option}. My Learning Plan")
    print("0. Logout")
    choice = input("Select an option: ").strip()
    if choice == "0":
        return "login", None
    if not choice.isdigit():
        print("Invalid option.")
        return "home", state
    choice_num = int(choice)
    if choice_num == plan_option:
        nav_stack.push("home")
        return "my_plan", state
    if 1 <= choice_num <= len(em.CATEGORIES):
        state["category"] = em.CATEGORIES[choice_num - 1]
        nav_stack.push("home")
        return "category_list", state
    print("Invalid option.")
    return "home", state
def category_list_page(nav_stack, state):
    category = state["category"]
    events_in_category = [e for e in em.load_events() if e["category"] == category]
    print("==========================================")
    print(f"           {category} EVENTS")
    print("==========================================")
    print("1. View Default Order")
    print("2. Sort by Price")
    print("3. Sort by Duration")
    print("4. Search by Name")
    print("0. Back")
    choice = input("Select an option: ").strip()
    if choice == "0":
        page = nav_stack.pop()
        return page or "home", state
    if choice == "1":
        display_events(events_in_category)
    elif choice == "2":
        order = input("Ascending or Descending (a/d): ").strip().lower()
        display_events(algo.sort_by_price(events_in_category, ascending=order != "d"))
    elif choice == "3":
        order = input("Ascending or Descending (a/d): ").strip().lower()
        display_events(algo.sort_by_duration(events_in_category, ascending=order != "d"))
    elif choice == "4":
        name = input("Enter event name to search: ").strip()
        found = algo.binary_search(events_in_category, name)
        if found:
            display_events([found])
        else:
            print("No event found with that name.")
    else:
        print("Invalid option.")
        return "category_list", state
    detail_id = input("Enter Event ID to view details, or press Enter to stay: ").strip()
    if detail_id.isdigit():
        chosen_event = em.get_event_by_id(int(detail_id))
        if chosen_event and chosen_event["category"] == category:
            nav_stack.push("category_list")
            state["event"] = chosen_event
            return "event_detail", state
        print("Event ID not found in this category.")
    return "category_list", state
def event_detail_page(nav_stack, state):
    event = state["event"]
    print("==========================================")
    print("               EVENT DETAILS")
    print("==========================================")
    print(f"ID: {event['id']}")
    print(f"Name: {event['name']}")
    print(f"Trainer: {event['trainer']}")
    print(f"Location: {event['location']}")
    print(f"Price: {event['price']} EGP")
    print(f"Duration: {event['duration']} hours")
    print(f"Rating: {event['rating']}")
    print(f"Available Seats: {event['available_seats']}")
    print(f"Category: {event['category']}")
    print("1. Add to My Learning Plan")
    print("2. Remove from My Learning Plan")
    print("0. Back")
    choice = input("Select an option: ").strip()
    if choice == "0":
        page = nav_stack.pop()
        return page or "category_list", state
    if choice == "1":
        refresh_plan_data()
        success, message = plan.add_to_plan(event["id"], state["user"]["national_id"])
        print(message)
    elif choice == "2":
        refresh_plan_data()
        success, message = plan.remove_from_plan(event["id"], state["user"]["national_id"])
        print(message)
    else:
        print("Invalid option.")
    return "event_detail", state
def my_plan_page(nav_stack, state):
    refresh_plan_data()
    national_id = state["user"]["national_id"]
    plan_events = plan.view_plan(national_id)
    print(plan.format_plan_display(plan_events))
    if plan_events:
        print("1. Remove an Event from Plan")
        print("2. View Final Summary")
    print("0. Back")
    choice = input("Select an option: ").strip()
    if choice == "0":
        page = nav_stack.pop()
        return page or "home", state
    if choice == "1" and plan_events:
        event_id = input("Enter Event ID to remove: ").strip()
        if event_id.isdigit():
            success, message = plan.remove_from_plan(int(event_id), national_id)
            print(message)
    elif choice == "2" and plan_events:
        nav_stack.push("my_plan")
        return "final_summary", state
    return "my_plan", state
def final_summary_page(nav_stack, state):
    refresh_plan_data()
    national_id = state["user"]["national_id"]
    fees = plan.calculate_total_fees(national_id)
    hours = plan.calculate_total_hours(national_id)
    transport = plan.calculate_transportation(national_id)
    final_cost = plan.calculate_final_cost(national_id)
    print("==========================================")
    print("         MY LEARNING PLAN SUMMARY")
    print("==========================================")
    print(f"Total Event Fees: {fees} EGP")
    print(f"Total Transportation Cost: {transport} EGP")
    print(f"Total Learning Hours: {hours} hours")
    print(f"Final Learning Plan Cost: {final_cost} EGP")
    print("0. Back")
    input("Press Enter to continue: ")
    page = nav_stack.pop()
    return page or "my_plan", state
def admin_panel_page(state):
    print("==========================================")
    print(f"Welcome {state['user']['name']}")
    print("==========================================")
    em.admin_menu()
    return "login", None
def run():
    nav_stack = auth.Stack()
    page = "login"
    state = None
    while True:
        if page == "login":
            page, result = login_page(nav_stack)
            if page == "home":
                state = {"user": result, "category": None, "event": None}
            elif page == "admin_panel":
                state = {"user": result}
        elif page == "register":
            page = register_page()
        elif page == "home":
            page, state = home_page(nav_stack, state)
        elif page == "category_list":
            page, state = category_list_page(nav_stack, state)
        elif page == "event_detail":
            page, state = event_detail_page(nav_stack, state)
        elif page == "my_plan":
            page, state = my_plan_page(nav_stack, state)
        elif page == "final_summary":
            page, state = final_summary_page(nav_stack, state)
        elif page == "admin_panel":
            page, state = admin_panel_page(state)
        elif page == "end":
            print("Goodbye.")
            break
        else:
            page = "login"
if __name__ == "__main__":
    run()
