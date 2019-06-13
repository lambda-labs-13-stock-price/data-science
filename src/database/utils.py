from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def connect(username, password, host, port, drivername='postgres'):
    postgres_db = {
        'drivername': drivername,
        'username': username,
        'password': password,
        'host': host,
        'port': port
    }

    url = URL(**postgres_db).__to_string__()
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)

    return Session()
