# Django Blog

![Django Blog Banner](file:///C:/Users/Admin/.gemini/antigravity/brain/ecfa2ca1-1cad-459b-a456-ed7eb5091693/django_blog_banner_1777910346806.png)

A professional, responsive, and feature-rich blogging platform built with **Django 6.0**. This project offers a complete CMS (Content Management System) experience for bloggers, editors, and administrators.

---

## 🚀 Core Features

### 📝 Dynamic Blogging System
- **Advanced Post Management**: Create, edit, and delete blog posts with ease.
- **Draft & Publish Workflow**: Save your progress as a draft and publish when ready.
- **Featured Posts**: Highlight your best content on the home page with a dedicated "Featured" flag.
- **Categorization**: Organize content into various categories (Sports, Politics, Tech, etc.).
- **Smart Slugs**: Automatic SEO-friendly URL generation with duplicate handling.
- **Rich Media**: Integrated image upload support for featured images using **Pillow**.

### 🛠️ Powerful Admin Dashboard
- **Comprehensive Analytics**: Overview of total blogs and categories at a glance.
- **CRUD Operations**: Full Control over Posts, Categories, and Users from a sleek interface.
- **User Management**: Specialized dashboard for managing platform users.

### 🔐 Advanced Authorization & Roles
The system supports multiple levels of access to ensure secure content management:
- **Superuser (Admin)**: Full access to all settings, users, and content.
- **Staff (Editors/Managers)**: Access to the dashboard to manage posts and categories.
- **Author Control**: Authors can only edit and delete their own posts, preventing unauthorized changes.

### 🔍 Interactive User Experience
- **Live Search**: Robust search functionality to find blogs by title or content.
- **Commenting System**: Engages readers with a built-in commenting feature.
- **Social Integration**: Easily manage social links and "About" content via the `assignments` app.
- **Fully Responsive**: Optimized for all devices using **Bootstrap 4** and **Crispy Forms**.

---


## 🛠️ Tech Stack

- **Backend**: Django 6.0 (Python Framework)
- **Frontend**: HTML5, CSS3, Bootstrap 4
- **Forms**: Django Crispy Forms (Bootstrap 4 pack)
- **Database**: SQLite (Default), PostgreSQL ready
- **Image Handling**: Pillow
- **Server**: Gunicorn (WSGI HTTP Server)
- **Static Files**: WhiteNoise

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd django-blog
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the site at `http://127.0.0.1:8000/`.

---

## 📁 Project Structure

- `blog_main/`: Project configuration and root URLs.
- `blogs/`: Main blog app (Models, Views, Templates for content).
- `dashboard/`: Custom administration interface logic.
- `assignments/`: Utility app for managing "About" and "Social Links".
- `media/`: User-uploaded images and content.
- `templates/`: Shared HTML templates and layouts.

---

## 👤 Credits

Built with ❤️ by **Drishti Rajput**

---

> [!NOTE]
> This README was beautified and documented with the help of Antigravity AI.
