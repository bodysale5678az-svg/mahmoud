# 🚗 Auto Parts Store — Management System

A complete **desktop application** for managing an auto parts store, built with **Python**, **Tkinter** and a clean **object-oriented** architecture.

---

## ✨ Features

- 🔐 **Authentication & Roles** — separate `Admin` and `Staff` accounts with different permissions
- 📦 **Inventory Management** — add, edit, delete and search car parts
- 👥 **Customer Management** — full customer records
- 💰 **Sales Tracking** — record sales and keep history
- 💾 **JSON Persistence** — data saved locally, no database server required
- 🖥️ **Full GUI** — built with Tkinter (tabs, tables, forms, messages)

---

## 🏗️ Architecture

The project follows **Object-Oriented Programming** principles:

```
User (ABC)
 ├── Admin
 └── Staff

Part        → inventory item (encapsulated with properties)
Customer    → customer record
AutoPartsStore       → business logic layer
AutoPartsStoreGUI    → presentation layer (Tkinter)
```

**Concepts applied:**
- Abstract Base Classes (`ABC`)
- Inheritance & polymorphism
- Encapsulation with `@property` getters
- Separation of concerns (logic vs UI)
- JSON serialization for persistence

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=flat-square&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=flat-square&logo=json&logoColor=white)

---

## 🚀 Getting Started

```bash
# No dependencies needed — Tkinter ships with Python
python pro.py
```

Data files are created automatically:
- `parts.json` — inventory
- `customers.json` — customers
- `sales.json` — sales records
- `users.json` — accounts

---

## 📸 Screenshots

_Coming soon_

---

## 👤 Author

**Mahmoud Saleh** — [@bodysale5678az-svg](https://github.com/bodysale5678az-svg)
