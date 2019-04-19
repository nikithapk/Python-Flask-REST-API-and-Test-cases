import unittest
import json
import rest
import sqlite3

good_url = [
    '141',
    '0123',
    '1',
    '0001'
]
missing_input = [
    {
     'username': 'NewUser'
    },
    {
     'email':'abcdef@gmail.com'
    },
    {
     'username': 'NewUser',
     'username': 'newuser'
    },
    {
     'email':'abcdef@gmail.com',
     'email':'wxyz@gmail.com'
    }
]
wrong_content_type = [
    'None',
    'application/atom+xml',
    'application/ecmascript',
    'application/javascript',
    'application/octet-stream',
    'application/ogg',
    'application/pdf',
    'application/postscript',
    'application/rdf+xml',
    'application/soap+xml',
    'application/font-woff',
    'application/x-yaml',
    'application/xhtml+xml',
    'application/xml',
    'application/xml-dtd',
    'application/xop+xml',
    'application/zip',
    'application/gzip',
    'application/graphql',
    'application/x-www-form-urlencoded',
    'audio/basic',
    'audio/L24',
    'audio/mp4',
    'audio/mpeg',
    'audio/ogg',
    'audio/vorbis',
    'audio/vnd.rn-realaudio',
    'audio/vnd.wave',
    'audio/webm',
    'image/gif',
    'image/jpeg',
    'image/pjeg',
    'image/gif',
    'image/png',
    'image/tiff',
    'image/svg+xml',
    'message/http',
    'message/imdn+xml',
    'message/partial',
    'message/rfc822',
    'multipart/mixed',
    'multipart/alternative',
    'multipart/related',
    'multipart/form-data',
    'multipart/signed',
    'multipart/encrypted',
    'text/plain',
    'text/vcard'
]

invalid_username =[
    'Niki tha',
    '!@#nikitha',
    '!@#@#',
    '____',
    '----',
    '34435',
    'nik__tha',
    'nik--tha'
]
invalid_email=[
    'nikitha122com',
    'nikitha.gmail',
    'nikitha@com.gmail',
    '123##.in',
    'com.gmail@nikitha',
]
not_found_id = [
    '123',
    '21',
    '456',
    '000'
]


class TestInputMethods(unittest.TestCase):
    def setUp(self):
        rest.con = sqlite3.connect(":memory:", check_same_thread=False)
        rest.cursor = rest.con.cursor()
        rest.cursor.execute("DROP TABLE IF EXISTS user")
        rest.cursor.execute(
            "CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL)")
        self.app = rest.app.test_client()
        self.app.testing = True

    def test_post_missing_input(self):
        for item in missing_input:
            response = self.app.post('/user',
                                     data=json.dumps(item),
                                     content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_put_missing_input(self):
        for item in missing_input:
            for id in good_url:
                response = self.app.put('/user/'+id,
                                        data=json.dumps(item),
                                        content_type='application/json')
                self.assertEqual(response.status_code, 400)

    def test_post_wrong_content_type(self):
        for con_type in wrong_content_type:
            response = self.app.post('/user',
                                     data=json.dumps(dict(
                                         username="NewUser",
                                         email="newuser@gmail.com"
                                     )),
                                    content_type = con_type)
            self.assertEqual(response.status_code, 400)

    def test_put_wrong_content_type(self):
        for con_type in wrong_content_type:
            for _id in good_url:
                response = self.app.put('/user/'+_id,
                                        data=json.dumps(dict(
                                         username="NewUser",
                                         email="newuser@gmail.com"
                                        )),
                                        content_type=con_type)
                self.assertEqual(response.status_code, 400)

    def test_post_invalidUsername(self):
        for name in invalid_username:
            response = self.app.post('/user',
                                     data=json.dumps(dict(
                                         username=name,
                                         email="newuser@gmail.com"
                                     )),
                                     content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_put_invalidUsername(self):
        for name in invalid_username:
            for _id in good_url:
                response = self.app.put('/user/'+_id,
                                        data=json.dumps(dict(
                                         username=name,
                                         email="newuser@gmail.com"
                                        )),
                                        content_type='application/json')
                self.assertEqual(response.status_code, 400)

    def test_post_invalidEmail(self):
        for email in invalid_email:
            response = self.app.post('/user',
                                     data=json.dumps(dict(
                                         username="NewUser",
                                         email=email
                                     )),
                                     content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_put_invalidEmail(self):
        for email in invalid_email:
            for _id in good_url:
                response = self.app.put('/user/'+_id,
                                        data=json.dumps(dict(
                                            username="NewUser",
                                            email=email
                                        )),
                                        content_type='application/json')
                self.assertEqual(response.status_code, 400)

    def test_not_found_record(self):
        for _id in not_found_id:
            response = self.app.get('/user/' + _id)
            query = rest.cursor.execute("SELECT * FROM user WHERE id=?", [int(_id), ])
            row = query.fetchone()
            self.assertEqual(response.status_code, 404)

    def test_found_record(self):
        u = {"username": "NewUser", "email": "newuser@gmail.com"}
        response = self.app.post('/user',
                                 data=json.dumps(u),
                                 content_type='application/json')
        post_response = json.loads(response.data.decode())
        posted_id = str(post_response["YOUR ID"])
        response = self.app.get('/user/' + posted_id)
        query = rest.cursor.execute("SELECT * FROM user WHERE id=?", [int(posted_id), ])
        row = query.fetchone()
        self.assertIn(posted_id, str(row[0]))
        self.assertEqual(response.status_code, 200)

    def test_email_already_exist(self):
        email = "newuser@gmail.com"
        response1 = self.app.post('/user',
                                 data=json.dumps(dict(
                                     username="NewUser",
                                     email=email
                                 )),
                                 content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/user',
                                data=json.dumps(dict(
                                        username="NewUser",
                                        email=email
                                )),
                                content_type='application/json')
        query = rest.cursor.execute("SELECT * FROM user WHERE email=?", [email, ])
        row = query.fetchone()
        self.assertTrue
        self.assertEqual(response2.status_code, 400)

    def tearDown(self):
        rest.con.close()


if __name__ == '__main__':
        unittest.main()