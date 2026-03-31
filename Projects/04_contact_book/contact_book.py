"""
Project — Contact Book
========================
A CRUD contact manager with: add/edit/delete/search, JSON persistence.
Skills: OOP, dataclasses, JSON, CLI
"""

import json, os
from dataclasses import dataclass, asdict, field
from typing import Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")

@dataclass
class Contact:
    name:    str
    phone:   str = ""
    email:   str = ""
    address: str = ""
    notes:   str = ""

    def matches(self, query: str) -> bool:
        q = query.lower()
        return any(q in v.lower() for v in [self.name, self.phone, self.email, self.address])

    def __str__(self) -> str:
        lines = [f"  👤 {self.name}"]
        if self.phone:   lines.append(f"     📞 {self.phone}")
        if self.email:   lines.append(f"     📧 {self.email}")
        if self.address: lines.append(f"     🏠 {self.address}")
        if self.notes:   lines.append(f"     📝 {self.notes}")
        return "\n".join(lines)


class ContactBook:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.contacts: dict[str, Contact] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath) as f:
                    for entry in json.load(f):
                        c = Contact(**entry)
                        self.contacts[c.name.lower()] = c
            except Exception:
                pass

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump([asdict(c) for c in self.contacts.values()], f, indent=2)

    def add(self, **kwargs) -> Contact:
        c = Contact(**kwargs)
        self.contacts[c.name.lower()] = c
        self._save()
        return c

    def delete(self, name: str) -> bool:
        key = name.lower()
        if key in self.contacts:
            del self.contacts[key]
            self._save()
            return True
        return False

    def search(self, query: str) -> list:
        return [c for c in self.contacts.values() if c.matches(query)]

    def list_all(self) -> list:
        return sorted(self.contacts.values(), key=lambda c: c.name.lower())

    def run(self):
        print("=" * 40)
        print("    📒  CONTACT BOOK")
        print("=" * 40)
        while True:
            print("\n  add | list | search | delete | quit")
            cmd = input("  > ").strip().lower()
            if cmd == "quit":
                print("  Goodbye! 👋"); break
            elif cmd == "add":
                name = input("  Name:    ").strip()
                if not name: continue
                phone   = input("  Phone:   ").strip()
                email   = input("  Email:   ").strip()
                address = input("  Address: ").strip()
                notes   = input("  Notes:   ").strip()
                c = self.add(name=name, phone=phone, email=email, address=address, notes=notes)
                print(f"\n  ✅ Saved:\n{c}")
            elif cmd == "list":
                contacts = self.list_all()
                if not contacts: print("  📭 No contacts."); continue
                for c in contacts:
                    print(f"\n{c}")
            elif cmd == "search":
                q = input("  Search: ").strip()
                results = self.search(q)
                if not results: print("  No matches.")
                for c in results: print(f"\n{c}")
            elif cmd == "delete":
                name = input("  Name to delete: ").strip()
                if self.delete(name):
                    print(f"  🗑️  Deleted '{name}'.")
                else:
                    print(f"  ⚠️  '{name}' not found.")
            else:
                print("  ⚠️  Unknown command.")

if __name__ == "__main__":
    ContactBook().run()
