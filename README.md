# 🚀 Django Starter Project

A beginner-friendly Django project setup with virtual environment configuration, migrations, superuser creation, and local development server setup.

---

## 📌 Features

* Django project initialization
* Virtual environment setup
* Database migrations
* Django admin panel
* Local development server
* Beginner-friendly workflow

---

# 🛠️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/DevXtechnic/ojt10.git
cd ojt10
```

---

# 🐍 Create & Activate Virtual Environment

## Install Required Packages

```bash
pip install virtualenv django
```

## Create Virtual Environment

```bash
virtualenv env
```

OR

```bash
python -m virtualenv env
```

## Activate Virtual Environment

### Linux / macOS

```bash
source env/bin/activate
```

### Windows

```bash
env\Scripts\activate
```

---

# ⚡ Create Django Project

```bash
django-admin startproject firstproject
```

---

# 🗄️ Run Database Migrations

```bash
python manage.py migrate
```

---

# 👤 Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin credentials.

---

# ▶️ Run Development Server

```bash
python manage.py runserver
```

Now open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Django Admin Panel

Access the admin dashboard here:

```text
http://127.0.0.1:8000/admin
```

Login using the superuser credentials you created earlier.

---

# 📂 Project Structure

```bash
ojt10/
│── env/
│── firstproject/
│── manage.py
│── db.sqlite3
```

---

# 📚 Useful Django Commands

| Command                             | Description               |
| ----------------------------------- | ------------------------- |
| `python manage.py runserver`        | Start development server  |
| `python manage.py migrate`          | Apply database migrations |
| `python manage.py makemigrations`   | Create migration files    |
| `python manage.py createsuperuser`  | Create admin user         |
| `python manage.py startapp appname` | Create a new Django app   |

---

# 🧠 Tech Stack

* Python
* Django
* SQLite
* Virtualenv

---
