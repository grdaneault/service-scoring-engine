import requests
import requests.exceptions
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from ldap3 import Server, Connection, ALL, LDAPException



# Disable the warning about self-signed certs
import requests.packages.urllib3
from checks import CheckResult, ServiceCheck
from checks.services import Service

requests.packages.urllib3.disable_warnings()

class LdapService(Service):

    def requires_credentials(self, check):
        return False

    def friendly_name(self):
        return 'Ldap Server (AD)'

    __mapper_args__ = {'polymorphic_identity': 'ldap'}
    checks = relationship('LdapCheck', backref='service')

    def __init__(self, host, port):
        Service.__init__(self, host, port)

    def run_check(self, check, credentials=None):
        try:
            server = Server(self.host, get_info=ALL)
            connection = Connection(server, auto_bind=True)
            if check.expected_info in server.info:
                return CheckResult(True, 'Successful ldap verification.')
            else:
                return CheckResult(False, 'LDAP Server missing info \'%s\'' % check.expected_info)
        except LDAPException as e:
            return CheckResult(False, 'LDAP Error: %s' % e)

    def __str__(self):
        return '<LDAP Server on %s>' % self.host



class LdapCheck(ServiceCheck):
    __tablename__ = 'check_detail_imap'
    __mapper_args__ = {'polymorphic_identity': 'ldap'}

    imap_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    expected_info = Column(Text)

    def __init__(self, expected_info, value=10):
        ServiceCheck.__init__(self, value=value)
        self.expected_info = expected_info

    def __str__(self):
        return '<LdapCheck of \'%s\' for %s>' % (self.service.host, self.expected_info)

    def friendly_name(self):
        return 'Check Active Directory LDAP Server availability on %s ' % self.service.host
