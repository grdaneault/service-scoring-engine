import abc

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from checks.check import CheckResult
from configuration.persistence import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)

    is_enabled = Column(Boolean, nullable=False, default=True)

    discriminator = Column('type', String(20))
    __mapper_args__ = {'polymorphic_on': discriminator}

    check_results = relationship('ServiceCheckRound', backref='service')

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
        if not credentials:
            return self.missing_credentials()

        return CheckResult(False, 'Credential Error.  %s:%s is not authorized for system %s' %
                           (credentials.user, credentials.password, self.host))

    def missing_credentials(self):
        """
        Helper utility to represent the error when a check requires credentials but the team does not have any stored
        :return: CheckResult failed
        """
        return CheckResult(False, 'Missing Credentials for check on %s' % self.host)


