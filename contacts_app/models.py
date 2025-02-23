from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from contacts_app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Додано поле для збереження хешованого пароля

    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))  # Додано поле owner_id
    owner = relationship("User", back_populates="contacts")  # Відносини між Contact і User
