import unittest
import rest
import json

bad_url = [
    'aaa',
    '12qwe',
    'as12',
    '12q21',
    'as10as',
    '#$%^&',
    '!@12as'
]
good_url = [
    '141',
    '0123',
    '1',
    '0001'
]


class TestUrlMethods(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()
        self.app.testing = True

    def test_get_bad_url(self):
        for _id in bad_url:
            response = self.app.get('user/'+_id)
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("INVALID INPUT", response_json["MESSAGE"])

    def test_post_bad_url(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        for _id in bad_url:
            response = self.app.post('/'+_id, data=json.dumps(u),
                                 content_type='application/json')
            self.assertEqual(response.status_code, 404)

    def test_put_bad_url(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        for _id in bad_url:
            response = self.app.put('user/'+_id,data=json.dumps(u),
                                 content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete_bad_url(self):
        for _id in bad_url:
            response = self.app.delete('user/'+_id)
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("INVALID INPUT", response_json["MESSAGE"])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
