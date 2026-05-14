from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import users, products, categories, cart, orders

from fastapi import Request
import time

from app.logger import logger

from app.monitoring import add_request, add_error
from app.routes import monitoring, performance

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)

app.include_router(products.router)

app.include_router(categories.router)

app.include_router(cart.router)

app.include_router(orders.router)

app.include_router(monitoring.router)

app.include_router(performance.router)



@app.get("/")
def home():
    return {"message": "E-Commerce API Running"}

# =========================
# Request Logging & Monitoring Middleware
# =========================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    try:
        response = await call_next(request)

    except Exception as e:

        process_time = time.time() - start_time

        # ERROR -> Unhandled application exception
        logger.error(f"Unhandled error on {request.url.path}: {str(e)}")

        add_error(str(e))
        add_request(process_time, 500)

        raise e

    process_time = time.time() - start_time

    add_request(process_time, response.status_code)

    if response.status_code >= 400:
        add_error(
            f"{request.method} {request.url.path} returned {response.status_code}"
        )

    logger.info(
        f"{request.method} | "
        f"{request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    return response