from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text
from sqlalchemy.orm import relationship
from configuration.persistence import Base

__author__ = 'gregd'


class ServiceCheck(Base):
    __tablename__ = 'service_check'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    check_type = Column('type', String(50), nullable=False)
    value = Column(Integer, nullable=False, default=50)

    results = relationship('CheckResult', backref='check', lazy='noload')
    __mapper_args__ = {'polymorphic_on': check_type}

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)


class CheckResult(Base):
    __tablename__ = 'check_result'

    id = Column(Integer, primary_key=True)
    check_id = Column(Integer, ForeignKey('service_check.id'), nullable=False)
    team_check_round_id = Column(Integer, ForeignKey('team_check_round.id'), nullable=False)

    success = Column(Boolean, nullable=False, default=False)
    message = Column(Text, nullable=False, default='')

    def __init__(self, success=True, message=''):
        self.success = success
        self.message = message

    def __eq__(self, other):
        return isinstance(other, CheckResult) \
               and self.success == other.success \
               and self.message == other.message

    def __str__(self):
        return 'Check<%s, %s>' % (self.success, self.message)


class CheckCredentials(Base):
    __tablename__ = 'check_credentials'

    id = Column(Integer, primary_key=True)

    user = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password