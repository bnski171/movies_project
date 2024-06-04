from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class FilmWorkBase(BaseModel):
    title: str
    description: Optional[str] = None
    creation_date: Optional[date] = None
    file_path: Optional[str] = None
    rating: Optional[float] = None
    type: str

class FilmWorkCreate(FilmWorkBase):
    pass

class FilmWork(FilmWorkBase):
    id: UUID
    created: Optional[datetime] = None
    modified: Optional[datetime] = None

    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    full_name: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: UUID
    created: Optional[datetime] = None
    modified: Optional[datetime] = None

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: UUID
    created: Optional[datetime] = None
    modified: Optional[datetime] = None

    class Config:
        orm_mode = True

class PersonFilmWorkBase(BaseModel):
    film_work_id: UUID
    person_id: UUID
    role: str

class PersonFilmWorkCreate(PersonFilmWorkBase):
    pass

class PersonFilmWork(PersonFilmWorkBase):
    id: UUID
    created: Optional[datetime] = None

    class Config:
        orm_mode = True

class GenreFilmWorkBase(BaseModel):
    film_work_id: UUID
    genre_id: UUID

class GenreFilmWorkCreate(GenreFilmWorkBase):
    pass

class GenreFilmWork(GenreFilmWorkBase):
    id: UUID
    created: Optional[datetime] = None

    class Config:
        orm_mode = True
