from pydantic import BaseModel, validator
from datetime import datetime

class Allocation(BaseModel):
    employee_id: int
    vehicle_id: int
    date: str  

# Validator to enforce 'YYYY-MM-DD' format for the date field
    @validator('date')
    def validate_date_format(cls, value):
        try:
            # Attempt to parse the date in the 'YYYY-MM-DD' format
            allocation_date = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            # Raise a validation error if the format is incorrect
            raise ValueError("Invalid date format. The date must be in 'YYYY-MM-DD' format.")

        # Get today's date
        today = datetime.now().date()

        # Check if the allocation date is in the past
        if allocation_date < today:
            raise ValueError("You cannot set the allocation date for past dates.")

        # Check if the allocation date is today's date
        if allocation_date == today:
            raise ValueError("You must create the allocation before the allocation date.")

        return value

# Validator to enforce 'YYYY-MM-DD' format for the date path (filtering)
    @validator('date')
    def validate_date_format_path(cls, value):
        try:
            # Attempt to parse the date in the 'YYYY-MM-DD' format
            allocation_date = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            # Raise a validation error if the format is incorrect
            raise ValueError("Invalid date format. The date must be in 'YYYY-MM-DD' format.")
        
        return value