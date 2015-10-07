import time
import ftplib
import os

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from checks import CheckResult, ServiceCheck
from checks.services import Service


class FtpService(Service):

    def friendly_name(self):
        return 'FTP Server'

    __mapper_args__ = {'polymorphic_identity': 'ftp'}
    checks = relationship('FtpCheck', backref='service')

    def __init__(self, host, port=21):
        Service.__init__(self, host, port)

    def requires_credentials(self, check):
        return not check.is_anonymous

    def run_check(self, check, credentials=None):
        filename = 'check_%s' % time.time()

        try:
            ftp = ftplib.FTP(self.host, timeout=5)
            if check.is_anonymous:
                ftp.login("anonymous", "check@scoring-engine.com")
            else:
                ftp.login(credentials.user, credentials.password)

            output = []
            if check.operation == FtpCheck.LIST:
                ftp.dir(output.append)
                ftp.quit()

                if output:
                    return CheckResult(True, 'File listing succeeded for server %s' % self.host)
                else:
                    return CheckResult(False, 'File listing failed for server %s' % self.host)
            else:

                check_file = open(filename, 'w')
                check_file.write(filename)
                check_file.close()
                check_file = open(filename, 'rb')
                ftp.storlines('STOR %s' % filename, check_file)
                check_file.close()
                lines = []
                ftp.retrlines('RETR %s' % filename, lines.append)
                os.remove(filename)
                if len(lines) == 1:
                    if lines[0] == filename:
                        return CheckResult(True, 'File upload and download succeeded for server %s' % self.host)
                    else:
                        return CheckResult(False, 'File download with unexpected content from server %s' % self.host)
                else:
                    return CheckResult(False, 'Error downloading file from server %s' % self.host)

        except ftplib.error_reply:
            result = CheckResult(False, 'Unexpected server reply from %s' % self.host)
        except ftplib.error_perm as e:
            result = self.invalid_credentials(credentials)
        except OSError:
            result = self.connection_error()

        if os.path.exists(filename):
            os.remove(filename)

        return result

    def __str__(self):
        return '<Ftp Server on %s>' % self.host



class FtpCheck(ServiceCheck):
    __tablename__ = 'check_detail_ftp'
    __mapper_args__ = {'polymorphic_identity': 'ftp'}

    ftp_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    is_anonymous = Column(Boolean, nullable=False, default=False)
    operation = Column(String(20), nullable=False)

    LIST = 'list'
    UPLOAD = 'write'

    def __str__(self):
        user_str = 'anonymous' if self.is_anonymous else 'authenticated'
        return '<FtpCheck of \'%s\' %s as an %s user>' % (self.service.host, self.operation, user_str)
