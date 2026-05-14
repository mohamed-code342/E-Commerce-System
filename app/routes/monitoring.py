from fastapi import APIRouter, Depends

from app.auth import admin_only
from app.monitoring import monitoring_data


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)


# =========================
# Get Monitoring Dashboard Data (Admin Only)
# =========================

@router.get("/dashboard")
def get_monitoring_dashboard(
    current_user=Depends(admin_only)
):

    total_requests = monitoring_data["total_requests"]
    total_response_time = monitoring_data["total_response_time"]
    error_count = monitoring_data["error_count"]

    average_response_time = 0

    if total_requests > 0:
        average_response_time = total_response_time / total_requests

    error_rate = 0

    if total_requests > 0:
        error_rate = (error_count / total_requests) * 100

    return {
        "total_requests": total_requests,
        "average_response_time": round(average_response_time, 4),
        "error_count": error_count,
        "error_rate": round(error_rate, 2),
        "recent_errors": monitoring_data["recent_errors"],
        "system_health": monitoring_data["system_health"]
    }