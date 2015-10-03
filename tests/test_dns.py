from checks.dns import DnsService, DnsCheck
from checks.service_checks import ServiceCheck

__author__ = 'gregd'

import unittest


class DnsTestCase(unittest.TestCase):
    def test_lookup_non_strict(self):
        check = DnsService('8.8.8.8', DnsCheck('google.com', '', False))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('8.8.8.8 resolved google.com correctly', result.reason)

    def test_lookup_non_strict_failed(self):
        check = DnsService('8.8.8.8', DnsCheck('this-domain-is-not-real-1234.com', '', False))
        result = check.execute()
        self.assertEqual(False, result.success)
        self.assertEqual('8.8.8.8 returned no such domain for this-domain-is-not-real-1234.com', result.reason)

    def test_lookup_strict(self):
        check = DnsService('8.8.8.8', DnsCheck('asdf.com', '69.163.240.208', True))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('8.8.8.8 resolved asdf.com correctly to 69.163.240.208', result.reason)

    def test_lookup_strict_failed(self):
        check = DnsService('8.8.8.8', DnsCheck('asdf.com', '127.0.0.127', True))
        result = check.execute()
        self.assertEqual(False, result.success)
        self.assertEqual("8.8.8.8 did not resolve asdf.com to 127.0.0.127 (did get: ['69.163.240.208'])", result.reason)

    def test_lookup_server_down(self):
        check = DnsService('8.8.8.9', DnsCheck('google.com', '', False))
        self.assertEqual(check.timeout(), check.execute())

if __name__ == '__main__':
    unittest.main()
