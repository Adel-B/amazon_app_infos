import unittest
import routes

class TestsApp(unittest.TestCase):

    def setUp(self):
        routes.app.config['TESTING'] = True
        self.app = routes.app.test_client()


    def test_post(self):
        #self.assertTrue()
        pass

    def test_get(self):
        print("\nRunning: test_get")
        resp = self.app.get('/home')
        assert 200 == resp.status_code
#        assert "About the Sample Application" in resp.data


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()