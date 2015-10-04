from sqlalchemy.orm import sessionmaker

from checks.service_checks import CheckCredentials
from checks.services.check_dns import DnsService, DnsCheck
from checks.services.check_mysql import MysqlService, MysqlCheck
from checks.services.check_ssh import SshService, SshCheck
from checks.services.check_web import WebService, WebCheck
from configuration.persistence import Base, engine
from teams.team import Team

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

blue = Team(name='Blue')



# MySQL
mysql = MysqlService('192.168.243.131')
mysql_creds = CheckCredentials(user='greg', password='greg')
mysql.credentials.append(mysql_creds)
mysql.checks.append(MysqlCheck('secret', 'secret_keys'))

# DNS
dns = DnsService('8.8.8.8')
dns.checks.append(DnsCheck('asdf.com', ip='', strict_match=False))
dns.checks.append(DnsCheck('sparsa.org', ip='129.21.24.131', strict_match=True))
dns.checks.append(DnsCheck('google.com', ip='', strict_match=False))

# Web
http = WebService('asdf.com')
https = WebService('sparsa.org')

http.checks.append(WebCheck('http', '', 200, WebCheck.STATUS))
http.checks.append(WebCheck('http', 'not-there.html', 404, WebCheck.STATUS))

https.checks.append(WebCheck('http', '', 200, WebCheck.STATUS))
https.checks.append(WebCheck('http', 'not-there.html', 404, WebCheck.STATUS))
https.checks.append(WebCheck('https', '', 200, WebCheck.STATUS))
https.checks.append(WebCheck('https', 'not-there.html', 404, WebCheck.STATUS))

# SSH
ssh = SshService('192.168.243.100')
ssh.credentials.append(CheckCredentials('greg', 'greg'))
ssh.credentials.append(CheckCredentials('jeff', 'jeff'))
ssh.credentials.append(CheckCredentials('bob', 'bob'))
ssh.checks.append(SshCheck('whoami'))
ssh.checks.append(SshCheck('ls'))


blue.services.append(ssh)
blue.services.append(dns)
blue.services.append(http)
blue.services.append(https)
blue.services.append(mysql)

session.add(blue)
session.commit()

