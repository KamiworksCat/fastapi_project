from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_administrator = Column(Boolean, default=True)
    disabled = Column(Boolean, default=False)
    quota = Column(Integer, default=0)

    items = relationship("Item", back_populates="owner")
