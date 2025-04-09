import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, sessions, feedback, data
from .config import settings
from .database import init_db
import asyncio
import sentry_sdk
from phoenix.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

# tracer_provider = register(
#   project_name=settings.PHOENIX_PROJECT_NAME,
#   endpoint=settings.PHOENIX_TRACER_ENDPOINT
# )

# LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,    
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router)
app.include_router(chat.router)
app.include_router(sessions.router)
app.include_router(feedback.router)


base_api_url = "/"
if settings.ENVIRONMENT == "development":
    base_api_url = "/api/"
    

@app.on_event("startup")
async def startup_event():
    # await asyncio.sleep(10)
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get(base_api_url + "sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0