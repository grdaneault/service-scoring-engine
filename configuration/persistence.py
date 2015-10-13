from sqlalchemy.ext.declarative import declarative_base
from configuration.web_configuration import ConfigClass

Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine(ConfigClass.SQLALCHEMY_DATABASE_URI)

