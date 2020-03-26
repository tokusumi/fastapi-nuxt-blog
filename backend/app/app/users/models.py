from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, default="")
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    icon = Column(String, default="")
    is_active = Column(Boolean, default=True)
    post = relationship("Post")

    def __str__(self):
        return self.email

    def update_dict(self, dict):
        is_update = False
        for name, value in dict.items():
            if name in self.__dict__ and value != getattr(self, name):
                setattr(self, name, value)
                is_update = True
        return is_update
