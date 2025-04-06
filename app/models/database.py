from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "sqlite:////data/publications.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#ORM models
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    journal_id = Column(Integer, ForeignKey("journals.id"), nullable=False)
    publication_date = Column(String, nullable=False)

class PublicationAuthor(Base):
    __tablename__ = "publication_authors"
    publication_id = Column(Integer, ForeignKey("publications.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)