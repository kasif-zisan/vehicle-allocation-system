from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Specify the database
db = client['vehicle_allocation_db']

# Define collections
employees_collection = db['employees']
vehicles_collection = db['vehicles']
allocations_collection = db['allocations']

# Function to seed initial data
def seed_data():
    # Seed 1000 employees
    employees = [{"name": f"employee{i+1}", "employee_id": i+1} for i in range(1000)]
    employees_collection.insert_many(employees)
    
    # Seed 1000 vehicles
    vehicles = [{"vehicle_id": i+1, "driver": f"driver{i+1}"} for i in range(1000)]
    vehicles_collection.insert_many(vehicles)

# Run the seed_data function
if __name__ == "__main__":
    seed_data()