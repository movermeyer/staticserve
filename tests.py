import random
import threading
from time import sleep
import unittest
from wsgiref.simple_server import make_server
from wsgiref.validate import validator

import requests

from static import StringMagic, Shock


def serve_requests(port):
    # Fire up static as a serve
    magics = [StringMagic(title="String Test"), ]
    app = Shock('testdata/pub', magics=magics)
    make_server('localhost', port, validator(app)).serve_forever()


def serve_one_request(count):
    # Start webserver in new thread
    t = threading.Thread(target=serve_requests, args=[count])
    t.daemon = True
    t.start()


class TestMakeServer(unittest.TestCase):

    def test_serve_basic(self):
        port = random.randrange(10000, 65535)
        serve_one_request(port)
        sleep(1)
        r = requests.get("http://localhost:{0}".format(port))
        self.assertEqual(r.status_code, 200)
        self.assertTrue("mixed content test" in str(r.content))

    def test_serve_image(self):
        port = random.randrange(10000, 65535)
        serve_one_request(port)
        sleep(1)
        r = requests.get("http://localhost:{0}/682px-Oscypki.jpg".format(port))
        self.assertEqual(r.status_code, 200)
        with open("testdata/pub/682px-Oscypki.jpg", "rb") as f:
            image = f.read()
        self.assertEqual(len(r.content), len(image))

