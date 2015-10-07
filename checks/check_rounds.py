import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configuration.persistence import Base

__author__ = 'gregd'


class CheckRound(Base):
    __tablename__ = 'check_round'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
    team_checks = relationship('TeamCheckRound', backref='check_round')

    def __init__(self):
        Base.__init__(self)
        self.start = datetime.datetime.now()

    def finish(self):
        self.end = datetime.datetime.now()


class TeamCheckRound(Base):
    __tablename__ = 'team_check_round'

    id = Column(Integer, primary_key=True)
    check_round_id = Column(Integer, ForeignKey('check_round.id'), nullable=False)

    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    team = relationship('Team')

    checks = relationship('CheckResult', backref='checks')