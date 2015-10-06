import unittest

from checks.services.check_ping import PingService
from tests.service_test import ServiceTest


class PingTestCase(ServiceTest):
    def test_ping(self):
        service = PingService('192.168.243.131')
        result = service.try_check(service.checks[0])

        self.assertEqual(True, result.success)
        self.assertEqual('Host 192.168.243.131 is up', result.message)

    def test_ping_down(self):
        service = PingService('192.168.243.123')
        result = service.try_check(service.checks[0])

        self.assertEqual(False, result.success)
        self.assertEqual('Host 192.168.243.123 is down', result.message)


if __name__ == '__main__':
    unittest.main()
