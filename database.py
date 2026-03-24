from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root@localhost/cardapio"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# função que você perguntou 👇
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()