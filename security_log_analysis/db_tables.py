# coding: utf-8
from sqlalchemy import (BigInteger, Column, Date, DateTime, ForeignKey, String)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class HostCountry(Base):
    __tablename__ = 'host_country'

    host = Column(String(60), primary_key=True, unique=True)
    code = Column(String(2), nullable=False)


class ApacheLog(Base):
    __tablename__ = 'apache_log'

    datetime = Column(DateTime, nullable=False)
    host = Column(String(15), ForeignKey(u'host_country.host'), nullable=False)


class ApacheLogCloud(Base):
    __tablename__ = 'apache_log_cloud'

    datetime = Column(DateTime, nullable=False)
    host = Column(String(15), ForeignKey(u'host_country.host'), nullable=False)


class CountryCode(Base):
    __tablename__ = 'country_code'
    
    code = Column(String(2), nullable=False)
    country = Column(String(50), nullable=False)


class SSHLog(Base):
    __tablename__ = 'ssh_log'
    datetime = Column(DateTime, nullable=False)
    host = Column(String(60), ForeignKey(u'host_country.host'),
                  nullable=False)
    username = Column(String(15))


class SSHLogCloud(Base):
    __tablename__ = 'ssh_log_cloud'
    datetime = Column(DateTime, nullable=False)
    host = Column(String(60), ForeignKey(u'host_country.host'),
                  nullable=False)
    username = Column(String(15))


class LocalRemoteCompare(Base):
    __tablename__ = 'local_remote_compare'
    
    date = Column(Date)
    local = Column(BigInteger)
    remote = Column(BigInteger)
