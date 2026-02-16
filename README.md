# AUTH-API – Role-Based Task Management System

## Overview

AUTH-API is a FastAPI-based authentication and task management API that implements role-based access control (RBAC).  
The system supports three roles — **user**, **manager**, and **admin** — each with clearly defined permissions for managing tasks.

This project demonstrates secure authentication, authorization, and controlled access to resources using modern backend practices.


## Features

- User signup and login
- JWT-based authentication
- Role-based access control (RBAC)
- Roles: user, manager, admin
- Admin auto-creation on application startup
- Task creation, update, and deletion with role rules
- User-to-manager assignment
- SQLite database with SQLAlchemy ORM


## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- OAuth2 + JWT
- Uvicorn


## Roles and Permissions

### User
- Can sign up and log in
- Can create tasks
- Can view, update, and delete their own tasks

### Manager
- Cannot create tasks
- Can update and delete tasks assigned to them
- Can only manage tasks linked to them

### Admin
- Automatically created on app startup
- Can update and delete any task
- Can assign managers to users


## Database Models

### User
- `id`
- `email`
- `username`
- `hashed_password`
- `role`
- `manager_id` (self-referencing foreign key)

### Task
- `id`
- `title`
- `description`
- `completed`
- `user_id`
- `manager_id`
- `created_at`


## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd AUTH-API

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

Activate it:

window
``  bash
venv\Scripts\activate

macOS / Linux
```bash
source venv/bin/activate

### 3. Install Dependencies

```bash
pip install -r requirements.txt

### 4. Running the Application

Start the development server:

uvicorn main:app --relo

### 5. Application Access

Base URL

http://127.0.0.1:8000


Swagger API Documentation

http://127.0.0.1:8000/docs



