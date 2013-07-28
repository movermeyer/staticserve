import threading
import unittest
from wsgiref.simple_server import make_server
from wsgiref.validate import validator

import requests

from static import StringMagic, Shock


def serve_requests():
    # Fire up static as a serve
    magics = [StringMagic(title="String Test"), ]
    app = Shock('testdata/pub', magics=magics)
    make_server('localhost', 9999, validator(app)).serve_forever()


def serve_one_request():
    # Start webserver in new thread
    t = threading.Thread(target=serve_requests)
    t.daemon = True
    t.start()


class TestMakeServer(unittest.TestCase):
    def setUp(self):
        serve_one_request()

    def test_serve_basic(self):
        r = requests.get("http://localhost:9999")
        self.assertEqual(r.status_code, 200)
        self.assertTrue("mixed content test" in str(r.content))

    
