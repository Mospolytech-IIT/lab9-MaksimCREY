"""Модели для базы данных"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Модель для таблицы пользователей (Users)
class User(Base):
    """
    Модель для представления пользователя в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        username (str): Имя пользователя (уникальное).
        email (str): Электронная почта пользователя (уникальная).
        password (str): Пароль пользователя.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user')


# Модель для таблицы постов (Posts)
class Post(Base):
    """
    Модель для представления поста в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор поста.
        title (str): Заголовок поста.
        content (str): Содержание поста.
        user_id (int): Внешний ключ, ссылающийся на пользователя.
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')
