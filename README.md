# Expense Tracker API

Expense Tracker API is a backend RESTful service built using Flask and MySQL.
It allows users to securely manage their expenses with authentication,
CRUD operations, category-based summaries, and report generation.

---

## Features
- User Signup & Login (JWT Authentication)
- Access, Refresh & ID Tokens
- Secure Logout using Token Revocation
- User Profile Management
- Expense CRUD Operations
- Category-wise Expense Summary
- PDF & Excel Report Generation
- Clean MVC Architecture

---

## 🛠 Tech Stack
- Python (Flask)
- MySQL
- SQLAlchemy
- Flask-JWT-Extended
- bcrypt
- Pandas / openpyxl
- ReportLab

---

## Project Structure

app/
├── controllers/
├── models/
├── routes/
├── services/
├── utils/
├── extensions/


---

## Authentication Flow
1. User logs in and receives JWT access token
2. Token must be sent in request header:


Authorization: Bearer <access_token>

3. Backend extracts user identity from token

---

## API Endpoints

### Auth
- POST `/auth/signup`
- POST `/auth/login`
- POST `/auth/refresh`
- POST `/auth/logout`

### User
- GET `/user/profile`
- PUT `/user/profile`
- DELETE `/user/profile`

### Expenses
- POST `/api/expenses`
- GET `/api/expenses`
- PUT `/api/expenses/{id}`
- DELETE `/api/expenses/{id}`
- GET `/api/expenses/summary`
- GET `/api/expenses/export/pdf`

### FORGOT PASSWORD
- POST `/auth/forgot-password`
- POST `/auth/verify-otp`
- POST `/auth/reset-password`




---

## Run the Project

### 1. Create a Virtual Environment

**Windows (CMD / PowerShell)**

    ```bash
    python -m venv .venv
    ```

### 2.Activate the Virtual Environment

**Windows (PowerShell)**

    ```bash
    .venv\Scripts\Activate
    ```

### 3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```