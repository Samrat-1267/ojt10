# Python + Django Notes

> Learning backend development with Python and Django.  
> Because apparently making the browser talk to your code is considered progress.

---

# What is Django?

Django is a **high-level Python web framework** used to build web applications quickly. It follows the **MVT (Model-View-Template)** architecture and includes many built-in features like authentication, admin panel, ORM, and routing.

It is designed for developers who want to build things fast without manually wiring every component like some ritual sacrifice to web dev gods.

---

# Why Django?

## Advantages

- Fast development
- Clean structure
- Secure by default
- Built-in admin panel
- Scalable
- Uses Python (which means readable syntax and fewer headaches)

---

# Python Basics Needed Before Django

Django is just Python with extra bureaucracy.

Before starting Django, understand:

## Must Know

- Variables
- Data types
- Functions
- Loops
- Conditions
- Lists / Tuples / Dictionaries
- Classes & Objects
- OOP basics
- File handling
- Modules
- Virtual environments
- pip package manager
- Exception handling

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

## Check Version

```bash
python -m django --version
```

---

# Create Django Project

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
| manage.py | Main command file |
| settings.py | Project settings |
| urls.py | URL routing |
| asgi.py | Async deployment |
| wsgi.py | Standard deployment |

---

# Project vs App

This naming confuses beginners because naming things is one of humanity’s oldest failures.

## Project

Entire website/application.

## App

A module inside project handling one feature.

Example:

- Project = school website
- App = students
- App = attendance
- App = teachers

Create app:

```bash
python manage.py startapp students
```

---

# Common Commands

## Run Server

```bash
python manage.py runserver
```

Server:

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

## Create Admin User

```bash
python manage.py createsuperuser
```

---

# MVT Architecture

Django uses **MVT**:

## Model

Handles database structure.

## View

Handles logic.

## Template

Handles frontend HTML.

Flow:

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

- Each class = table
- Each field = column
- Django ORM manages SQL automatically

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

Maps URL paths to views.

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

Templates are HTML files with Django variables.

Example:

```html
<h1>{{ title }}</h1>
```

---

# Template Syntax

## Variable

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

ORM = Object Relational Mapping

Allows database operations using Python.

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

Django provides a built-in admin dashboard.

Register model:

```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

Visit:

```text
/admin
```

This thing is absurdly useful considering how little effort it takes.

---

# Database

Default database:

```text
SQLite
```

Good for:

- Learning
- Testing
- Small projects

Production commonly uses:

- PostgreSQL

---

# Static Files

Used for:

- CSS
- JavaScript
- Images

Folder:

```text
static/
```

---

# Media Files

Used for uploaded files.

Examples:

- profile images
- documents
- PDFs

Folder:

```text
media/
```

---

# Forms

Django forms help validate user input.

Example:

```python
from django import forms

class StudentForm(forms.Form):
	name = forms.CharField()
```

---

# Authentication

Django has built-in:

- login
- logout
- signup
- password reset

Useful for:

- dashboards
- portals
- user systems

---

# Recommended Learning Order

## Step 1

Learn Python basics:

- functions
- classes
- dictionaries
- file handling

## Step 2

Learn Django basics:

- project
- app
- views
- urls

## Step 3

Learn backend features:

- models
- migrations
- ORM
- templates

## Step 4

Build small CRUD apps

That’s where things stop being tutorial cosplay and start becoming actual skill.

---

# Useful Folder Layout

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

Extra tools:

```bash
pip install django
pip install pillow
pip install django-crispy-forms
pip install django-filter
```

---

# Common Mistakes

## Forgetting to register app

In `settings.py`:

```python
INSTALLED_APPS = [
	'students',
]
```

## Forgetting migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Wrong URL include

Always check:

- project `urls.py`
- app `urls.py`

## Static files not loading

Usually incorrect path or missing settings. Django enjoys letting you discover this at the least convenient time.

---

# Quick Cheatsheet

```bash
python manage.py runserver
python manage.py startapp appname
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

# Final Notes

Django is excellent for:

- backend learning
- school projects
- CRUD systems
- dashboards
- admin tools
- APIs
- hackathons
