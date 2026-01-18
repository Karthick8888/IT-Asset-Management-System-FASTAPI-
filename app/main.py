from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


from app.api.V1.endpoints.assets import router as assets_router
from app.api.V1.endpoints.dashboard import router as dashboard_router
from app.api.V1.endpoints.employees import router as employee_router
from app.api.V1.endpoints.expiry_tracking import router as expirytracking_router
from app.api.V1.endpoints.assignments import router as assignment_router
from app.api.V1.endpoints.reports import router as reports_router

app = FastAPI()



# Allow your frontend to access the backend
origins = [
    "http://127.0.0.1:5500",  # your frontend URL
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE
    allow_headers=["*"],        # allow headers like Content-Type
)



@app.get("/")
def root():
    return {"message": "API is running.....Build by Karthick Manikandan E"}



app.include_router(
    assets_router,
    prefix="/api/v1/assets",
    tags=["Assets"]
)
app.include_router(
    dashboard_router,
    prefix="/api/dashboard",
    tags=["dashboard"]
)

app.include_router(
    employee_router,
    prefix="/api/employees",
    tags=["employees"]
)

app.include_router(
    expirytracking_router,
    prefix="/expirytracking",
    tags=["expirytracking"]
)

app.include_router(
    assignment_router,
    prefix="/api/v1/assignment",
    tags=["assignment"]
)

app.include_router(
    reports_router,
    prefix="/reports",
    tags=["reports"]
)


