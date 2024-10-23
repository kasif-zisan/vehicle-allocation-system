from pydantic import BaseModel

class Vehicle(BaseModel):
    vehicle_id: int
    driver: str