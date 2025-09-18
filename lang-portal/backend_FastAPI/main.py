from fastapi import FastAPI
from database import Base, engine
from routers import (
    words,
    groups,
    study_sessions,
    study_activities,
    dashboard,
)

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Language Portal API",
    version="1.0.0"
)

# Include routers
app.include_router(words.router, prefix="/api", tags=["Words"])
app.include_router(groups.router, prefix="/api", tags=["Groups"])
app.include_router(study_sessions.router, prefix="/api", tags=["Study Sessions"])
app.include_router(study_activities.router, prefix="/api", tags=["Study Activities"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
