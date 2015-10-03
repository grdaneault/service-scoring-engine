import socket

from sqlalchemy import Column, Integer, ForeignKey, String
import paramiko
from sqlalchemy.orm import relationship

from checks.service_checks import Service, CheckResult
from configuration.persistence import Base


class SshService(Service):
    __mapper_args__ = {'polymorphic_identity': 'ssh'}
    checks = relationship('SshCheck', backref='checks')

    def __init__(self, host, port=22):
        Service.__init__(self, host, port)

    def check(self, check, credentials=None):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host,
                           port=self.port,
                           username=credentials.user,
                           password=credentials.password,
                           timeout=2)

            chan = client.get_transport().open_session()
            chan.exec_command(check.command)
            exit_code = chan.recv_exit_status()
            if 0 == exit_code:
                return CheckResult(True, 'Command %s executed successfully over SSH' % check.command)
            else:
                return CheckResult(False, 'Command %s exited with code %d' % (check.command, exit_code))

        except paramiko.ssh_exception.AuthenticationException:
            return self.invalid_credentials(credentials)
        except socket.timeout:
            return self.timeout()
        except ConnectionRefusedError:
            return self.refused()


class SshCheck(Base):
    __tablename__ = 'check_detail_ssh'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))

    command = Column(String(255))

    def __init__(self, command):
        self.command = command
