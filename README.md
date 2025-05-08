# 🍽️ Real-Time Menu Management System

A production-ready web application for restaurants to manage their menu in real-time and allow customers to order food seamlessly via mobile devices.

---

## 🚀 Features

### 👥 User Roles
- **Customer**: View menu, place orders, cancel orders, pay online, call the waiter.
- **Waiter/Staff**: Receive orders, serve tables, update status.
- **Admin**: Manage menu items, tables, staff, and transactions.

### 🔧 Functional Highlights
- Real-time menu updates across all user interfaces.
- QR-based customer access (scan to open menu).
- Role-based authentication and access control.
- Seamless ordering and digital payments (eSewa integration).
- Admin dashboard for restaurant configuration.

### 📡 Real-Time Sync
- Changes made by the admin (e.g., marking items unavailable) are reflected instantly on customer and waiter interfaces using WebSockets or Redis Pub/Sub mechanism.

---

## 🛠️ Tech Stack

| Layer        | Technology                 |
|--------------|-----------------------------|
| **Backend**  | Django (Python)             |
| **Frontend** | HTML, CSS                   |
| **Database** | SQLite (Development), MySQL (Production) |
| **Real-Time**| Django Channels + Redis (planned) |
| **Auth**     | Django’s built-in authentication |
| **Payment**  | eSewa integration           |

---


> Real-time updates are powered by Redis Pub/Sub or Django Channels (in production).

---

## 🧩 ER Diagram, Use Case, and Flow
Detailed system diagrams including:
- Block Diagram
- Use Case Diagram
- ER Diagram
- Sequence Diagram (planned)

> 📁 All design documentation is available in the `/docs/` directory.

---

## ✅ Non-Functional Requirements

- Secure role-based access and login
- Logging and monitoring (planned)
- Mobile responsive UI
- Scalable database design
- Modular Django app structure

---

## 🛠 Setup & Installation

```bash
git clone https://github.com/yourusername/menu-management-system.git
cd menu-management-system

# Create virtual environment and activate it
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```
## 👨‍💻 Contributors
- [Diya Shakya](https://github.com/diashakya)