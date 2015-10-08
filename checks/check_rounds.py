import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configuration.persistence import Base


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

    service_results = relationship('ServiceCheckRound', backref='team_round')

class ServiceCheckRound(Base):
    __tablename__ = 'service_check_round'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    team_round_id = Column(Integer, ForeignKey('team_check_round.id'))
    results = relationship('CheckResult', backref='service_check_round')


    def get_maximum_service_score(self):
        score = 0
        for result in self.results:
            score += result.check.value

        return score

    def get_service_score(self):
        score = 0
        for result in self.results:
            score += result.check.value if result.success else 0

        return score
