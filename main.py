import uvicorn
from fastapi import FastAPI, Depends
from app.api.routers.admin import admin_router
from app.api.routers.auth import auth_router
from app.api.routers.author import author_router
from app.api.routers.book import book_router
from app.api.routers.genre import genre_router
from app.api.routers.user import user_router
from app.log.logger import logger


app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(author_router)
app.include_router(book_router)
app.include_router(genre_router)
app.include_router(user_router)


if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(app="main:app")
