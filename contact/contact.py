# Contact Book Application

import json
import os

contacts = []  # List to store contact dictionaries
CONTACTS_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")


def load_contacts():
    """Load contacts from a JSON file into the global contacts list.

    If the file does not exist or is invalid, start with an empty list.
    """
    global contacts
    try:
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    contacts = data
    except Exception:
        # If loading fails, keep contacts as empty list; don't crash the app.
        contacts = []


def save_contacts():
    """Save the current contacts list to a JSON file."""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
    except Exception:
        # Best-effort persistence; ignore save errors for now.
        pass


def add_contact():
    print("\n===== ADD NEW CONTACT =====")
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()
    address = input("Enter Address: ").strip()

    if not name:
        print("⚠️ Name cannot be empty. Contact not added.\n")
        return

    contact = {"Name": name, "Phone": phone, "Email": email, "Address": address}
    contacts.append(contact)
    save_contacts()
    print(f"✅ Contact '{name}' added successfully!\n")


def view_contacts():
    print("\n===== CONTACT LIST =====")
    if not contacts:
        print("No contacts found.")
        return

    for i, contact in enumerate(contacts, start=1):
        print(f"{i}. {contact['Name']} - {contact['Phone']}")
    print()


def search_contact():
    print("\n===== SEARCH CONTACT =====")
    keyword = input("Enter name or phone number to search: ").strip().lower()

    matches = []
    for contact in contacts:
        if keyword in contact.get("Name", "").lower() or keyword in contact.get("Phone", ""):
            matches.append(contact)

    if not matches:
        print("❌ Contact not found.\n")
        return

    print(f"\n--- {len(matches)} Contact(s) Found ---")
    for contact in matches:
        print(f"Name: {contact.get('Name')}")
        print(f"Phone: {contact.get('Phone')}")
        print(f"Email: {contact.get('Email')}")
        print(f"Address: {contact.get('Address')}\n")


def update_contact():
    print("\n===== UPDATE CONTACT =====")
    name = input("Enter the name of the contact to update: ").strip().lower()

    for contact in contacts:
        if contact.get("Name", "").lower() == name:
            print("Enter new details (leave blank to keep current value):")
            new_phone = input(f"New Phone ({contact.get('Phone','')}): ").strip() or contact.get('Phone')
            new_email = input(f"New Email ({contact.get('Email','')}): ").strip() or contact.get('Email')
            new_address = input(f"New Address ({contact.get('Address','')}): ").strip() or contact.get('Address')

            contact['Phone'] = new_phone
            contact['Email'] = new_email
            contact['Address'] = new_address
            save_contacts()

            print(f"✅ Contact '{contact.get('Name')}' updated successfully!\n")
            return
    print("❌ Contact not found.\n")


def delete_contact():
    print("\n===== DELETE CONTACT =====")
    name = input("Enter the name of the contact to delete: ").strip().lower()

    for contact in contacts:
        if contact.get("Name", "").lower() == name:
            contacts.remove(contact)
            save_contacts()
            print(f"🗑️ Contact '{contact.get('Name')}' deleted successfully!\n")
            return
    print("❌ Contact not found.\n")


def main_menu():
    # Ensure contacts are loaded when menu starts
    load_contacts()
    while True:
        print("===== CONTACT BOOK MENU =====")
        print("1. Add Contact")
        print("2. View Contact List")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("👋 Exiting Contact Book. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.\n")


# Run the application
if __name__ == "__main__":
    main_menu()
