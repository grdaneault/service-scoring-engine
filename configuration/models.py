import checks
from configuration.persistence import Base
import teams


class Models:
    User = teams.User
    Team = teams.Team

    # Service Base
    Service = checks.Service
    ServiceCheck = checks.ServiceCheck
    CheckCredentials = checks.CheckCredentials
    CheckResult = checks.CheckResult
    CheckRound = checks.CheckRound

    # Services
    DnsService = checks.services.DnsService
    DnsCheck = checks.services.DnsCheck
    FtpService = checks.services.FtpService
    FtpCheck = checks.services.FtpCheck
    MysqlService = checks.services.MysqlService
    MysqlCheck = checks.services.MysqlCheck
    PingService = checks.services.PingService
    PingCheck = checks.services.PingCheck
    SshService = checks.services.SshService
    SshCheck = checks.services.SshCheck
    WebService = checks.services.WebService
    WebCheck = checks.services.WebCheck

    @staticmethod
    def create_tables(engine):
        Base.metadata.create_all(engine)
