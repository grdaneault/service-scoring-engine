import datetime
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from configuration.persistence import Base


class Flag(Base):
    __tablename__ = 'flag'
    id = Column(Integer, primary_key=True)
    flag = Column(String(255), nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
    description = Column(Text, nullable=True)
    value = Column(Integer, nullable=False, default=200)



class FlagDiscovery(Base):
    __tablename__ = 'flag_discovery'
    id = Column(Integer, primary_key=True)
    flag_id = Column(Integer, ForeignKey('flag.id'))
    flag = relationship('Flag', backref='discoveries')
    team_id = Column(Integer, ForeignKey('team.id'))
    discovery_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    discovery_user = relationship('User')

    date_discovered = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.date_discovered = datetime.datetime.now()
