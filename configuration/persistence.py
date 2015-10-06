from flask.ext.sqlalchemy import _QueryProperty
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://greg:greg@192.168.243.100/scoring_engine')

