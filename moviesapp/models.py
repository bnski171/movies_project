from sqlalchemy import Column, String, Text, Date, Float, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .database import Base

class FilmWork(Base):
    __tablename__ = 'film_work'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    creation_date = Column(Date)
    file_path = Column(Text)
    rating = Column(Float)
    type = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))
    genres = relationship('Genre', secondary='content.genre_film_work', back_populates='film_works')
    persons = relationship('Person', secondary='content.person_film_work', back_populates='film_works')

class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))
    film_works = relationship('FilmWork', secondary='content.person_film_work', back_populates='persons')

class Genre(Base):
    __tablename__ = 'genre'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))
    film_works = relationship('FilmWork', secondary='content.genre_film_work', back_populates='genres')

class PersonFilmWork(Base):
    __tablename__ = 'person_film_work'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    film_work_id = Column(UUID(as_uuid=True), ForeignKey('content.film_work.id', ondelete='CASCADE'), nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey('content.person.id', ondelete='CASCADE'), nullable=False)
    role = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))

class GenreFilmWork(Base):
    __tablename__ = 'genre_film_work'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    film_work_id = Column(UUID(as_uuid=True), ForeignKey('content.film_work.id', ondelete='CASCADE'), nullable=False)
    genre_id = Column(UUID(as_uuid=True), ForeignKey('content.genre.id', ondelete='CASCADE'), nullable=False)
    created = Column(TIMESTAMP(timezone=True))
