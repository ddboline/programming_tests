#!/usr/bin/python3

import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from binascii import b2a_hex, a2b_hex, b2a_base64

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

print(Base.metadata.create_all(engine))

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name, ed_user.password, ed_user.id)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()
print(our_user, our_user.id)

session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'), User(name='mary', fullname='Mary Contrary', password='xxg527'), User(name='fred', fullname='Fred Flinstone', password='blah')])

print(session.new)

session.commit()

for u in session.query(User).filter_by(password='foobar').all():
    u.password = b2a_base64(os.urandom(12))

print(session.query(User).all())
