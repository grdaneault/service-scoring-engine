from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from configuration.persistence import Base


class Team(Base):

    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    services = relationship('Service', order_by='Service.id', backref=backref('team'))
