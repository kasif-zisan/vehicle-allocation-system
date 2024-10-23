# Vehicle Allocation System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Running Procedure](#running-procedure)
- [Deployment](#deployment)

## Overview
The Vehicle Allocation System is a FastAPI-based application integrated with MongoDB that allows employees of a company to allocate a vehicle for a day. Each vehicle is pre-assigned to a driver and can only be allocated to one employee per day. The app ensures that vehicles are not double-booked for the same day. It also provides CRUD operations for creating, updating, and deleting allocations, with limitations that prevent changes after the allocation date. Additionally, users can generate a history report of all allocations using various filters.

## Features
- **Employee Vehicle Allocation:** Employees can allocate a vehicle for a day, provided the vehicle has not already been allocated.
- **CRUD Operations:** Create, update, and delete vehicle allocations, with restrictions on editing allocations after the allocation date.
- **Pre-Assigned Drivers:** Each vehicle is pre-assigned to a driver.
- **Data Seeding:** The app seeds the database with 1000 employees, 1000 vehicles, and 1000 drivers.
- **History Reports:** Generate filtered history reports for all vehicle allocations.

## Tech Stack
-  **Backend Framework**: FastAPI
- **Database**: MongoDB (hosted on MongoDB Atlas)
- **Python Libraries**: 
  - `fastapi`
  - `uvicorn`
  - `pymongo[srv]`
  - `python-dotenv`

 ## Running Procedure

1. **Clone the Repository**  
   First, clone the project repository from GitHub:
   ```bash
   git clone https://github.com/kasif-zisan/vehicle-allocation-system.git
2. **Create and Activate Virtual Environment**
   Create a virtual environment to install the required packages:
   ```bash
   python -m venv env
   ```
   Then activate the virtual environment:
   ```bash
   env\Scripts\activate
   ```
3. **Install Required Packages**
   Install the necessary Python libraries:
   ```bash
   pip install fastapi uvicorn python-dotenv
   ```
   Install pymongo[srv] according to your python version, for example if you have python version 3.11 or later, you can install like this -
   ```bash
   python -m pip install "pymongo[srv]"==3.11
   ```
4. **MongoDB Atlas Setup**
   The database is hosted on MongoDB Atlas. Ensure you have a MongoDB Atlas cluster.
5. **Create `.env` File**
   To securely store your MongoDB database access credentials, in you `app` folder, create a `.env` file and paste the following line into it:
   ```python
   MONGO_URI=mongodb+srv://<username>:<password>@<clustername>.wjjv1.mongodb.net/vehicle_allocation_db?retryWrites=true&w=majority
   ```
   Replace:
   - `<username>` with your MongoDB database access username.
   - `<password>` with the corresponding password.
   - `<clustername>` with your MongoDB cluster name (e.g., `cluster0`).
6. Seed the Database
   Run the `seed_data.py` script to populate the database with employees, vehicles, and drivers:
   ```bash
   python seed_data.py
   ```
7. **Run the Application**
   Start the FastAPI server by running the following command:
   ```bash
   uvicorn app.main:app --reload
   ```
You can access the interactive Swagger documentation at: http://127.0.0.1:8000/docs#/

## Deployment
I aim to containerize this application using Docker, which allows the app to run consistently across different environments.
