# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine,
    text,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

env = os.environ.get

db_uri = env('SQLALCHEMY_DATABASE_URI',
             'mysql+mysqldb://{user}:{pwd}@{host:port}/{db}?charset=utf8mb4')

# 'mysql+mysqldb://{user}:{pwd}@{host:port}/{db}?charset=utf8mb4'
# 'postgresql://{user}:{pwd}@{host:port}/{db}'
# 'sqlite:////test.sqlite'

db_engine = create_engine(db_uri, echo=True)

Session = sessionmaker(bind=db_engine)

session = Session()

BaseModel = declarative_base()


def init_db(engine=db_engine):
    BaseModel.metadata.create_all(engine)


def drop_db(engine=db_engine):
    BaseModel.metadata.drop_all(engine)


def query_rows(query, engine=db_engine):
    with engine.begin() as conn:
        # 'SELECT * FROM users'
        rows = conn.execute(query)
        results = [dict(row) for row in rows]
        return results


def execute(sql, engine=db_engine, **kwargs):
    with engine.begin() as conn:
        t = text(sql).bindparams(**kwargs)
        result = conn.execute(t)
        return result


class Relog(BaseModel):
    __tablename__ = 'relog'
    id = Column(Integer, primary_key=True)
    reported_at = Column(DateTime, default=datetime.utcnow)
    is_success = Column(Boolean)
    request_id = Column(String(64))

    def __init__(self, form):
        pass

    def __repr__(self):
        pass

    def save(self):
        session.add(self)
        session.commit()
        return self

    def delete(self):
        session.delete(self)
        session.commit()
        return self


