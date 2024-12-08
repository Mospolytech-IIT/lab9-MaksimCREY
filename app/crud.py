"""CRUD operations module"""
from sqlalchemy.orm import Session
from .models import User, Post
from .schemas import UserCreate, PostCreate

# Функция для добавления пользователя
def create_user(db: Session, user: UserCreate):
    """
    Создает нового пользователя в базе данных.
    """
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Функция для добавления поста
def create_post(db: Session, post: PostCreate, user_id: int):
    """
    Создает новый пост в базе данных.
    """
    db_post = Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Получение всех пользователей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список всех пользователей из базы данных.
    """
    return db.query(User).offset(skip).limit(limit).all()

# Получение всех постов
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список всех постов из базы данных.
    """
    return db.query(Post).offset(skip).limit(limit).all()

# Получение постов конкретного пользователя
def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Получает список постов для конкретного пользователя.
    """
    return db.query(Post).filter(Post.user_id == user_id).offset(skip).limit(limit).all()

# Обновление email пользователя
def update_user_email(db: Session, user_id: int, new_email: str):
    """
    Обновляет электронную почту пользователя.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user

# Обновление контента поста
def update_post_content(db: Session, post_id: int, new_content: str):
    """
    Обновляет содержимое поста.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()
        db.refresh(post)
    return post

# Удаление поста
def delete_post(db: Session, post_id: int):
    """
    Удаляет пост по его ID.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()

# Удаление пользователя и его постов
def delete_user_and_posts(db: Session, user_id: int):
    """
    Удаляет пользователя и все его посты.

    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.query(Post).filter(Post.user_id == user.id).delete()
        db.delete(user)
        db.commit()
