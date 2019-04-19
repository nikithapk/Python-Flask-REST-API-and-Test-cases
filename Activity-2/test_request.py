import unittest
import json
import rest
import sqlite3


class TestRequestMethods(unittest.TestCase):
    def setUp(self):
        rest.con = sqlite3.connect(":memory:", check_same_thread=False)
        rest.cursor = rest.con.cursor()
        rest.cursor.execute("DROP TABLE IF EXISTS user")
        rest.cursor.execute(
            "CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL)")
        self.app = rest.app.test_client()
        self.app.testing = True

    def test_get_request(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        response = self.app.post('/user',
                                 data=json.dumps(u),
                                 content_type='application/json')
        post_response = json.loads(response.data.decode())
        posted_id = post_response['YOUR ID']
        response = self.app.get('/user/' + posted_id)
        response_json = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'NewUser' in response_json['username']

    def test_post_request(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        response = self.app.post('/user',
                                 data=json.dumps(u),
                                 content_type='application/json')
        post_response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

    def test_put_request(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        response = self.app.post('/user',
                                 data=json.dumps(u),
                                 content_type='application/json')
        post_response = json.loads(response.data.decode())
        posted_id = post_response['YOUR ID']
        response = self.app.put('/user/' + posted_id,
                                data=json.dumps(u),
                                content_type='application/json')
        put_response_json = json.loads(response.data.decode())
        self.assertEqual(put_response_json['MESSAGE'], 'UPDATED SUCCESSFULLY')
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        response = self.app.post('/user',
                                 data=json.dumps(u),
                                 content_type='application/json')
        post_response = json.loads(response.data.decode())
        posted_id = post_response["YOUR ID"]
        response = self.app.delete('/user/' + posted_id)
        delete_response_json = json.loads(response.data.decode())
        self.assertEqual(delete_response_json["MESSAGE"], 'DELETED SUCCESSFULLY')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        rest.con.close()


if __name__ == '__main__':
        unittest.main()