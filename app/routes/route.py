from fastapi import APIRouter, HTTPException, Query
from config.db import get_employees_collection, get_vehicles_collection, get_allocations_collection
from models.allocation import Allocation
from schemas.schema import employee_list, vehicle_list, allocation_list
from bson import ObjectId
from datetime import datetime
from typing import Optional

# Initialize the router for allocation-related endpoints
router = APIRouter()

# -------------------- EMPLOYEE ROUTES --------------------
@router.get("/employees", summary="Retrieve all employees", description="Fetches a list of all employees.", tags=["Employees"])
async def get_all_employees():
    """
    This endpoint retrieves all employees from the database.
    """
    employees_collection = get_employees_collection()
    employees = employees_collection.find()  
    return employee_list(employees)  

# -------------------- VEHICLE ROUTES --------------------
@router.get("/vehicles", summary="Retrieve all vehicles", description="Fetches a list of all vehicles.", tags=["Vehicles"])
async def get_all_vehicles():
    """
    This endpoint retrieves all vehicles from the database.
    """
    vehicles_collection = get_vehicles_collection()
    vehicles = vehicles_collection.find()  
    return vehicle_list(vehicles)  

# -------------------- ALLOCATION ROUTES --------------------
@router.get(
    "/allocations",
    summary="Retrieve all allocations",
    description="Fetch all vehicle allocations. You can filter by employee ID, vehicle ID, or allocation date.",
    tags=["Allocations"],
    response_model=list,
    responses={
        200: {"description": "List of allocations fetched successfully"},
        404: {"description": "No allocations found based on the criteria"}
    }
)
async def get_all_allocations(
    employee_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    date: Optional[str] = Query(None)
):
    """
    Retrieve all allocations, with optional filters such as employee_id, vehicle_id, or date.
    """
    allocations_collection = get_allocations_collection()

    query_filter = {}

     # Filter by employee_id if provided
    if employee_id is not None:
        employee_exists = allocations_collection.find_one({"employee_id": employee_id})
        if not employee_exists:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found.")
        query_filter["employee_id"] = employee_id

    # Filter by vehicle_id if provided
    if vehicle_id is not None:
        vehicle_exists = allocations_collection.find_one({"vehicle_id": vehicle_id})
        if not vehicle_exists:
            raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} not found.")
        query_filter["vehicle_id"] = vehicle_id

    # Filter by date if provided and also enforce date format
    if date is not None:
        try:
            Allocation.validate_date_format_path(date)
            date_exists = allocations_collection.find_one({"date": date})
            if not date_exists:
                raise HTTPException(status_code=404, detail=f"No allocations found for the date {date}.")
            else:
                query_filter["date"] = date
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Retrieve allocations based on filters
    allocations = allocations_collection.find(query_filter)

    # Check if any allocations were found, if not, return 404
    if not allocations:
        raise HTTPException(status_code=404, detail="No allocations found matching the given criteria.")

    return allocation_list(allocations)  # Return the filtered allocation list

