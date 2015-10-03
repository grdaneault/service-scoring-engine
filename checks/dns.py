import dns.resolver
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from checks.service_checks import Service, CheckResult
from configuration.persistence import Base


class DnsService(Service):

    __mapper_args__ = {'polymorphic_identity': 'dns'}

    checks = relationship('DnsCheck', backref='checks')

    def __init__(self, host, port=53):
        Service.__init__(self, host, port)

    def check(self, check, credentials=None):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.host]
        resolver.timeout = 2
        resolver.lifetime = 2

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


class DnsCheck(Base):
    __tablename__ = 'check_detail_dns'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))

    hostname = Column(String(255))
    ip = Column(String(45))
    strict_match = Column(Boolean)

    def __init__(self, hostname, ip, strict_match=True):
        self.hostname = hostname
        self.ip = ip
        self.strict_match = strict_match

        if not ip and strict_match:
            raise ValueError('strict match requires an IP')
