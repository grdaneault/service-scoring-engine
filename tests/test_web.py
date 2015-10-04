import unittest

from checks.services.check_web import WebService, WebCheck
from tests.service_test import ServiceTest


class WebTestCase(ServiceTest):
    def test_web_http(self):
        service = WebService('asdf.com')
        result = service.try_check(WebCheck('http', '', 200, WebCheck.STATUS))
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/ returned 200 (should be 200)', result.message)

    def test_web_http_404(self):
        service = WebService('asdf.com')
        result = service.try_check(WebCheck('http', 'not-there.html', 404, WebCheck.STATUS))
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/not-there.html returned 404 (should be 404)', result.message)

    def test_web_http_content_contains(self):
        service = WebService('asdf.com')
        result = service.try_check(WebCheck('http', '', '<title>asdf</title>', WebCheck.CONTENT_CONTAINS))
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/ contained check content', result.message)

    def test_web_http_content_contains_fail(self):
        service = WebService('asdf.com')
        result = service.try_check(WebCheck('http', '', 'keyword string to match', WebCheck.CONTENT_CONTAINS))
        self.assertEqual(False, result.success)
        self.assertEqual("http://asdf.com/ did not contain 'keyword string to match'", result.message)

    def test_web_http_server_down(self):
        service = WebService('8.8.8.8')
        result = service.try_check(WebCheck('http', '', 200, WebCheck.STATUS))
        self.assertEqual(service.connection_error(), result)

    def test_web_https(self):
        service = WebService('sparsa.org')
        result = service.try_check(WebCheck('https', '', 200, WebCheck.STATUS))
        self.assertEqual(True, result.success)
        self.assertEqual('https://sparsa.org/ returned 200 (should be 200)', result.message)

    def test_web_https_manual_port(self):
        service = WebService('sparsa.org', 443)
        result = service.try_check(WebCheck('https', '', 200, WebCheck.STATUS))
        self.assertEqual(True, result.success)
        self.assertEqual('https://sparsa.org/ returned 200 (should be 200)', result.message)

    def test_web_http_manual_port(self):
        service = WebService('sparsa.org', 80)
        result = service.try_check(WebCheck('http', '', 200, WebCheck.STATUS))
        self.assertEqual(True, result.success)
        self.assertEqual('http://sparsa.org/ returned 200 (should be 200)', result.message)


if __name__ == '__main__':
    unittest.main()
