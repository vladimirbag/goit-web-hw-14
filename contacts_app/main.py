from fastapi import FastAPI
from contacts_app.routes.contacts import contacts_router
from contacts_app.auth import auth_router

app = FastAPI()

# Підключення маршрутів
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API"}
