# Flash Tans E-Commerce Application

A simple e-commerce application for selling premium products, built with Python Flask and MySQL.

## Features

- Browse products
- Add products to cart
- Place orders
- Admin panel for managing products and viewing orders
- MySQL database integration

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation Instructions

### 1. SSH into Your VM

From your host machine's terminal:

```bash
ssh user@<FLOATING_IP>
```

Replace `<FLOATING_IP>` with your instance's floating IP address.

### 2. Update System & Install Dependencies

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv mysql-server
```

### 3. Clone/Upload the Application

You can clone from a repository or upload the files. For example:

```bash
# If cloning from git
git clone <repository-url> flashtans-app
cd flashtans-app

# OR if uploading, use scp from your host machine:
# scp -r /path/to/flashtans-app user@<FLOATING_IP>:~/
```

### 4. Set Up MySQL Database

```bash
# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Login to MySQL
sudo mysql

# Create database and user
CREATE DATABASE flash_tans_db;
CREATE USER 'flashtans_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON flash_tans_db.* TO 'flashtans_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your database credentials
nano .env
```

Update the following values in `.env`:
```
PORT=8000
DB_HOST=localhost
DB_USER=flashtans_user
DB_PASSWORD=your_secure_password
DB_NAME=flash_tans_db
DB_PORT=3306
SECRET_KEY=change-this-to-a-random-secret-key
```

### 6. Create Virtual Environment & Install Python Dependencies

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 7. Run the Application

**IMPORTANT:** The application must listen on `0.0.0.0` (not `127.0.0.1`) to be accessible from outside the VM.

```bash
# Make sure you're in the flashtans-app directory and virtual environment is activated
python3 app.py
```

The application will start on `http://0.0.0.0:8000`

### 8. Access the Application

Open your web browser and navigate to:
```
http://<FLOATING_IP>:8000
```

Replace `<FLOATING_IP>` with your instance's floating IP address.

## Default Pages

- **Home/Products:** `http://<FLOATING_IP>:8000/`
- **Shopping Cart:** `http://<FLOATING_IP>:8000/cart`
- **Admin Panel:** `http://<FLOATING_IP>:8000/admin`

## Sample Products

The application comes with 3 sample products:
1. Buckets - Amazon S3 Buckets for scalable storage
2. Load Balancers - Customizable load balancers
3. Microsoft Azure - Cloud computing services

## Running in Production

For production deployment, consider:

1. Using a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

2. Setting up a reverse proxy with Nginx

3. Using a process manager like systemd or supervisor

4. Disabling Flask debug mode (set `debug=False` in `app.py`)

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL service is running: `sudo systemctl status mysql`
- Verify database credentials in `.env` file
- Check if database exists: `mysql -u flashtans_user -p -e "SHOW DATABASES;"`

### Port Already in Use
If port 8000 is already in use, change the PORT in `.env` file to another port (e.g., 8080)

### Permission Denied
Make sure you have proper permissions for the application directory and MySQL can be accessed by your user.

## Technology Stack

- **Backend:** Python 3 with Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript
- **Template Engine:** Jinja2

## Project Structure

```
flashtans-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── config/
│   └── database.py        # Database configuration
├── models/
│   ├── product.py         # Product model
│   ├── customer.py        # Customer model
│   └── order.py           # Order model
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── admin.html
│   ├── cart.html
│   └── error.html
└── public/
    └── js/
        └── app.js         # Frontend JavaScript

```

## License

This is a educational project for Cloud Infrastructure & Computing Course.
