# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine,
    text,
    orm,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql.base import MEDIUMTEXT

import os

env = os.environ.get

db_uri = env('SQLALCHEMY_DATABASE_URI',
             'mysql+mysqldb://{user}:{pwd}@{host:port}/{db}?charset=utf8mb4')

# 'mysql+mysqldb://{user}:{pwd}@{host:port}/{db}?charset=utf8mb4'
# 'postgresql://{user}:{pwd}@{host:port}/{db}'
# 'sqlite:////test.sqlite'

db_engine = create_engine(db_uri, echo=True)

Session = orm.sessionmaker(bind=db_engine)

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


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Book(BaseModel):
    __tablename__ = 'relog'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    create_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    readers = orm.relationship('User', uselist=True, backref=orm.backref('book', lazy='select'))
    title = Column(String(64))
    content = Column(MEDIUMTEXT)

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
