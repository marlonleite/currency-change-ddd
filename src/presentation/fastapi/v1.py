from fastapi.routing import APIRouter

from .resources.currency import currency_router
from .resources.healthy import health_router

router = APIRouter(prefix="/api/v1")


router.include_router(health_router)
router.include_router(currency_router)
