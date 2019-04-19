import unittest
from flask_restful import Resource, Api
from flask_restful.utils import http_status_message
import rest
from flask import Flask


class TestApiMethods(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()
        self.app.testing = True

    def test_http_code(self):
        self.assertEqual(http_status_message(200), 'OK')
        self.assertEqual(http_status_message(201), 'Created')
        self.assertEqual(http_status_message(400), 'Bad Request')
        self.assertEqual(http_status_message(404), 'Not Found')

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
        pass


if __name__ == '__main__':
    unittest.main()
