from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.dashboard_schema import DashboardResponse
from app.services.dashboard_service import build_dashboard_data

router = APIRouter()


@router.get("/dashboard/me", response_model=DashboardResponse)
def get_my_dashboard(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return build_dashboard_data(db=db, vendor=current_vendor)
