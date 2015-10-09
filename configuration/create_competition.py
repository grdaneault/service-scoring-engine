from sqlalchemy.orm import sessionmaker
from checks import CheckCredentials

from checks.services.check_dns import DnsService, DnsCheck
from checks.services.check_ftp import FtpService, FtpCheck
from checks.services.check_mysql import MysqlService, MysqlCheck
from checks.services.check_ping import PingService, PingCheck
from checks.services.check_ssh import SshService, SshCheck
from checks.services.check_web import WebService, WebCheck
from configuration.models import create_tables
from scoreboard.app import db, user_manager
from teams.user import User
from teams.team import Team

create_tables(db.engine)

Session = sessionmaker(bind=db.engine)
session = Session()

white = Team(name='White')
blue = Team(name='Blue')
red = Team(name='Red')

def create_mysql_service(server, credentials):
    mysql = MysqlService(server)
    mysql.checks.append(MysqlCheck(database='secret',
                                   table='secret_keys',
                                   credentials=credentials))
    return mysql

def create_dns_service(server):
    dns = DnsService(server)
    dns.checks.append(DnsCheck('dns.team1.ists', ip='192.168.159.100', strict_match=True))
    dns.checks.append(DnsCheck('www.team1.ists', ip='192.168.159.110', strict_match=True))
    dns.checks.append(DnsCheck('ftp.team1.ists', ip='192.168.159.110', strict_match=True))
    dns.checks.append(DnsCheck('ssh.team1.ists', ip='192.168.159.120', strict_match=False))
    dns.checks.append(DnsCheck('mail.team1.ists', ip='192.168.159.130', strict_match=True))
    dns.checks.append(DnsCheck('smtp.team1.ists', ip='192.168.159.130', strict_match=True))
    dns.checks.append(DnsCheck('pop.team1.ists', ip='192.168.159.130', strict_match=True))
    dns.checks.append(DnsCheck('irc.team1.ists', ip='192.168.159.140', strict_match=True))
    dns.checks.append(DnsCheck('db.team1.ists', ip='192.168.159.150', strict_match=True))
    return dns

def create_web_service(server, protocol):
    web = WebService(server)
    web.checks.append(WebCheck(protocol, '', 200, WebCheck.STATUS, value=5))
    web.checks.append(WebCheck(protocol, '', 'It works', WebCheck.CONTENT_CONTAINS, value=10))
    web.checks.append(WebCheck(protocol, 'not-there.html', 404, WebCheck.STATUS, value=5))
    return web

def create_ssh_service(server, credentials):
    ssh = SshService(server)
    ssh.checks.append(SshCheck(credentials=credentials))
    ssh.checks.append(SshCheck(command='ls', credentials=credentials))
    return ssh

def create_ftp_service(server, credentials):
    ftp = FtpService(server)
    ftp.checks.append(FtpCheck(is_anonymous=False, operation=FtpCheck.UPLOAD, credentials=credentials))
    ftp.checks.append(FtpCheck(is_anonymous=False, operation=FtpCheck.LIST, credentials=credentials))
    ftp.checks.append(FtpCheck(is_anonymous=True, operation=FtpCheck.LIST))
    return ftp

def create_ping_service(network):
    ping = PingService(network)
    for host in range(10, 50, 10):
        ping.checks.append(PingCheck('192.168.159.1%s' % host))
    return ping

blue_credentials = [
    CheckCredentials('greg', 'greg'),
    CheckCredentials('jeff', 'jeff'),
    CheckCredentials('bob', 'bob')
]

blue.services.append(create_dns_service('192.168.159.100'))
blue.services.append(create_ftp_service('ftp.team1.ists', blue_credentials[1:2]))
blue.services.append(create_web_service('192.168.159.110', 'http'))
blue.services.append(create_web_service('www.team1.ists', 'https'))
blue.services.append(create_ssh_service('ssh.team1.ists', blue_credentials))
blue.services.append(create_mysql_service('db.team1.ists', blue_credentials[0:1]))
blue.services.append(create_ping_service('192.168.159.0/24'))

blue.credentials.extend(blue_credentials)

for team in [white, blue, red]:
    password = team.name + '123'
    user = User(username=team.name.lower(),
                password=user_manager.hash_password(password),
                active=True,
                team=team)
    session.add(team)
    session.add(user)
session.commit()

