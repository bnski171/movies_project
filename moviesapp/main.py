from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from uuid import UUID
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not crud.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# FilmWork routes
@app.post("/film_works/", response_model=schemas.FilmWork)
def create_film_work(
    film_work: schemas.FilmWorkCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_film_work(db=db, film_work=film_work)

@app.get("/film_works/{film_work_id}", response_model=schemas.FilmWork)
def read_film_work(film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_film_work = crud.get_film_work(db, film_work_id=film_work_id)
    if db_film_work is None:
        raise HTTPException(status_code=404, detail="Film work not found")
    return db_film_work

@app.get("/film_works/", response_model=List[schemas.FilmWork])
def read_film_works(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    film_works = crud.get_film_works(db, skip=skip, limit=limit)
    return film_works

@app.put("/film_works/{film_work_id}", response_model=schemas.FilmWork)
def update_film_work(film_work_id: UUID, film_work: schemas.FilmWorkCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_film_work = crud.update_film_work(db, film_work_id=film_work_id, film_work=film_work)
    if db_film_work is None:
        raise HTTPException(status_code=404, detail="Film work not found")
    return db_film_work

@app.delete("/film_works/{film_work_id}", response_model=schemas.FilmWork)
def delete_film_work(film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_film_work = crud.delete_film_work(db, film_work_id=film_work_id)
    if db_film_work is None:
        raise HTTPException(status_code=404, detail="Film work not found")
    return db_film_work

# Person routes
@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_person(db=db, person=person)

@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_person(person_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.get("/persons/", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons

@app.put("/persons/{person_id}", response_model=schemas.Person)
def update_person(person_id: UUID, person: schemas.PersonCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person = crud.update_person(db, person_id=person_id, person=person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.delete("/persons/{person_id}", response_model=schemas.Person)
def delete_person(person_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person = crud.delete_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

# Genre routes
@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_genre(db=db, genre=genre)

@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@app.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    genres = crud.get_genres(db, skip=skip, limit=limit)
    return genres

@app.put("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: UUID, genre: schemas.GenreCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre = crud.update_genre(db, genre_id=genre_id, genre=genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@app.delete("/genres/{genre_id}", response_model=schemas.Genre)
def delete_genre(genre_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre = crud.delete_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

# PersonFilmWork routes
@app.post("/person_film_works/", response_model=schemas.PersonFilmWork)
def create_person_film_work(person_film_work: schemas.PersonFilmWorkCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_person_film_work(db=db, person_film_work=person_film_work)

@app.get("/person_film_works/{person_film_work_id}", response_model=schemas.PersonFilmWork)
def read_person_film_work(person_film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person_film_work = crud.get_person_film_work(db, person_film_work_id=person_film_work_id)
    if db_person_film_work is None:
        raise HTTPException(status_code=404, detail="PersonFilmWork not found")
    return db_person_film_work

@app.get("/person_film_works/", response_model=List[schemas.PersonFilmWork])
def read_person_film_works(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    person_film_works = crud.get_person_film_works(db, skip=skip, limit=limit)
    return person_film_works

@app.put("/person_film_works/{person_film_work_id}", response_model=schemas.PersonFilmWork)
def update_person_film_work(person_film_work_id: UUID, person_film_work: schemas.PersonFilmWorkCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person_film_work = crud.update_person_film_work(db, person_film_work_id=person_film_work_id, person_film_work=person_film_work)
    if db_person_film_work is None:
        raise HTTPException(status_code=404, detail="PersonFilmWork not found")
    return db_person_film_work

@app.delete("/person_film_works/{person_film_work_id}", response_model=schemas.PersonFilmWork)
def delete_person_film_work(person_film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_person_film_work = crud.delete_person_film_work(db, person_film_work_id=person_film_work_id)
    if db_person_film_work is None:
        raise HTTPException(status_code=404, detail="PersonFilmWork not found")
    return db_person_film_work

# GenreFilmWork routes
@app.post("/genre_film_works/", response_model=schemas.GenreFilmWork)
def create_genre_film_work(genre_film_work: schemas.GenreFilmWorkCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_genre_film_work(db=db, genre_film_work=genre_film_work)

@app.get("/genre_film_works/{genre_film_work_id}", response_model=schemas.GenreFilmWork)
def read_genre_film_work(genre_film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre_film_work = crud.get_genre_film_work(db, genre_film_work_id=genre_film_work_id)
    if db_genre_film_work is None:
        raise HTTPException(status_code=404, detail="GenreFilmWork not found")
    return db_genre_film_work

@app.get("/genre_film_works/", response_model=List[schemas.GenreFilmWork])
def read_genre_film_works(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    genre_film_works = crud.get_genre_film_works(db, skip=skip, limit=limit)
    return genre_film_works

@app.put("/genre_film_works/{genre_film_work_id}", response_model=schemas.GenreFilmWork)
def update_genre_film_work(genre_film_work_id: UUID, genre_film_work: schemas.GenreFilmWorkCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre_film_work = crud.update_genre_film_work(db, genre_film_work_id=genre_film_work_id, genre_film_work=genre_film_work)
    if db_genre_film_work is None:
        raise HTTPException(status_code=404, detail="GenreFilmWork not found")
    return db_genre_film_work

@app.delete("/genre_film_works/{genre_film_work_id}", response_model=schemas.GenreFilmWork)
def delete_genre_film_work(genre_film_work_id: UUID, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_genre_film_work = crud.delete_genre_film_work(db, genre_film_work_id=genre_film_work_id)
    if db_genre_film_work is None:
        raise HTTPException(status_code=404, detail="GenreFilmWork not found")
    return db_genre_film_work
