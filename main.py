## DB
from sqlmodel import SQLModel
from schema import engine, init_user
from webapi import user

## FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse,PlainTextResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up!") # Startup logic
    SQLModel.metadata.create_all(engine)
    init_user()
    yield
    print("Application is shutting down!") # Shutdown logic
    SQLModel.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)
# app = FastAPI(title="Authentication Demo", version="1.0.0")

# app config
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "path": request.url.path
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": request.url.path
        }
    )

# Web PAGE
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Authentication Demo"}

@app.get("/err404")
async def err404():
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/err500")
async def err500():
    raise Exception('123123')

@app.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots_txt():
    return """
    User-agent: *
    Allow: /
    """

# Web API
app.include_router(user.router, tags=["Users"], prefix="/api/user")


# main.sh
import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)