__author__ = 'gregd'
from checks.services import check_ftp, check_dns, check_web, check_ssh, check_ping, check_mysql

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
