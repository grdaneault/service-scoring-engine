from checks.services.check_dns import DnsService, DnsCheck
from tests.service_test import ServiceTest

__author__ = 'gregd'

import unittest

class DnsTestCase(ServiceTest):
    def test_lookup_non_strict(self):
        service = DnsService('8.8.8.8')
        result = service.try_check(DnsCheck('google.com', '', False))
        self.assertEqual(True, result.success)
        self.assertEqual('8.8.8.8 resolved google.com correctly', result.message)

    def test_lookup_non_strict_failed(self):
        service = DnsService('8.8.8.8')
        result = service.try_check(DnsCheck('this-domain-is-not-real-1234.com', '', False))
        self.assertEqual(False, result.success)
        self.assertEqual('8.8.8.8 returned no such domain for this-domain-is-not-real-1234.com', result.message)

    def test_lookup_strict(self):
        service = DnsService('8.8.8.8')
        result = service.try_check(DnsCheck('asdf.com', '69.163.240.208', True))
        self.assertEqual(True, result.success)
        self.assertEqual('8.8.8.8 resolved asdf.com correctly to 69.163.240.208', result.message)

    def test_lookup_strict_failed(self):
        service = DnsService('8.8.8.8')
        result = service.try_check(DnsCheck('asdf.com', '127.0.0.127', True))
        self.assertEqual(False, result.success)
        self.assertEqual("8.8.8.8 did not resolve asdf.com to 127.0.0.127 (did get: ['69.163.240.208'])", result.message)

    def test_lookup_server_down(self):
        service = DnsService('8.8.8.9')
        result = service.try_check(DnsCheck('google.com', '', False))
        self.assertEqual(service.timeout(), result)

if __name__ == '__main__':
    unittest.main()
