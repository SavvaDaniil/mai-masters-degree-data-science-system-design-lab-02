
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ApplicationDbContext(object):
    
    def create_session():
        engine = create_engine("postgresql://postgres:postgres@localhost:5432/mai_master_degree_systems_analysis", echo = False, pool_size=10, max_overflow=20)
        Session = sessionmaker(bind = engine)
        session = Session()
        return session