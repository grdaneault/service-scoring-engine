from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from configuration.persistence import Base
from scoring.inject import team_inject_relation, Inject


class Team(Base):

    RED = 'red'
    WHITE = 'white'
    BLUE = 'blue'

    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    role = Column(String(10), nullable=False, default=BLUE)
    ip_space = Column(String(45), nullable=True)
    root_domain = Column(String(45), nullable=True)

    services = relationship('Service', order_by='Service.id', backref=backref('team'))
    credentials = relationship('CheckCredentials')
    own_flags = relationship('Flag')
    solved_flags = relationship('FlagDiscovery')

    available_injects = relationship('Inject', secondary=team_inject_relation, backref='teams')
    solved_injects = relationship('InjectSolve', backref='team')



