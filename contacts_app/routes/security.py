from passlib.context import CryptContext

# Налаштування алгоритму хешування
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хешує пароль для збереження в базі даних."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє, чи збігається хешований пароль із введеним паролем."""
    return pwd_context.verify(plain_password, hashed_password)
