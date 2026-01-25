from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.endpoints import offers,influencers,countries
from app.db.database import create_db_and_tables,AsyncSessionLocal
from app.db.seed.initial_seed import seed_initial_data
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)
    yield


app = FastAPI(
    title="Choose your offer that you are planning to promote",
    description=(
        "Offers are used to promote specific products on behalf of brands or advertisers. "
        "Influencers can browse available offers and see how they would be paid for promoting them."
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
    prefix=settings.API_PREFIX+"/offers",
    tags=["Offers"],
)

app.include_router(
    influencers.router,
    prefix=settings.API_PREFIX+"/influencer",
    tags=["influencer"],
)

app.include_router(
    countries.router,
    prefix=settings.API_PREFIX+"/country",
    tags=["country"],
)