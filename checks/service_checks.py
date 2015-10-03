import abc
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from configuration.persistence import Base


class Service(Base):

    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    host = Column(String(255))
    port = Column(Integer)

    credentials = relationship('CheckCredentials', backref='service')

    discriminator = Column('type', String(20))
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __init__(self, host, port=None):
        Base.__init__(self, host=host, port=port)

    @abc.abstractmethod
    def check(self, check, credentials=None):
        """
        Execute the check for scoring

        :type credentials: CheckCredential
        :param credentials:  Optional credentials to execute the check
        :return:
        """
        return CheckResult()

    def timeout(self):
        """
        Helper utility to represent connection timeout failures

        :return: CheckResult failed
        """
        return CheckResult(False, 'Connection to %s timed out' % self.host)

    def refused(self):
        """
        Helper utility to represent connection refused

        :return: CheckResult failed
        """
        return CheckResult(False, 'Connection to %s refused' % self.host)

    def connection_error(self):
        """
        Helper utility to represent a general connection error

        :return: CheckResult failed
        """
        return CheckResult(False, 'Error connecting to %s' % self.host)

    def invalid_credentials(self, credentials):
        """
        Helper utility to represent a general credential error
        
        :type credentials: CheckCredential
        :param credentials: The invalid credentials
        :return: CheckResult failed
        """
        return CheckResult(False, 'Credential Error.  %s:%s is not authorized for system %s' %
                           (credentials.user, credentials.password, self.host))

class CheckResult(Base):
    __tablename__ = 'check_result'

    id = Column(Integer, primary_key=True)

    success = Column(Boolean)
    message = Column(String(255))

    def __init__(self, success=True, reason=''):
        self.success = success
        self.reason = reason

    def __eq__(self, other):
        return isinstance(other, CheckResult) \
               and self.success == other.success \
               and self.reason == other.reason


class CheckCredentials(Base):
    __tablename__ = 'check_credentials'

    id = Column(Integer, primary_key=True)

    user = Column(String(255))
    password = Column(String(255))
    service_id = Column(Integer, ForeignKey('service.id'))

    def __init__(self, user, password):
        self.user = user
        self.password = password

class CheckRound(Base):
    __tablename__ = 'check_round'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)

    checks = relationship('CheckResult', backref='check_round')
