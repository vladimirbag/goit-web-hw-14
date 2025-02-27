from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contacts_app.routes.contacts import contacts_router
from contacts_app.auth import auth_router

app = FastAPI()

# Додаємо CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволити всі домени
    allow_credentials=True,
    allow_methods=["*"],  # Дозволити всі методи HTTP
    allow_headers=["*"],  # Дозволяти всі заголовки
)

# Підключення маршрутів
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API"}
