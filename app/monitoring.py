# =========================
# Monitoring Metrics Storage
# =========================

monitoring_data = {
    "total_requests": 0,
    "total_response_time": 0,
    "error_count": 0,
    "recent_errors": [],
    "system_health": "healthy"
}


def add_request(response_time: float, status_code: int):

    monitoring_data["total_requests"] += 1
    monitoring_data["total_response_time"] += response_time

    if status_code >= 400:
        monitoring_data["error_count"] += 1


def add_error(error_message: str):

    monitoring_data["recent_errors"].append(error_message)

    if len(monitoring_data["recent_errors"]) > 10:
        monitoring_data["recent_errors"].pop(0)