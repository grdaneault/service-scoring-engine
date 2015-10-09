import requests
import requests.exceptions
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship



# Disable the warning about self-signed certs
import requests.packages.urllib3
from checks import CheckResult, ServiceCheck
from checks.services import Service

requests.packages.urllib3.disable_warnings()

DEFAULT_PORTS = {'http': 80, 'https': 443}


class WebService(Service):

    def requires_credentials(self, check):
        return False

    def friendly_name(self):
        return 'Web Server'

    __mapper_args__ = {'polymorphic_identity': 'web'}
    checks = relationship('WebCheck', backref='service')

    def __init__(self, host, port=None):
        Service.__init__(self, host, port)

    def get_url(self, check):
        port_str = ':%s' % self.port if self.port and self.port != DEFAULT_PORTS[check.protocol] else ""
        return '%s://%s%s/%s' % (check.protocol, self.host, port_str, check.path)

    def run_check(self, check, credentials=None):
        try:
            result = requests.get(self.get_url(check),
                                  timeout=Service.TIMEOUT,
                                  verify=False)

            if check.check_mode == WebCheck.STATUS:
                return CheckResult(result.status_code == int(check.content), '%s returned %s (should be %s)' %
                                   (self.get_url(check), result.status_code, check.content))
            elif check.check_mode == WebCheck.CONTENT_CONTAINS:
                if check.content in result.text:
                    return CheckResult(True, '%s contained check content' % self.get_url(check))
                else:
                    return CheckResult(False, '%s did not contain \'%s\'' % (self.get_url(check), check.content))
            else:
                return CheckResult(result.status_code == 200, '%s returned %s (should be 200)' %
                                   (self.get_url(check), result.status_code))
        except requests.exceptions.ConnectionError as e:
            return self.connection_error()
        except requests.exceptions.Timeout:
            return self.timeout()
        except requests.exceptions.TooManyRedirects:
            return self.too_many_redirects(check)

    def __str__(self):
        return '<Web Server on %s:%s>' % (self.host, self.port)

    def too_many_redirects(self, check):
        return CheckResult(False, 'Too many redirects experienced when accessing %s' % self.get_url(check))


class WebCheck(ServiceCheck):
    __tablename__ = 'check_detail_web'
    __mapper_args__ = {'polymorphic_identity': 'web'}

    web_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    path = Column(String(255))
    protocol = Column(String(50))
    content = Column(Text)
    check_mode = Column(String(50))

    STATUS = 'status'
    CONTENT_CONTAINS = 'contentContains'
    CONTENT_MATCHES = 'contentMatches'
    CONTENT_HASH = 'contentHash'

    DEFAULT_VALUES = {
        STATUS: 2,
        CONTENT_CONTAINS: 5,
        CONTENT_MATCHES: 5,
        CONTENT_HASH: 10
    }

    def __init__(self, protocol, path, content, check_mode, value=None):
        value = WebCheck.DEFAULT_VALUES[check_mode] if value is None else value
        ServiceCheck.__init__(self, value=value)
        self.protocol = protocol
        self.path = path
        self.content = content
        self.check_mode = check_mode

    def __str__(self):
        return '<WebCheck of \'%s\' for %s>' % (self.service.get_url(self), self.content)

    def friendly_name(self):

        if self.check_mode == WebCheck.STATUS:
            check = 'returns a %s status code for %s' % (self.content, self.service.get_url(self))
        elif self.check_mode in [WebCheck.CONTENT_CONTAINS, WebCheck.CONTENT_MATCHES]:
            check = 'returns a page containing the expected content for %s' % self.service.get_url(self)
        elif self.check_mode == WebCheck.CONTENT_HASH:
            check = 'returns a page with the exact specified content'

        return 'Check that the web server %s.' % check