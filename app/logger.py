import logging


# =========================
# Logging Configuration
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ecommerce_api")


# =========================
# Logging Levels Examples
# =========================

# DEBUG -> Detailed debugging information
# Example:
#logger.debug(f"Current user ID: {current_user.id}")

# INFO -> Successful operations
# Example:
#logger.info(f"User logged in successfully: {db_user.email}")

# WARNING -> Suspicious or failed attempts
# Example:
#logger.warning(f"Failed login attempt: {user.email}")

# ERROR -> Application errors
# Example:
#logger.error("Cart is empty during checkout")

# CRITICAL -> Critical system failures
# Example:
#logger.critical("Database connection failed")