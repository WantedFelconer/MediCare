MediCare Flask App

Overview

MediCare is a web application built using the Flask framework with a MySQL database backend. It provides a simple and intuitive interface for managing patient records, appointments, and related healthcare data. The project demonstrates CRUD (Create, Read, Update, Delete) operations using raw SQL queries integrated with Flask routes.

Features

User authentication and authorization

Patient management (add, edit, delete, view)

Appointment scheduling

Prescription tracking

Responsive frontend using HTML templates and Bootstrap

Project Structure

MediCare/
│── app.py              # Main Flask application
│── requirements.txt    # Python dependencies
│── venv/               # Virtual environment
│── templates/          # HTML templates (Jinja2)
│── static/             # CSS, JS, images
│── config.py           # Database configuration

Installation

Clone the repository:

git clone https://github.com/WantedFelconer/MediCare.git
cd MediCare

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

Configure database in config.py:

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'medicare'

Initialize the database:

CREATE DATABASE medicare;
USE medicare;
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    email VARCHAR(100)
);

Running the App

python app.py

Visit http://127.0.0.1:5000/ in your browser.

Usage

Navigate to /patients to view patient records.

Use /patients/add to add new patients.

Edit or delete patients via the interface.

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License

This project is licensed under the MIT License.
