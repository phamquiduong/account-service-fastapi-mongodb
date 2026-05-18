from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import auth_router
from routers.auth_user import auth_user_router
from routers.user import user_router
from settings import ORIGINS

# Main application
app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "ok"}


# Include router
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(auth_user_router)
