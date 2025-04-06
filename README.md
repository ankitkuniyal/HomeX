# Household Services Management System

A Flask-based web application for managing household service requests, connecting customers with service professionals.

## Features

- User roles: Customers, Service Professionals, Admin
- Service request lifecycle management
- Professional approval system
- Service history tracking
- Admin dashboard for management

## Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

## Setup Instructions

### 1. Clone the repository
```bash
git clone [your-repository-url]
cd household-services-app
```

2. Set up virtual environment

```bash
python -m venv venv
```
On Windows:

```bash
venv\Scripts\activate
```
On macOS/Linux:

```bash
source venv/bin/activate
```
3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Initialize the database

```bash
python app.py
```
(This will create the SQLite database file household_services.db)

5. (Optional) Populate sample data

```bash
python populate_sample_data.py
```

Running the Application

```bash
python app.py
```
The application will run at http://localhost:5500

Default Accounts

Admin

Email: admin@admin.com
Password: admin123
Sample Customers (if populated)

Email: john@example.com
Password: password123
Sample Professionals (if populated)

Email: mike@example.com (Plumber)
Password: password123
