import unittest
from flask_restful import Resource, Api
from flask_restful.utils import http_status_message
from copy import deepcopy
import json
import rest
from flask import Flask

bad_url = [
    'aaa',
    '12qwe',
    'as12',
    '12q21',
    'as10as'
    '#$%^&'
    '!@12as'
]
good_url = [
    '141',
    '0123',
    '1',
    '0001'
]
missing_input = [
    {
     'name': 'NewUser'
    },
    {
     'email':'abcdef@gmail.com'
    },
    {
     'name': 'NewUser',
     'name': 'newuser'
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
found_id =[
    '101',
    '201',
    '301',
    '401',
    '501',
    '601',
    '701',
    '801'
]
already_exist_email =[
    'john@gmail.com',
    'ranjitha@gmail.com',
    'nik@gmail.com',
    'div@gmail.com',
    'vin@gmail.com',
    'suman@gmail.com',
    'sristi@gmail.com',
    'kirti@gmail.com'
]


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.backup_items = deepcopy(rest.userDB)
        self.app = rest.app.test_client()
        self.app.testing = True

    def test_http_code(self):
        self.assertEqual(http_status_message(200), 'OK')
        self.assertEqual(http_status_message(201), 'Created')
        self.assertEqual(http_status_message(400), 'Bad Request')
        self.assertEqual(http_status_message(404), 'Not Found')

    def test_get_bad_url(self):
        for _id in bad_url:
            response = self.app.get('user/'+_id)
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("INVALID INPUT", response_json["MESSAGE"])

    def test_post_bad_url(self):
        for _id in bad_url:
            response = self.app.post('/'+_id)
            self.assertEqual(response.status_code, 404)

    def test_put_bad_url(self):
        for _id in bad_url:
            response = self.app.put('user/'+_id)
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("INVALID INPUT", response_json["MESSAGE"])

    def test_delete_bad_url(self):
        for _id in bad_url:
            response = self.app.delete('user/'+_id)
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("INVALID INPUT", response_json["MESSAGE"])

    def test_get_request(self):
        response = self.app.post('/user',
                                 data=json.dumps(dict(
                                     username="NewUser",
                                     email="newuser@gmail.com"
                                 )),
                                 content_type='application/json')
        post_response = json.loads(response.data.decode())
        posted_id = post_response["YOUR ID"]
        response = self.app.get('/user/' + posted_id)
        response_json = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'NewUser' in response_json["username"]

    def test_post_request(self):
        response = self.app.post('/user',
                                 data=json.dumps(dict(
                                     username="NewUser",
                                     email="newuser@gmail.com"
                                 )),
                                 content_type='application/json')
        post_response_json = json.loads(response.data.decode())
        self.assertEqual(post_response_json["MESSAGE"],'CREATED SUCCESSFULLY')
        self.assertEqual(response.status_code, 201)

    def test_put_request(self):
        response = self.app.put('/user/101',
                                data=json.dumps(dict(
                                     username="NewUser",
                                     email="newuser@gmail.com"
                                 )),
                                content_type='application/json')
        put_response_json = json.loads(response.data.decode())
        self.assertEqual(put_response_json["MESSAGE"],'UPDATED SUCCESSFULLY')
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        response = self.app.delete('/user/801')
        delete_response_json = json.loads(response.data.decode())
        self.assertEqual(delete_response_json["MESSAGE"],'DELETED SUCCESSFULLY')
        self.assertEqual(response.status_code, 200)

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
                                    content_type=con_type)
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
            self.assertNotIn(_id, [user["_id"] for user in rest.userDB])
            self.assertEqual(response.status_code, 404)

    def test_found_record(self):
        for _id in found_id:
            response = self.app.get('/user/' + _id)
            self.assertIn(_id, [user["_id"] for user in rest.userDB])
            self.assertEqual(response.status_code, 200)

    def test_email_already_exist(self):
        for email in already_exist_email:
            response = self.app.post('/user',
                                     data=json.dumps(dict(
                                         username="NewUser",
                                         email=email
                                     )),
                                     content_type='application/json')
            self.assertIn(email, [user["email"] for user in rest.userDB])
            self.assertEqual(response.status_code,400)

    def test_endpoints(self):
        app = Flask(__name__)
        api = Api(app)

        class User(Resource):
            def get(self):
                pass
        api.add_resource(User, '/user/<string:_id>', endpoint="user")
        with app.test_request_context('/user'):
            self.assertFalse(api._has_fr_route())

        with app.test_request_context('/user/3'):
            self.assertTrue(api._has_fr_route())

    def test_url(self):
        app = Flask(__name__)
        api = Api(app)

        class User(Resource):
            def get(self):
                pass
        api.add_resource(User, '/user/<string:_id>')
        with app.test_request_context('/user'):
            self.assertEqual(api.url_for(User, _id=123), '/user/123')

    def test_add_two_conflicting_resources_on_same_endpoint(self):
        app = Flask(__name__)
        api = Api(app)

        class User(Resource):
            def get(self):
                return 'true'

        class Users(Resource):
            def get(self):
                return 'true'

        api.add_resource(User, '/user', endpoint='user')
        self.assertRaises(ValueError, api.add_resource, Users, '/user/<string:_id>', endpoint='user')

    def test_add_the_same_resource_on_different_endpoint(self):
        app = Flask(__name__)
        api = Api(app)

        class User(Resource):
            def get(self):
                return 'true'
        api.add_resource(User, '/user', endpoint='create_user')
        api.add_resource(User, '/user/_id', endpoint='user')
        with app.test_client() as client:
            response = client.get('/user')
            self.assertEqual(response.status_code, 200)
            response = client.get('/user/_id')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        rest.userDB = self.backup_items


if __name__ == '__main__':
    unittest.main()
