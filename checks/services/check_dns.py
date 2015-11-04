import dns.resolver
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from checks import CheckResult, ServiceCheck
from checks.services import Service


class DnsService(Service):

    def requires_credentials(self, check):
        return False

    def friendly_name(self):
        return 'DNS Server'

    __mapper_args__ = {'polymorphic_identity': 'dns'}

    checks = relationship('DnsCheck', backref='service')

    def __init__(self, host, port=53):
        Service.__init__(self, host, port)

    def run_check(self, check, credentials=None):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.host]
        resolver.timeout = Service.TIMEOUT
        resolver.lifetime = Service.TIMEOUT

        try:
            answer = resolver.query(check.hostname)
        except dns.resolver.NXDOMAIN:
            return CheckResult(False, '%s returned no such domain for %s' % (self.host, check.hostname))
        except dns.exception.Timeout:
            return self.timeout()

        if check.strict_match:
            found = False
            for record in answer:
                if record.address == check.ip:
                    found = True
                    break

            if found:
                return CheckResult(True, '%s resolved %s correctly to %s' % (self.host, check.hostname, check.ip))
            else:
                return CheckResult(False, '%s did not resolve %s to %s (did get: %s)' %
                                   (self.host, check.hostname, check.ip, str([record.address for record in answer])))
        else:
            return CheckResult(True, '%s resolved %s correctly' % (self.host, check.hostname))


class DnsCheck(ServiceCheck):
    __tablename__ = 'check_detail_dns'
    __mapper_args__ = {'polymorphic_identity': 'dns'}

    dns_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    hostname = Column(String(255), nullable=False)
    ip = Column(String(45), nullable=True)
    strict_match = Column(Boolean, nullable=False, default=False)

    def __init__(self, hostname, ip, strict_match=True, value=1):
        ServiceCheck.__init__(self, value=value)
        self.hostname = hostname
        self.ip = ip
        self.strict_match = strict_match

        if not ip and strict_match:
            raise ValueError('strict match requires an IP')

    def __str__(self):
        strict_str = self.ip if self.strict_match else "non-strict"
        return '<DnsCheck of %s \'%s\' (%s)>' % (self.service.host, strict_str, self.hostname)

    def friendly_name(self):
        requirement = 'to %s' % self.ip if self.strict_match else 'correctly'
        return 'Checking that %s resolves %s.' % (self.hostname, requirement)


