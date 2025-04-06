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
Project Structure

Copy
household-services-app/
├── app.py                 # Main application file
├── populate_sample_data.py # Sample data generator
├── requirements.txt       # Dependencies
├── venv/                  # Virtual environment
├── static/                # Static files (CSS, JS, images)
│   └── ...
└── templates/             # HTML templates
    └── ...
API Endpoints

/ - Login page
/login - Authentication handler
/customer_register - Customer registration
/professional_register - Professional registration
/admin - Admin dashboard
/customer_dashboard/<int:customer_id> - Customer dashboard
/professional_dashboard/<int:professional_id> - Professional dashboard
Technologies Used

Flask (Python web framework)
SQLAlchemy (ORM)
SQLite (Database)
Jinja2 (Templating)
Bootstrap (Frontend framework - assumed from templates)
License

MIT License

Copy

### Key Features of this README:

1. **Clear Setup Instructions**: Step-by-step guide from environment setup to running the app
2. **Default Credentials**: Includes the admin credentials from your code
3. **Project Structure**: Shows expected directory layout
4. **API Documentation**: Lists main endpoints
5. **Optional Sample Data**: Mentions the populate script
6. **Technology Stack**: Lists the main technologies used

To use this:
1. Save as `README.md` in your project root
2. Update the `[your-repository-url]` placeholder if applicable
3. Add any additional sections specific to your deployment needs

Would you like me to add any additional sections such as:
- Deployment instructions (e.g., for Heroku or AWS)
- Testing instructions
- Contribution guidelines
- Screenshots of the application?
