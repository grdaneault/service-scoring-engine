from checks.service_checks import CheckCredential
from checks.ssh import SshCheck

__author__ = 'gregd'

import unittest


class SshTestCase(unittest.TestCase):
    def test_ssh(self):
        check = SshCheck('192.168.243.100')
        creds = CheckCredential('greg', 'greg')
        result = check.execute(creds)
        self.assertEqual('Successful SSH login for greg on 192.168.243.100', result.reason)
        self.assertEqual(True, result.success)

    def test_ssh_bad_creds(self):
        check = SshCheck('192.168.243.100')
        creds = CheckCredential('greg', 'notgreg')
        result = check.execute(creds)
        self.assertEqual(check.invalid_credentials(creds), result)

    def test_ssh_no_connection(self):
        check = SshCheck('192.168.243.10')
        creds = CheckCredential('greg', 'greg')
        result = check.execute(creds)
        self.assertEqual(check.timeout(), result)

    def test_ssh_connection_refused(self):
        check = SshCheck('192.168.243.100', 1234)
        creds = CheckCredential('greg', 'greg')
        result = check.execute(creds)
        self.assertEqual(check.refused(), result)

if __name__ == '__main__':
    unittest.main()
