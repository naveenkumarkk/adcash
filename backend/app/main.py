from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.endpoints import offers, influencers, countries
from app.db.database import create_db_and_tables, AsyncSessionLocal
from app.db.seed.initial_seed import seed_initial_data
from fastapi_pagination import add_pagination

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting application")
    await create_db_and_tables()
    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application")

app = FastAPI(
    title="ADCash Offers API",
    description=(
        "API for managing advertising offers and influencer promotions. "
        "Influencers can browse available offers and see payment details."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    offers.router,
    prefix=f"{settings.API_PREFIX}/offers",
    tags=["Offers"],
)

app.include_router(
    influencers.router,
    prefix=f"{settings.API_PREFIX}/influencer",
    tags=["Influencers"],
)

app.include_router(
    countries.router,
    prefix=f"{settings.API_PREFIX}/country",
    tags=["Countries"],
)