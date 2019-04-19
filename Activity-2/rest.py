from flask import Flask, request, Blueprint
from flask_restful import Resource, Api
import re
import logging
import sqlite3

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
logging.basicConfig(filename='info.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

con = sqlite3.connect(":memory:", check_same_thread=False)
cursor = con.cursor()
cursor.execute("DROP TABLE IF EXISTS user")
cursor.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL)")


class Store:
    def show(self, _id):
        query = cursor.execute("SELECT * FROM user WHERE id=?", [int(_id), ])
        row = query.fetchone()
        if row:
            return {'id': str(row[0]), 'username': row[1], 'email': row[2]}, 200
        else:
            logging.debug('USER NOT FOUND')
            return {'MESSAGE-1': 'USER NOT FOUND'}, 404

    def add(self, username, email):
        query = cursor.execute("SELECT * FROM user WHERE email=?", [email, ])
        row = query.fetchone()
        if row:
            logging.info('User already exits')
            return {'MESSAGE': 'EMAIL ALREADY EXISTS'}, 400
        else:
            cursor.execute("INSERT INTO user(username, email) VALUES(?,?)", [username, email])
            query = cursor.execute("select last_insert_rowid()")
            row = query.fetchone()
            con.commit()
            logging.info('CREATED SUCCESSFULLY')
            return {'MESSAGE': 'CREATED SUCCESSFULLY', 'YOUR ID': str(row[0])}, 201

    def update(self, _id, username, email):
        query = cursor.execute("SELECT * FROM user WHERE id=?", [int(_id), ])
        row = query.fetchone()
        if row:
            cursor.execute("UPDATE user SET username = '" + str(username) + "',email = '" + str(
                email) + "' WHERE id = %d" % int(_id))

            logging.info('UPDATED SUCCESSFULLY')
            return {'MESSAGE': 'UPDATED SUCCESSFULLY'}, 200
        else:
            logging.debug('USER NOT FOUND')
            return {'MESSAGE': 'USER NOT FOUND'}, 404

    def remove(self, _id):
        query = cursor.execute("SELECT * FROM user WHERE id=?", [int(_id), ])
        row = query.fetchone()
        if row:
            cursor.execute("DELETE FROM user WHERE id = %d" % int(_id))
            logging.info('DELETED SUCCESSFULLY')
            return {'MESSAGE': 'DELETED SUCCESSFULLY'}, 200
        else:
            logging.debug('USER NOT FOUND')
            return {'MESSAGE': 'USER NOT FOUND'}, 404


class Validate:
    def _validate_email(self, email):
        self.match = re.search('^[_A-Za-z0-9-]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,4})$', email)
        if self.match:
            return True
        else:
            return False

    def _validate_username(self, username):
        self.match = re.search('^[a-zA-Z]+[0-9]*([ _-]{0,1}|[a-zA-Z0-9]*)$', username)
        if self.match:
            return True
        else:
            return False

    def _validate_id(self, _id):
        self.t = True
        self.f = False
        if _id.isdigit():
            return self.t
        else:
            return self.f


class Users(Resource, Validate, Store):
    def post(self):
        try:
            usr = request.get_json()
            username = str(usr['username'])
            email = str(usr['email'])
            if self._validate_username(username)is True and self._validate_email(email) is True:
                return self.add(username, email)
            else:
                logging.warning('INVALID INPUT')
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except KeyError as e:
            logging.exception(str(e))
            return {'MESSAGE': 'Exception caught: KeyError,expected '+str(e)}, 400
        except Exception as e:
            logging.exception(str(e))
            return {'MESSAGE': str(e)}, 400

    def get(self, _id):
        try:
            if self._validate_id(_id):
                return self.show(_id)
            else:
                logging.warning('INVALID INPUT')
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except Exception as e:
            logging.exception(str(e))
            return {'MESSAGE': str(e)}, 400

    def put(self, _id):
        try:
            usr = request.get_json()
            updated_name = usr['username']
            updated_email = usr['email']
            if self._validate_id(_id) and self._validate_username(updated_name) and self._validate_email(updated_email):
                return self.update(str(_id), updated_name, updated_email)
            else:
                logging.warning('INVALID INPUT')
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except KeyError as e:
            logging.exception(str(e))
            return {'MESSAGE': 'Exception caught: KeyError,expected ' + str(e)}, 400
        except Exception as e:
            logging.exception(str(e))
            return {'MESSAGE': str(e)}, 400

    def delete(self, _id):
        try:
            if self._validate_id(_id):
                return self.remove(_id)
            else:
                logging.warning('INVALID INPUT')
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except Exception as e:
            logging.exception(str(e))
            return {'MESSAGE': str(e)}, 400


api.add_resource(Users, '/user', methods=['POST'], endpoint='create_user')
api.add_resource(Users, '/user/<string:_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='user')
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=5002, debug=True)

