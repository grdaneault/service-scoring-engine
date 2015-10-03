import requests
import requests.exceptions
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from checks.service_checks import Service, CheckResult


# Disable the warning about self-signed certs
import requests.packages.urllib3
from configuration.persistence import Base

requests.packages.urllib3.disable_warnings()

DEFAULT_PORTS = {'http': 80, 'https': 443}


class WebService(Service):

    __mapper_args__ = {'polymorphic_identity': 'web'}
    checks = relationship('WebCheck', backref='checks')

    def __init__(self, host, port=80):
        Service.__init__(self, host, port)

    def get_url(self, check):
        port_str = ':%s' % self.port if self.port != DEFAULT_PORTS[check.protocol] else ""
        return '%s://%s%s/%s' % (check.protocol, self.host, port_str, check.path)

    def check(self, check, credentials=None):
        try:
            result = requests.get(self.get_url(check), timeout=2, verify=False)

            if check.check_type == WebService.STATUS:
                return CheckResult(result.status_code == int(check.content), '%s returned %s (should be %s)' %
                                   (self.get_url(check), result.status_code, check.content))
            elif check.check_type == WebService.CONTENT_CONTAINS:
                if check.content in result.text:
                    return CheckResult(True, '%s contained check content' % self.get_url(check))
                else:
                    return CheckResult(False, '%s did not contain \'%s\'' % (self.get_url(check), check.content))
            else:
                return CheckResult(result.status_code == 200, '%s returned %s (should be 200)' %
                                   (self.get_url(check), result.status_code))
        except requests.exceptions.ConnectionError:
            return self.connection_error()
        except requests.exceptions.Timeout:
            return self.timeout()
        except requests.exceptions.TooManyRedirects:
            return self.too_many_redirects(check)

    def too_many_redirects(self, check):
        return CheckResult(False, 'Too many redirects experienced when accessing %s' % self.get_url(check))


class WebCheck(Base):

    __tablename__ = 'check_detail_web'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))

    path = Column(String(255))
    protocol = Column(String(50))
    content = Column(Text)
    check_type = Column(String(50))

    STATUS = 'status'
    CONTENT_CONTAINS = 'contentContains'
    CONTENT_MATCHES = 'contentMatches'

    def __init__(self, protocol, path, content, check_type):
        self.protocol = protocol
        self.path = path
        self.content = content
        self.check_type = check_type
