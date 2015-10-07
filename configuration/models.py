from configuration.persistence import Base
import teams
from checks import service_checks
from checks.services import check_ftp, check_dns, check_web, check_ssh, check_ping, check_mysql

class Models:
    User = teams.User
    Team = teams.Team

    # Service Base
    Service = service_checks.Service
    ServiceCheck = service_checks.ServiceCheck
    CheckCredentials = service_checks.CheckCredentials
    CheckResult = service_checks.CheckResult
    CheckRound = service_checks.CheckRound
    TeamCheckRound = service_checks.TeamCheckRound

    # Services
    DnsService = check_dns.DnsService
    DnsCheck = check_dns.DnsCheck
    FtpService = check_ftp.FtpService
    FtpCheck = check_ftp.FtpCheck
    MysqlService = check_mysql.MysqlService
    MysqlCheck = check_mysql.MysqlCheck
    PingService = check_ping.PingService
    PingCheck = check_ping.PingCheck
    SshService = check_ssh.SshService
    SshCheck = check_ssh.SshCheck
    WebService = check_web.WebService
    WebCheck = check_web.WebCheck

    @staticmethod
    def create_tables(engine):
        Base.metadata.create_all(engine)
