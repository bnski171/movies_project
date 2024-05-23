from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID

# FilmWork CRUD operations
def get_film_work(db: Session, film_work_id: UUID):
    return db.query(models.FilmWork).filter(models.FilmWork.id == film_work_id).first()

def get_film_works(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FilmWork).offset(skip).limit(limit).all()

def create_film_work(db: Session, film_work: schemas.FilmWorkCreate):
    db_film_work = models.FilmWork(**film_work.dict())
    db.add(db_film_work)
    db.commit()
    db.refresh(db_film_work)
    return db_film_work

def update_film_work(db: Session, film_work_id: UUID, film_work: schemas.FilmWorkCreate):
    db_film_work = db.query(models.FilmWork).filter(models.FilmWork.id == film_work_id).first()
    if db_film_work:
        for key, value in film_work.dict().items():
            setattr(db_film_work, key, value)
        db.commit()
        db.refresh(db_film_work)
    return db_film_work

def delete_film_work(db: Session, film_work_id: UUID):
    db_film_work = db.query(models.FilmWork).filter(models.FilmWork.id == film_work_id).first()
    if db_film_work:
        db.delete(db_film_work)
        db.commit()
    return db_film_work

# Person CRUD operations
def get_person(db: Session, person_id: UUID):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: UUID, person: schemas.PersonCreate):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person:
        for key, value in person.dict().items():
            setattr(db_person, key, value)
        db.commit()
        db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: UUID):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person

# Genre CRUD operations
def get_genre(db: Session, genre_id: UUID):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()

def get_genres(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_genre(db: Session, genre_id: UUID, genre: schemas.GenreCreate):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre:
        for key, value in genre.dict().items():
            setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, genre_id: UUID):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre:
        db.delete(db_genre)
        db.commit()
    return db_genre

# PersonFilmWork CRUD operations
def get_person_film_work(db: Session, person_film_work_id: UUID):
    return db.query(models.PersonFilmWork).filter(models.PersonFilmWork.id == person_film_work_id).first()

def get_person_film_works(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PersonFilmWork).offset(skip).limit(limit).all()

def create_person_film_work(db: Session, person_film_work: schemas.PersonFilmWorkCreate):
    db_person_film_work = models.PersonFilmWork(**person_film_work.dict())
    db.add(db_person_film_work)
    db.commit()
    db.refresh(db_person_film_work)
    return db_person_film_work

def update_person_film_work(db: Session, person_film_work_id: UUID, person_film_work: schemas.PersonFilmWorkCreate):
    db_person_film_work = db.query(models.PersonFilmWork).filter(models.PersonFilmWork.id == person_film_work_id).first()
    if db_person_film_work:
        for key, value in person_film_work.dict().items():
            setattr(db_person_film_work, key, value)
        db.commit()
        db.refresh(db_person_film_work)
    return db_person_film_work

def delete_person_film_work(db: Session, person_film_work_id: UUID):
    db_person_film_work = db.query(models.PersonFilmWork).filter(models.PersonFilmWork.id == person_film_work_id).first()
    if db_person_film_work:
        db.delete(db_person_film_work)
        db.commit()
    return db_person_film_work

# GenreFilmWork CRUD operations
def get_genre_film_work(db: Session, genre_film_work_id: UUID):
    return db.query(models.GenreFilmWork).filter(models.GenreFilmWork.id == genre_film_work_id).first()

def get_genre_film_works(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.GenreFilmWork).offset(skip).limit(limit).all()

def create_genre_film_work(db: Session, genre_film_work: schemas.GenreFilmWorkCreate):
    db_genre_film_work = models.GenreFilmWork(**genre_film_work.dict())
    db.add(db_genre_film_work)
    db.commit()
    db.refresh(db_genre_film_work)
    return db_genre_film_work

def update_genre_film_work(db: Session, genre_film_work_id: UUID, genre_film_work: schemas.GenreFilmWorkCreate):
    db_genre_film_work = db.query(models.GenreFilmWork).filter(models.GenreFilmWork.id == genre_film_work_id).first()
    if db_genre_film_work:
        for key, value in genre_film_work.dict().items():
            setattr(db_genre_film_work, key, value)
        db.commit()
        db.refresh(db_genre_film_work)
    return db_genre_film_work

def delete_genre_film_work(db: Session, genre_film_work_id: UUID):
    db_genre_film_work = db.query(models.GenreFilmWork).filter(models.GenreFilmWork.id == genre_film_work_id).first()
    if db_genre_film_work:
        db.delete(db_genre_film_work)
        db.commit()
    return db_genre_film_work
