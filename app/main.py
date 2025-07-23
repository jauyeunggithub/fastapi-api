from fastapi import FastAPI
from app.routes import users, items, email
from app import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(email.router)