# Route to create a new allocation
@router.post(
    "/allocations",
    summary="Create a new allocation",
    description="Create a new vehicle allocation for an employee. Ensure that the employee and vehicle exist, and that neither is double-booked.",
    tags=["Allocations"],
    response_model=Allocation,
    responses={
        201: {"description": "Allocation created successfully"},
        400: {"description": "Bad request or conflicts with existing allocations"},
        404: {"description": "Employee or vehicle not found"}
    }
)
async def create_allocation(allocation: Allocation):
    """
    Create a new allocation. Ensure the employee and vehicle exist and are not already booked for the same date.
    """

    # Get the collections
    employees_collection = get_employees_collection()
    vehicles_collection = get_vehicles_collection()
    allocations_collection = get_allocations_collection()

    # Step 1: Check if employee exists
    employee = employees_collection.find_one({"employee_id": allocation.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Step 2: Check if vehicle exists
    vehicle = vehicles_collection.find_one({"vehicle_id": allocation.vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # new feature
    # Step 3: Check if the employee has already booked another vehicle for the same date
    existing_allocation = allocations_collection.find_one({
        "employee_id": allocation.employee_id,
        "date": allocation.date
    })
    
    if existing_allocation:
        raise HTTPException(
            status_code=400,
            detail=f"Employee {allocation.employee_id} has already booked another vehicle for {allocation.date}."
        )

    # Step 4: Check if the vehicle is already allocated for that date
    existing_allocation = allocations_collection.find_one({"vehicle_id": allocation.vehicle_id, "date": allocation.date})
    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle is already allocated for this date")

    # Step 5: Create the allocation
    new_allocation = {
        "employee_id": allocation.employee_id,
        "vehicle_id": allocation.vehicle_id,
        "date": allocation.date
    }

    # Insert into the database
    result = allocations_collection.insert_one(new_allocation)

    # Return the created allocation
    return {
        "id": str(result.inserted_id),
        "employee_id": allocation.employee_id,
        "vehicle_id": allocation.vehicle_id,
        "date": allocation.date
    }

# Route to update existing allocation
@router.put(
    "/allocations/{allocation_id}",
    summary="Update an existing allocation",
    description="Update an existing vehicle allocation. Only the original employee who created the allocation can update it.",
    tags=["Allocations"],
    response_model=Allocation,
    responses={
        200: {"description": "Allocation updated successfully"},
        400: {"description": "Bad request or no changes detected"},
        403: {"description": "Not authorized to update the allocation"},
        404: {"description": "Allocation or vehicle not found"}
    }
)
async def update_allocation(allocation_id: str, allocation: Allocation):
    """
    Update an existing allocation. Only the original employee who made the allocation can update it.
    """

    # Get the collections
    employees_collection = get_employees_collection()
    vehicles_collection = get_vehicles_collection()
    allocations_collection = get_allocations_collection()

    # Step 1: Check if the allocation exists
    existing_allocation = allocations_collection.find_one({"_id": ObjectId(allocation_id)})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    # Step 2: Check if employee exists
    employee = employees_collection.find_one({"employee_id": allocation.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Step 3: Ensure that the same employee who made the allocation is the one updating it
    if allocation.employee_id != existing_allocation["employee_id"]:
        raise HTTPException(status_code=403, detail="You are not authorized to update this allocation. Only the original employee can update their allocation.")

    # Step 4: Check if vehicle exists
    vehicle = vehicles_collection.find_one({"vehicle_id": allocation.vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Step 5: Check if the employee has already booked another vehicle for the same date
    if allocation.employee_id != existing_allocation["employee_id"] or allocation.date != existing_allocation["date"]:
        existing_employee_allocation = allocations_collection.find_one({
            "employee_id": allocation.employee_id,
            "date": allocation.date
        })
        if existing_employee_allocation:
            raise HTTPException(
                status_code=400,
                detail=f"Employee {allocation.employee_id} has already booked another vehicle for {allocation.date}."
            )

    # Step 6: Check if the vehicle is already allocated for that date (to another employee)
    if allocation.vehicle_id != existing_allocation["vehicle_id"] or allocation.date != existing_allocation["date"]:
        existing_vehicle_allocation = allocations_collection.find_one({
            "vehicle_id": allocation.vehicle_id,
            "date": allocation.date
        })
        if existing_vehicle_allocation:
            raise HTTPException(
                status_code=400,
                detail=f"Vehicle {allocation.vehicle_id} is already allocated for {allocation.date}."
            )

    # Step 7: Check if any changes have been made
    if (
        allocation.employee_id == existing_allocation["employee_id"] and
        allocation.vehicle_id == existing_allocation["vehicle_id"] and
        allocation.date == existing_allocation["date"]
    ):
        raise HTTPException(status_code=400, detail="No changes detected.")

    # Step 8: Update the allocation
    updated_allocation = {
        "employee_id": allocation.employee_id,
        "vehicle_id": allocation.vehicle_id,
        "date": allocation.date
    }

    result = allocations_collection.update_one(
        {"_id": ObjectId(allocation_id)},
        {"$set": updated_allocation}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update the allocation.")

    return {
        "id": allocation_id,
        "employee_id": allocation.employee_id,
        "vehicle_id": allocation.vehicle_id,
        "date": allocation.date
    }

# Route to delete existing allocation
@router.delete(
    "/allocations/{allocation_id}",
    summary="Delete an existing allocation",
    description="Delete an allocation. Only the original employee can delete it, and it cannot be deleted if the date has already passed.",
    tags=["Allocations"],
    responses={
        200: {"description": "Allocation deleted successfully"},
        400: {"description": "Bad request or invalid date"},
        403: {"description": "Not authorized to delete the allocation"},
        404: {"description": "Allocation not found"}
    }
)
async def delete_allocation(allocation_id: str, allocation: Allocation):
    """
    Delete an allocation. Only the employee who created the allocation can delete it, and the date cannot be in the past.
    """
    allocations_collection = get_allocations_collection()

    # Step 1: Check if allocation exists
    existing_allocation = allocations_collection.find_one({"_id": ObjectId(allocation_id)})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    # Step 2: Ensure only the employee who created the allocation can delete it
    if existing_allocation["employee_id"] != allocation.employee_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this allocation.")

    # Step 3: Check if the allocation date is in the past
    today = datetime.now().date()
    allocation_date = datetime.strptime(existing_allocation["date"], "%Y-%m-%d").date()
    if allocation_date < today:
        raise HTTPException(status_code=400, detail="You cannot delete allocations that are in the past.")
    elif allocation_date == today:
        raise HTTPException(status_code=400, detail="You must delete the allocation before the allocation date.")

    # Step 4: Proceed to delete the allocation
    result = allocations_collection.delete_one({"_id": ObjectId(allocation_id)})

    # Step 5: Return success message
    if result.deleted_count == 1:
        return {"message": "Allocation successfully deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete allocation")