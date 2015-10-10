from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy import Integer
from configuration.persistence import Base


class Flag(Base):
    __tablename__ = 'flag'
    id = Column(Integer, primary_key=True)
    flag = Column(String(255), nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
    description = Column(Text, nullable=True)



class FlagDiscovery(Base):
    __tablename__ = 'flag_discovery'
    id = Column(Integer, primary_key=True)
    flag_id = Column(Integer, ForeignKey('flag.id'))
    team_id = Column(Integer, ForeignKey('team.id'))

    discovered = Column(DateTime, nullable=False)
