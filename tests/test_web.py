from checks.web import WebService, WebCheck

import unittest


class WebTestCase(unittest.TestCase):
    def test_web_http(self):
        check = WebService('asdf.com', 'http', WebCheck('', 200, WebService.STATUS))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/ returned 200 (should be 200)', result.reason)

    def test_web_http_404(self):
        check = WebService('asdf.com', 'http', WebCheck('not-there.html', 404, WebService.STATUS))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/not-there.html returned 404 (should be 404)', result.reason)

    def test_web_http_content_contains(self):
        check = WebService('asdf.com', 'http', WebCheck('', '<title>asdf</title>', WebService.CONTENT_CONTAINS))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('http://asdf.com/ contained check content', result.reason)

    def test_web_http_content_contains_fail(self):
        check = WebService('asdf.com', 'http', WebCheck('', 'keyword string to match', WebService.CONTENT_CONTAINS))
        result = check.execute()
        self.assertEqual(False, result.success)
        self.assertEqual("http://asdf.com/ did not contain 'keyword string to match'", result.reason)

    def test_web_http_server_down(self):
        check = WebService('8.8.8.8', 'http', WebCheck('', 200, WebService.STATUS))
        result = check.execute()
        self.assertEqual(check.connection_error(), result)

    def test_web_https(self):
        check = WebService('sparsa.org', 'https', WebCheck('', 200, WebService.STATUS))
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('https://sparsa.org/ returned 200 (should be 200)', result.reason)

    def test_web_https_manual_port(self):
        check = WebService('sparsa.org', 'https', WebCheck('', 200, WebService.STATUS), 443)
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('https://sparsa.org:443/ returned 200 (should be 200)', result.reason)

    def test_web_http_manual_port(self):
        check = WebService('sparsa.org', 'http', WebCheck('', 200, WebService.STATUS), 80)
        result = check.execute()
        self.assertEqual(True, result.success)
        self.assertEqual('http://sparsa.org:80/ returned 200 (should be 200)', result.reason)



if __name__ == '__main__':
    unittest.main()
