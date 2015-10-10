from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://greg:greg@192.168.159.200/scoring_engine')

