from fastapi import FastAPI

from routers.auth import auth_router
from routers.user import user_router

# Main application
app = FastAPI()

# Include router
app.include_router(user_router)
app.include_router(auth_router)
