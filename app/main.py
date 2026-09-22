from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from app.api.routes.main import api_router

@asynccontextmanager
async def lifespan(application: FastAPI):
  application.state.async_client = httpx.AsyncClient()
  application.state.sync_client = httpx.Client()

  yield

  await application.state.async_client.aclose()
  application.state.sync_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
