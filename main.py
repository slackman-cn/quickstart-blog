from schema import *
from webapi import user

## FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse,RedirectResponse,PlainTextResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up!") # Startup logic
    SQLModel.metadata.create_all(engine)
    user1 = User(username='admin', nickname='管理员', email='admin@example.com',
                 password_hash='$2b$12$XNBdL2iNdo4YNFB2GH/2wO4IN0VsDXTticOcrd.UgD50tReiIrTiu', user_role='ADMIN')
    user2 = User(username='demo', nickname='演示用户', email='demo@example.com',
                 password_hash='$2b$12$XNBdL2iNdo4YNFB2GH/2wO4IN0VsDXTticOcrd.UgD50tReiIrTiu')
    with Session(engine) as session:
        session.add(user1)
        session.add(user2)
        session.commit()
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

# Web PAGE
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Authentication Demo"}


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