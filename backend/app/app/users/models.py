from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


friendship = Table(
    'friendships', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('friend_id', Integer, ForeignKey('users.id')),
    UniqueConstraint('user_id', 'friend_id', name='unique_friendships'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, default="")
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    icon = Column(String, default="")
    is_active = Column(Boolean, default=True)
    post = relationship("Post")
    invite_code = Column(String, nullable=True, unique=True)
    friends = relationship('User',
                           secondary=friendship,
                           primaryjoin=id == friendship.c.user_id,
                           secondaryjoin=id == friendship.c.friend_id)

    def __str__(self):
        return self.email

    def update_dict(self, dict):
        is_update = False
        for name, value in dict.items():
            if name in self.__dict__ and value != getattr(self, name):
                setattr(self, name, value)
                is_update = True
        return is_update

    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)
            return True

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)
            return True
