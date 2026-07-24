import os

PRODUCT_NAME = os.getenv("PRODUCT_NAME", "PlateBridge LK")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./platebridge.db")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "demo123")
MAX_COOKED_HOURS = int(os.getenv("MAX_COOKED_HOURS", "4"))
DEFAULT_RADIUS_KM = int(os.getenv("DEFAULT_RADIUS_KM", "25"))

