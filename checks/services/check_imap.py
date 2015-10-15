import imaplib
import requests
import requests.exceptions
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship



# Disable the warning about self-signed certs
import requests.packages.urllib3
from checks import CheckResult, ServiceCheck
from checks.services import Service

requests.packages.urllib3.disable_warnings()

class ImapService(Service):

    def requires_credentials(self, check):
        return True

    def friendly_name(self):
        return 'Email Server (IMAP)'

    __mapper_args__ = {'polymorphic_identity': 'imap'}
    checks = relationship('ImapCheck', backref='service')

    def __init__(self, host, port):
        Service.__init__(self, host, port)

    def run_check(self, check, credentials=None):
        try:
            if check.protocol == 'IMAP4':
                mailbox = imaplib.IMAP4(self.host)
            else:
                mailbox = imaplib.IMAP4_SSL(self.host)

            mailbox.login(credentials.user, credentials.password)
            return CheckResult(True, 'Successful imap login for %s' % credentials.user)
        except imaplib.IMAP4.error as e:
            return CheckResult(False, 'IMAP Error: %s' % e)

    def __str__(self):
        return '<IMAP Server on %s:%s>' % (self.host, self.port)



class ImapCheck(ServiceCheck):
    __tablename__ = 'check_detail_imap'
    __mapper_args__ = {'polymorphic_identity': 'imap'}

    imap_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    protocol = Column(String(50))

    def __init__(self, protocol, value=2):
        ServiceCheck.__init__(self, value=value)
        self.protocol = protocol

    def __str__(self):
        return '<ImapCheck of \'%s\' using %s>' % (self.service.host, self.protocol)

    def friendly_name(self):
        return 'Check login for email using %s ' % self.protocol