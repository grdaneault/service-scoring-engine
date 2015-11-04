from configuration.cdt.austin_ad import AustinAd
from configuration.cdt.carter_web import CarterWeb
from configuration.cdt.dillon_dns import DillonDns
from configuration.cdt.dillon_honeypot import DillonHoneypot
from configuration.cdt.email import Email
from configuration.cdt.jason_telnet import JasonTelnet
from configuration.cdt.spicer_api import SpicerApi
from configuration.cdt.jason_ftp import JasonFtp
from configuration.cdt.jason_web import JasonWeb

machines = [
    AustinAd(),         # Domain Controller
    CarterWeb(),        # Wiki                      wiki.oldengland.com
    DillonDns(),        # DNS                       dns1.oldengland.com
    DillonHoneypot(),   # Honeypot
    Email(),            # Email Server
    JasonFtp(),         # FTP Server                ftp.oldengland.com
    JasonTelnet(),      # Telnet Server             cinema
    JasonWeb(),         # Game Server
    SpicerApi()         # Banquo (API Server)
]
