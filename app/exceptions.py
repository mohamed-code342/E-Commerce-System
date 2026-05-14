from fastapi import HTTPException


# =========================
# Reusable Error Responses
# =========================

def not_found_error(message: str):
    raise HTTPException(
        status_code=404,
        detail=message
    )


def bad_request_error(message: str):
    raise HTTPException(
        status_code=400,
        detail=message
    )


def unauthorized_error(message: str):
    raise HTTPException(
        status_code=401,
        detail=message
    )


def forbidden_error(message: str):
    raise HTTPException(
        status_code=403,
        detail=message
    )