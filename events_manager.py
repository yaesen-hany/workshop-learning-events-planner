import re
import json
import os

FILE = "events.json"

def load_events():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Corrupted data file.")
            return []
    return []

def save_events():
    try:
        with open(FILE, "w", encoding="utf-8") as file:
            json.dump(events, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

events = load_events()

def get_events_by_category(category: str):
    if not isinstance(category, str):
        return []
    return [e for e in events if e.get("category", "").lower() == category.lower()]

def get_event_by_id(event_id: int):
    try:
        event_id = int(event_id)
    except (ValueError, TypeError):
        return None

    for event in events:
        if event["id"] == event_id:
            return event
    return None

def valid_input(text, data_type=str, min_val=None, max_val=None):
    while True:

        user_input = input(text).strip()
        if user_input.lower() == "q":
            raise KeyboardInterrupt
        if data_type == str:
            if not user_input:
                print("Invalid input! Value cannot be empty. Try again.")
                continue
            if not re.fullmatch(r"[A-Za-z ]+", user_input):
                print("Invalid input! Please enter letters only.")
                continue
            return user_input
        try:
            val = data_type(user_input)
            if min_val is not None and val < min_val:
                print(f"Invalid input! Value must be at least {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"Invalid input! Value must not exceed {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print(f"Invalid input! Please enter a valid {data_type.__name__}.")




def add_event(name: str, trainer: str, location: str, price: float,
              duration: int, rating: float, available_seats: int, category: str):
    new_id = max([e["id"] for e in events], default=100) + 1
    new_event = {
        "id": new_id,
        "name": name.strip(),
        "trainer": trainer.strip(),
        "location": location.strip(),
        "price": float(price),
        "duration": int(duration),
        "rating": float(rating),
        "available_seats": int(available_seats),
        "category": category.strip()}
    events.append(new_event)
    save_events()
    return new_event

def update_event(event_id: int, **kwargs):
    event = get_event_by_id(event_id)
    if event:
        for key, value in kwargs.items():
            if key in event and key != "id":
                event[key] = value
        save_events()
        return True
    return False

def delete_event(event_id: int):
    event = get_event_by_id(event_id)
    if event:
        events.remove(event)
        save_events()
        return True
    return False


def update_price(event_id: int, new_price: float):
    return update_event(event_id, price=float(new_price))


def update_available_seats(event_id: int, new_seats: int):
    return update_event(event_id, available_seats=int(new_seats))



def get_event_input():
    print("\n--- Add New Event ---")
    name = valid_input("Enter Event Name: ", str)
    trainer = valid_input("Enter Trainer Name: ", str)
    location = valid_input("Enter Location: ", str)
    price = valid_input("Enter Price: ", float, min_val=0.0)
    duration = valid_input("Enter Duration (hours): ", int, min_val=1)
    rating = valid_input("Enter Rating (0.0 to 5.0): ", float, min_val=0.0, max_val=5.0)
    seats = valid_input("Enter Available Seats: ", int, min_val=0)
    category = choose_category()
    created_event = add_event(name, trainer, location, price, duration, rating, seats, category)
    print(f"\nSuccess! Event added with ID: {created_event['id']}")
    return created_event


CATEGORIES = [
    "Programming",
    "AI",
    "Data",
    "Entrepreneurship",
    "Design",
    "Soft Skills"]
def choose_category():
    print("\n--- Categories ---")
    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")
    print(f"{len(CATEGORIES) + 1}. Add New Category")
    choice = valid_input("Select a category: ",int,min_val=1,max_val=len(CATEGORIES) + 1)
    if choice <= len(CATEGORIES):
        return CATEGORIES[choice - 1]
    new_category = valid_input("Enter New Category: ",str)
    CATEGORIES.append(new_category)
    print(f'Category "{new_category}" added successfully.')
    return new_category


def admin_menu():
    while True:
     try:
        print("\n==========================================")
        print("              ADMIN PANEL                 ")
        print("==========================================")
        print("1. Add New Event")
        print("2. Update Event Information")
        print("3. Update Event Price")
        print("4. Update Available Seats")
        print("5. Delete Event")
        print("6. View All Events")
        print("7. View Events by Category")
        print("8. Exit Admin Panel")
        choice = valid_input("Select an option (1-8): ", int, min_val=1, max_val=8)

        if choice == 1:
            get_event_input()
        elif choice == 2:
            print("\n--- Update Event Information ---")
            event_id = valid_input("Enter Event ID: ", int, min_val=100)
            event = get_event_by_id(event_id)
            while True:
              try:
                if event:
                    print(f"\nEditing Event: {event['name']} (ID: {event_id})")
                    print("1. Update Name")
                    print("2. Update Trainer")
                    print("3. Update Location")
                    print("4. Update Category")
                    print("5. Exit")

                    field_choice = valid_input("What do you want to update? (1-5): ", int, min_val=1, max_val=5)

                    if field_choice == 1:
                        new_name = valid_input("Enter New Event Name: ", str)
                        update_event(event_id, name=new_name)

                    elif field_choice == 2:
                        new_trainer = valid_input("Enter New Trainer Name: ", str)
                        update_event(event_id, trainer=new_trainer)

                    elif field_choice == 3:
                        new_location = valid_input("Enter New Location: ", str)
                        update_event(event_id, location=new_location)

                    elif field_choice == 4:
                         new_category = choose_category()
                         update_event(event_id, category=new_category)

                    elif field_choice == 5:
                        print("Exit.")
                        break

                    if field_choice in [1, 2, 3, 4]:
                        print("\nSuccess: Event information updated successfully.")
                else:
                    print("\nError: Event ID not found.")
                    continue
              except KeyboardInterrupt:
                    print("\nReturning to Update Event Information")
                    continue


        elif choice == 3:
            print("\n--- Update Event Price ---")
            event_id = valid_input("Enter Event ID: ", int, min_val=100)
            if get_event_by_id(event_id):
                new_price = valid_input("Enter New Price: ", float, min_val=0.0)
                update_price(event_id, new_price)
                print("\nSuccess: Price updated successfully.")
            else:
                print("\nError: Event ID not found.")

        elif choice == 4:
            print("\n--- Update Available Seats ---")
            event_id = valid_input("Enter Event ID: ", int, min_val=100)
            if get_event_by_id(event_id):
                new_seats = valid_input("Enter New Seats Count: ", int, min_val=0)
                update_available_seats(event_id, new_seats)
                print("\nSuccess: Seats updated successfully.")
            else:
                print("\nError: Event ID not found.")

        elif choice == 5:
            print("\n--- Delete Event ---")
            event_id = valid_input("Enter Event ID to delete: ", int, min_val=100)
            if delete_event(event_id):
                print("\nSuccess: Event deleted successfully.")
            else:
                print("\nError: Event ID not found.")

        elif choice == 6:
            print("\n--- All Registered Events ---")
            if not events:
                print("No events found.")
            else:
                for ev in events:
                    print(f"ID: {ev['id']} | Name: {ev['name']} | Category: {ev['category']} | Price: {ev['price']} LE | Seats: {ev['available_seats']}")


        elif choice == 7:
            print("\n--- View Events by Category ---")
            category_name = valid_input("Enter Category Name (e.g., Programming, Design, AI): ", str)
            filtered = get_events_by_category(category_name)
            if filtered:
                print(f"\n--- Events in Category: {category_name} ---")
                for ev in filtered:
                    print(f"ID: {ev['id']} | Name: {ev['name']} | Trainer: {ev['trainer']} | Price: {ev['price']} LE | Seats: {ev['available_seats']}")
            else:
                print(f"\nNo events found under category: '{category_name}'")
        elif choice == 8:
            print("\nExiting Admin Panel...")
            break
     except KeyboardInterrupt:
          print("\nReturning to Admin Menu...")
          continue



if __name__ == "__main__":
    admin_menu()
