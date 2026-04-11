from fastapi import FastAPI

from routers.auth import auth_router
from routers.auth_user import auth_user_router
from routers.user import user_router

# Main application
app = FastAPI()


@app.get("/", include_in_schema=False)
async def health_check():
    return {"status": "ok"}


# Include router
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(auth_user_router)
