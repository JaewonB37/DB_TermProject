# DB_TermProject
# Real Estate Management System

## Introduction
The Real Estate Management System is a comprehensive Python-based application designed for managing real estate properties, agents, clients, transactions, and appointments. It offers an intuitive, user-friendly interface and robust backend integration for efficient management.

## Installation and Execution

### Prerequisites
- CentOS environment with internet access.
- Python installed on your system.
- MySQL installed on your CentOS environment.

### Steps

1. **Clone the Project from GitHub:**
   ```bash
   git clone https://github.com/JaewonB37/DB_TermProject.git

2. **Install and Configure MySQL:**
   ```bash
   sudo yum install mysql-server
   sudo systemctl start mysqld
   sudo mysql_secure_installation

3. **Set Up Python Environment:**
   ```bash
   pip install pymysql sshtunnel
   
4. **Run the Program:**
   ```bash
   python realestate.py

Features
Data Management: View, add, update, and delete details of properties, agents, clients, transactions, and appointments.
Secure Access: Uses SSH tunneling for secure database access.
Menu-Driven Interface: Easy-to-navigate, interactive menus for operations.
Technology Stack
Python: For application development.
MySQL: Backend database.
SSH Tunneling: Secure access method.
CentOS: Linux distribution hosting the backend.
