import json
import os
from datetime import datetime

DATA_FILE = "contacts.json"

class ContactBook:
    def __init__(self):
        self.contacts = self._load()

    def _load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.contacts, f, indent=2)

    def add(self):
        print("\nLet's add someone new:")
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        email = input("Email (optional): ").strip() or None
        addr = input("Address (optional): ").strip() or None

        if not name or not phone:
            print("Name and phone can't be blank.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "address": addr,
            "created_at": now,
            "updated_at": now
        })
        self._save()
        print(f"Saved '{name}' to your contacts!")

    def show(self, filtered=None):
        records = filtered if filtered is not None else self.contacts
        if not records:
            print("\nNo contacts yet.")
            return

        print("\nYour People:")
        print(f"{'#':<3} | {'Name':<20} | {'Phone':<15} | {'Email':<25} | Last Updated")
        print("-" * 90)
        for i, c in enumerate(records, 1):
            print(f"{i:<3} | {c['name']:<20} | {c['phone']:<15} | "
                  f"{c['email'] or '—':<25} | {c['updated_at']}")

    def find(self):
        term = input("\nSearch name or number: ").strip().lower()
        if not term:
            print("No search term entered.")
            return
        results = [c for c in self.contacts if term in c["name"].lower() or term in c["phone"]]
        self.show(results)

    def edit(self):
        self.show()
        if not self.contacts: return
        try:
            idx = int(input("\nUpdate which one? #")) - 1
            c = self.contacts[idx]
        except:
            print("Invalid number.")
            return

        print(f"Editing {c['name']}:")
        name = input(f"Name [{c['name']}]: ").strip() or c["name"]
        phone = input(f"Phone [{c['phone']}]: ").strip() or c["phone"]
        email = input(f"Email [{c['email'] or '—'}]: ").strip() or c["email"]
        addr = input(f"Address [{c['address'] or '—'}]: ").strip() or c["address"]

        c.update({
            "name": name,
            "phone": phone,
            "email": email if email != '—' else None,
            "address": addr if addr != '—' else None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._save()
        print("Updated!")

    def remove(self):
        self.show()
        if not self.contacts: return
        try:
            idx = int(input("\nDelete which one? #")) - 1
            removed = self.contacts.pop(idx)
        except:
            print("Invalid selection.")
            return
        self._save()
        print(f"Deleted '{removed['name']}'")

    def menu(self):
        print("\n== Contact Book ==")
        print("1. Add")
        print("2. View")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Exit")

    def run(self):
        while True:
            self.menu()
            try:
                pick = input("\nPick an option (1–6): ").strip()
                if pick == "1": self.add()
                elif pick == "2": self.show()
                elif pick == "3": self.find()
                elif pick == "4": self.edit()
                elif pick == "5": self.remove()
                elif pick == "6":
                    print("Goodbye.")
                    break
                else:
                    print("Not sure what you meant. Try 1–6.")
            except KeyboardInterrupt:
                print("\nStopped by user.")
                break
            except Exception as e:
                print(f"\nOops: {e}")

if __name__ == "__main__":
    ContactBook().run()
