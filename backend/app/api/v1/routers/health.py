from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """Usado por Azure App Service / Docker healthcheck."""
    return {"status": "ok"}
