"""Main application file"""
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Локальные импорты
from . import crud, models, schemas
from .database import engine, get_db

# Создание базы данных
models.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Указываем путь для шаблонов
templates = Jinja2Templates(directory="templates")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Создает нового пользователя в базе данных.

    Args:
        user (schemas.UserCreate): Данные для создания пользователя.
        db (Session): Сессия базы данных.

    Returns:
        schemas.User: Созданный пользователь.
    """
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Получает список всех пользователей.

    Args:
        db (Session): Сессия базы данных.

    Returns:
        List[schemas.User]: Список пользователей.
    """
    users = crud.get_users(db=db)
    return templates.TemplateResponse("users_list.html", {"request": db, "users": users})

@app.get("/posts/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """
    Получает список всех постов.

    Args:
        db (Session): Сессия базы данных.

    Returns:
        List[schemas.Post]: Список постов.
    """
    posts = crud.get_posts(db=db)
    return templates.TemplateResponse("posts_list.html", {"request": db, "posts": posts})

@app.get("/posts/create")
def create_post_form(request: Request):
    """
    Отображает форму для создания поста.

    Args:
        request (Request): Запрос от пользователя.

    Returns:
        TemplateResponse: Шаблон для создания поста.
    """
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/")
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Создает новый пост в базе данных.

    Args:
        post (schemas.PostCreate): Данные для создания поста.
        user_id (int): ID пользователя, создающего пост.
        db (Session): Сессия базы данных.

    Returns:
        dict: Сообщение об успешном создании.
    """
    crud.create_post(db=db, post=post, user_id=user_id)
    return {"message": "Post created successfully"}

@app.get("/posts/edit/{post_id}")
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Отображает форму для редактирования поста.

    Args:
        post_id (int): ID поста, который нужно отредактировать.
        request (Request): Запрос от пользователя.
        db (Session): Сессия базы данных.

    Returns:
        TemplateResponse: Шаблон для редактирования поста.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@app.put("/posts/{post_id}")
def update_post(post_id: int, content: str, db: Session = Depends(get_db)):
    """
    Обновляет содержимое поста.

    Args:
        post_id (int): ID поста для обновления.
        content (str): Новое содержимое поста.
        db (Session): Сессия базы данных.

    Returns:
        dict: Обновленный пост.
    """
    updated_post = crud.update_post_content(db=db, post_id=post_id, new_content=content)
    return updated_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пост по ID.

    Args:
        post_id (int): ID поста для удаления.
        db (Session): Сессия базы данных.

    Returns:
        dict: Сообщение об успешном удалении.
    """
    crud.delete_post(db=db, post_id=post_id)
    return {"message": "Post deleted"}

@app.get("/users/edit/{user_id}")
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Отображает форму для редактирования данных пользователя.

    Args:
        user_id (int): ID пользователя для редактирования.
        request (Request): Запрос от пользователя.
        db (Session): Сессия базы данных.

    Returns:
        TemplateResponse: Шаблон для редактирования пользователя.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.put("/users/{user_id}")
def update_user_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
    """
    Обновляет электронную почту пользователя.

    Args:
        user_id (int): ID пользователя, чью почту нужно обновить.
        new_email (str): Новый email.
        db (Session): Сессия базы данных.

    Returns:
        dict: Обновленный пользователь.
    """
    updated_user = crud.update_user_email(db=db, user_id=user_id, new_email=new_email)
    return updated_user
