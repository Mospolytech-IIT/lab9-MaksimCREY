"""Schemas for user and post data validation."""
from pydantic import BaseModel

# Модель данных для создания пользователя
class UserCreate(BaseModel):
    """
    Модель для создания нового пользователя.
    
    """
    username: str
    email: str
    password: str

# Модель данных для создания поста
class PostCreate(BaseModel):
    """
    Модель для создания нового поста.
    
    """
    title: str
    content: str

# Модель ответа для пользователя
class User(BaseModel):
    """
    Модель для представления данных пользователя в ответах API.
    """
    id: int
    username: str
    email: str

    class Config:
        """
        config
        """
        orm_mode = True

# Модель ответа для поста
class Post(BaseModel):
    """
    Модель для представления данных поста в ответах API.
  
    """
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        """
        config
        """
        orm_mode = True
