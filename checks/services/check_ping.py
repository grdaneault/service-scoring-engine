import shlex
import platform
import subprocess

from sqlalchemy import Column, String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from checks.service_checks import Service, CheckResult, ServiceCheck, ForeignKey


class PingService(Service):
    __mapper_args__ = {'polymorphic_identity': 'icmp'}
    checks = relationship('PingCheck', backref='service')

    def __init__(self):
        Service.__init__(self, '', None)

    def run_check(self, check, credentials=None):
        count_arg = 'n' if platform.platform() == 'Windows' else 'c'
        try:
            subprocess.check_output(['ping', '-%s' % count_arg, '1', shlex.quote(check.host)])
            return CheckResult(True, 'Host %s is up' % check.host)
        except subprocess.CalledProcessError as err:
            return CheckResult(False, 'Host %s is down (response: %d)' % (check.host, err.returncode))

    def requires_credentials(self, check):
        return False


class PingCheck(ServiceCheck):
    __tablename__ = 'check_detail_ping'
    __mapper_args__ = {'polymorphic_identity': 'icmp'}

    ping_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)
    host = Column(String(255), nullable=False)

    def __init__(self, host, value=5):
        ServiceCheck.__init__(self, value=value)
        self.host = host

    def __str__(self):
        return '<PingCheck of %s>' % self.host
