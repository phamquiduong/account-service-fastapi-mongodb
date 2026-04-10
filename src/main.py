from fastapi import FastAPI

from routers.user import user_router

# Main application
app = FastAPI()

# Include router
app.include_router(user_router)
