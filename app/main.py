from fastapi import FastAPI
from routes.route import router
app = FastAPI()
app.include_router(router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Vehicle Allocation System!"}