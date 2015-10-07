import unittest
from checks import CheckCredentials

from checks.services.check_ftp import FtpService, FtpCheck
from tests.service_test import ServiceTest


class FtpTestCase(ServiceTest):
    def test_ftp_anonymous(self):
        service = FtpService('ftp.debian.org')
        result = service.try_check(FtpCheck(is_anonymous=True, operation=FtpCheck.LIST))
        self.assertEqual('File listing succeeded for server ftp.debian.org', result.message)
        self.assertEqual(True, result.success)

    def test_ftp_authenticated_list(self):
        service = FtpService('192.168.243.133')
        result = service.try_check(
            FtpCheck(is_anonymous=False, operation=FtpCheck.LIST),
            CheckCredentials('greg', 'greg')
        )
        self.assertEqual('File listing succeeded for server 192.168.243.133', result.message)
        self.assertEqual(True, result.success)

    def test_ftp_authenticated_upload(self):
        service = FtpService('192.168.243.133')
        result = service.try_check(
            FtpCheck(is_anonymous=False, operation=FtpCheck.UPLOAD),
            CheckCredentials('greg', 'greg')
        )
        self.assertEqual('File upload and download succeeded for server 192.168.243.133', result.message)
        self.assertEqual(True, result.success)

    def test_ftp_authenticated_bad_credentials_list(self):
        service = FtpService('192.168.243.133')
        credentials = CheckCredentials('greg', 'bad_pass')
        result = service.try_check(
            FtpCheck(is_anonymous=False, operation=FtpCheck.LIST),
            credentials
        )
        self.assertEqual(service.invalid_credentials(credentials), result)

    def test_ftp_authenticated_bad_credentials_upload(self):
        service = FtpService('192.168.243.133')
        credentials = CheckCredentials('greg', 'bad_pass')
        result = service.try_check(
            FtpCheck(is_anonymous=False, operation=FtpCheck.UPLOAD),
            credentials
        )
        self.assertEqual(service.invalid_credentials(credentials), result)

if __name__ == '__main__':
    unittest.main()
