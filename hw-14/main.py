import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager

from src.config.constants import APIRoutes
from src.database.cache import get_cache
from src.database.db import get_db
from src.routes.auth import auth_router
from src.routes.contancts import contacts_router
from src.routes.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await get_cache()
    await FastAPILimiter.init(redis)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000"
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
def unexpected_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred"},
    )


app.include_router(contacts_router, prefix=APIRoutes.API_ROUTE_PREFIX)
app.include_router(auth_router, prefix=APIRoutes.API_ROUTE_PREFIX)
app.include_router(users_router, prefix=APIRoutes.API_ROUTE_PREFIX)


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        response = await db.execute(text("SELECT 1"))
        result = response.first()

        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

