# Python + Django Notes

A concise reference for learning backend development using Python and Django.

---

# What is Django?

Django is a high-level Python web framework used to build web applications efficiently. It follows the **MVT (Model-View-Template)** architectural pattern and provides many built-in tools for rapid development.

Key built-in features include:

- URL routing
- ORM (Object Relational Mapping)
- Authentication system
- Admin panel
- Security protections
- Template engine

---

# Why Django?

Django is widely used because it allows developers to create web applications quickly while maintaining clean project structure.

## Advantages

- Rapid development
- Secure by default
- Scalable
- Clean architecture
- Built-in admin interface
- Strong documentation
- Python-based syntax

---

# Python Prerequisites

Before learning Django, these Python concepts should be understood:

## Essential Topics

- Variables
- Data types
- Operators
- Functions
- Loops
- Conditional statements
- Lists
- Tuples
- Dictionaries
- File handling
- Modules
- Classes and objects
- OOP basics
- Exception handling
- Virtual environments
- Package management (`pip`)

## Example

```python
def greet(name):
	return f"Hello, {name}"
```

---

# Installing Django

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Django

```bash
pip install django
```

## Check Installed Version

```bash
python -m django --version
```

---

# Creating a Django Project

```bash
django-admin startproject myproject
```

Generated structure:

```text
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
```

---

# Important Files

| File | Purpose |
|---|---|
| `manage.py` | Project command utility |
| `settings.py` | Configuration settings |
| `urls.py` | URL declarations |
| `asgi.py` | ASGI deployment |
| `wsgi.py` | WSGI deployment |

---

# Project vs App

## Project

The complete web application.

## App

A module inside the project that handles a specific functionality.

Example:

- Project = School management system
- App = Students
- App = Attendance
- App = Teachers

Create app:

```bash
python manage.py startapp students
```

---

# Common Django Commands

## Run Development Server

```bash
python manage.py runserver
```

Default address:

```text
http://127.0.0.1:8000
```

## Create Migrations

```bash
python manage.py makemigrations
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

---

# MVT Architecture

Django follows the **MVT pattern**.

## Model

Handles database structure.

## View

Handles application logic.

## Template

Handles user interface rendering.

Request flow:

```text
User Request
	↓
URL
	↓
View
	↓
Model
	↓
Template
	↓
Response
```

---

# Models

Models define database tables.

Example:

```python
from django.db import models

class Student(models.Model):
	name = models.CharField(max_length=100)
	age = models.IntegerField()
```

## Notes

- Each class represents a table
- Each field represents a column
- Django ORM manages SQL operations internally

---

# Views

Views process requests and return responses.

Example:

```python
from django.http import HttpResponse

def home(request):
	return HttpResponse("Django page")
```

---

# URL Routing

Maps URLs to views.

Example:

```python
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
]
```

---

# Templates

Templates are HTML files used for frontend rendering.

Example:

```html
<h1>{{ title }}</h1>
```

---

# Template Syntax

## Variables

```html
{{ variable }}
```

## Loop

```html
{% for student in students %}
	<p>{{ student.name }}</p>
{% endfor %}
```

## Condition

```html
{% if user %}
	<p>Logged in</p>
{% endif %}
```

---

# Django ORM

ORM allows database interaction using Python code.

## Create

```python
Student.objects.create(name="Neo", age=16)
```

## Read

```python
Student.objects.all()
```

## Filter

```python
Student.objects.filter(age=16)
```

## Delete

```python
student.delete()
```

---

# Admin Panel

Django includes a built-in administration interface.

Register model:

```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

Access:

```text
/admin
```

---

# Database

Default database:

```text
SQLite
```

Suitable for:

- Learning
- Testing
- Small applications

Common production database:

- PostgreSQL

---

# Static Files

Used for frontend assets:

- CSS
- JavaScript
- Images

Directory:

```text
static/
```

---

# Media Files

Used for uploaded content.

Examples:

- Images
- Documents
- PDFs

Directory:

```text
media/
```

---

# Forms

Django forms simplify input validation.

Example:

```python
from django import forms

class StudentForm(forms.Form):
	name = forms.CharField()
```

---

# Authentication

Django provides built-in authentication tools.

Features:

- Login
- Logout
- Signup
- Password reset

Useful for:

- User dashboards
- Portals
- Management systems

---

# Recommended Learning Order

## Step 1

Learn Python fundamentals:

- Functions
- Classes
- Dictionaries
- File handling

## Step 2

Learn Django basics:

- Project creation
- App creation
- Views
- URLs

## Step 3

Learn backend features:

- Models
- Migrations
- ORM
- Templates

## Step 4

Build CRUD applications

---

# Typical Folder Layout

```text
project/
├── manage.py
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── static/
```

---

# Useful Packages

Additional packages often used with Django:

```bash
pip install django
pip install pillow
pip install django-crispy-forms
pip install django-filter
```

---

# Common Mistakes

## App not registered

Add app in `settings.py`:

```python
INSTALLED_APPS = [
	'students',
]
```

## Migrations not applied

```bash
python manage.py makemigrations
python manage.py migrate
```

## Incorrect URL configuration

Check:

- project `urls.py`
- app `urls.py`

## Static files not loading

Usually caused by:

- Incorrect file path
- Missing static settings
- Missing template configuration

---

# Quick Command Reference

```bash
python manage.py runserver
python manage.py startapp appname
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

# Final Notes

Django is useful for building:

- Web applications
- CRUD systems
- Admin dashboards
- APIs
- School projects
- Backend services

