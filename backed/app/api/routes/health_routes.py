from fastapi import APIRouter

router = APIRouter()

# Verifica que el backend está activo y respondiendo.
@router.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Backend running successfully"
    }