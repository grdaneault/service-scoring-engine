from checks.service_checks import CheckCredentials
from checks.services.check_ssh import SshService, SshCheck
from tests.service_test import ServiceTest

import unittest


class SshTestCase(ServiceTest):
    def test_ssh(self):
        service = SshService('192.168.243.100')
        creds = CheckCredentials('greg', 'greg')
        result = service.try_check(SshCheck('ls'), creds)
        self.assertEqual('Command ls executed against 192.168.243.100 by greg', result.message)
        self.assertEqual(True, result.success)

    def test_ssh_bad_command(self):
        service = SshService('192.168.243.100')
        creds = CheckCredentials('greg', 'greg')
        result = service.try_check(SshCheck('false'), creds)
        self.assertEqual('Command false exited with code 1 when run against 192.168.243.100 by greg', result.message)
        self.assertEqual(False, result.success)

    def test_ssh_bad_creds(self):
        service = SshService('192.168.243.100')
        creds = CheckCredentials('greg', 'bad_pass')
        result = service.try_check(SshCheck('ls'), creds)
        self.assertEqual(service.invalid_credentials(creds), result)

    def test_ssh_no_connection(self):
        service = SshService('192.168.243.10')
        creds = CheckCredentials('greg', 'greg')
        result = service.try_check(SshCheck('ls'), creds)
        self.assertEqual(service.timeout(), result)

    def test_ssh_connection_refused(self):
        service = SshService('192.168.243.100', 1234)
        creds = CheckCredentials('greg', 'greg')
        result = service.try_check(SshCheck('ls'), creds)
        self.assertEqual(service.refused(), result)

if __name__ == '__main__':
    unittest.main()
