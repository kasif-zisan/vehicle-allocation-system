from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client['vehicle_allocation_db']

employees_collection = db['employees']
vehicles_collection = db['vehicles']
allocations_collection = db['allocations']

def get_employees_collection():
    return employees_collection

def get_vehicles_collection():
    return vehicles_collection

def get_allocations_collection():
    return allocations_collection