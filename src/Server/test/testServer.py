import unittest
import sys
sys.path.append('../src')
import Server

#To run test cases please provide valid certificate and key to test locations
class test_Server(unittest.TestCase):

    def test_serverInitialization(self):
        server = Server.Server('localhost',8083,'key.pem','certificate.pem')

        self.assertEqual(server.host,'localhost')
        self.assertEqual(server.port,8083)
        self.assertEqual(server.keyfile,'key.pem')
        self.assertEqual(server.certfile,'certificate.pem')
        self.assertEqual(server.is_running,False)

