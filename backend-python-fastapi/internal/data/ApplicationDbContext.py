
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from internal.Entities import Base

#DATABASE_URL: str = "postgresql://postgres:postgres@db-postgres:5432/mai_master_degree_systems_analysis"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mai_master_degree_systems_analysis")

class ApplicationDbContext(object):
    
    def init_db() -> None:
        engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(engine)

    def create_session():
        engine = create_engine(DATABASE_URL, echo = False, pool_size=10, max_overflow=20)
        Session = sessionmaker(bind = engine)
        session = Session()
        return session