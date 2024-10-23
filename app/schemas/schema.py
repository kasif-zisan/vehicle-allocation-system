def individual_employee(employee) -> dict:
    return{
        "id" : str(employee["_id"]),
        "name" : employee["name"],
        "employee_id" : employee["employee_id"]
    }
def employee_list(employees) -> list:
    return [individual_employee(employee) for employee in employees]

def individual_vehicle(vehicle) -> dict:
    return{
        "id" : str(vehicle["_id"]),
        "vehicle_id" : vehicle["vehicle_id"],
        "driver" : vehicle["driver"],
    }
def vehicle_list(vehicles) -> list:
    return [individual_vehicle(vehicle) for vehicle in vehicles]

def individual_allocation(allocation) -> dict:
    return{
        "id" : str(allocation["_id"]),
        "employee_id" : allocation["employee_id"],
        "vehicle_id" : allocation["vehicle_id"],
        "date" : allocation["date"]
    }
def allocation_list(allocations) -> list:
    return [individual_allocation(allocation) for allocation in allocations]
