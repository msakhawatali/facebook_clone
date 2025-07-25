from sqlalchemy.orm import declarative_base, Session, sessionmaker

from sqlalchemy import create_engine

# Database Connection URL

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sakhawat@localhost/facebook_clone"

# Database Engine Initialization

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLAlchemy Base Class Declaration

Base = declarative_base()

# Database Session Factory

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Database Session Dependency Function

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()