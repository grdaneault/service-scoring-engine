import abc
import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from configuration.persistence import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)

    credentials = relationship('CheckCredentials', backref='service')

    discriminator = Column('type', String(20))
    __mapper_args__ = {'polymorphic_on': discriminator}

    TIMEOUT = 10

    def __init__(self, host, port=None):
        Base.__init__(self, host=host, port=port)

    @abc.abstractmethod
    def requires_credentials(self, check):
        """
        Gets whether the given checks requires credentials to execute

        :param check:
        :return: True, if needed.  False otherwise.
        """
        return False

    @abc.abstractmethod
    def run_check(self, check, credentials=None):
        """
        Execute the check for scoring

        :type credentials: CheckCredential
        :param credentials:  Optional credentials to execute the check
        :return:
        """
        return CheckResult()

    @abc.abstractstaticmethod
    def friendly_name(self):
        return 'Service Check'

    def try_check(self, check, credentials=None):
        if self.requires_credentials(check) and not credentials:
            result = self.missing_credentials()
        else:
            result = self.run_check(check, credentials)

        result.check = check
        return result

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

    def missing_credentials(self):
        """
        Helper utility to represent the error when a check requires credentials but the team does not have any stored
        :return: CheckResult failed
        """
        return CheckResult(False, 'Missing Credentials for check on' % self.host)


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
