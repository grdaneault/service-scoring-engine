from sqlalchemy import Column, String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from checks.service_checks import Service, CheckResult, ServiceCheck
import os
import shlex
import platform

class PingService(Service):
    __mapper_args__ = {'polymorphic_identity': 'icmp'}
    checks = relationship('ServiceCheck', backref='service')

    def __init__(self):
        Service.__init__(self, '', None)

    def run_check(self, check, credentials=None):
        count_arg = 'n' if platform.platform() == 'Windows' else 'c'
        response = os.system('ping -%s 1 %s' % (count_arg, shlex.quote(self.host)))
        if response == 0:
            return CheckResult(True, 'Host %s is up' % self.host)
        else:
            return CheckResult(False, 'Host %s is down' % self.host)

    def requires_credentials(self, check):
        return False


class PingCheck(ServiceCheck):
    __tablename__ = 'check_detail_ping'
    __mapper_args__ = {'polymorphic_identity': 'icmp'}

    ping_id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)

    def __init__(self, host, value=5):
        ServiceCheck.__init__(self, value=value)
        self.host = host
