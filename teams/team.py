from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from configuration.persistence import Base
from scoring.inject import team_inject_relation


class Team(Base):

    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    services = relationship('Service', order_by='Service.id', backref=backref('team'))
    credentials = relationship('CheckCredentials')
    own_flags = relationship('Flag')
    solved_flags = relationship('FlagDiscovery')

    available_injects = relationship('Inject', secondary=team_inject_relation, backref='teams')
    solved_injects = relationship('InjectSolve')
