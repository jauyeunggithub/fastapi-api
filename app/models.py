from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="items")
    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }


User.items = relationship("Item", back_populates="owner")


class Book(Item):
    __tablename__ = 'books'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    title = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }
