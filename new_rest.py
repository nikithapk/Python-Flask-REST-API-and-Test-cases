from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import re

app = Flask(__name__)
api = Api(app)


class Validate:
    def _validate_email(self, email):
        match = re.search('^[_A-Za-z0-9-]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,4})$', email)
        if match:
            return True
        else:
            return False

    def _validate_username(self, username):
        match = re.search('^[A-Za-z0-9_-]{3,20}$', username)
        if match:
            return True
        else:
            return False

    def _validate_id(self, id):
        if id.isdigit():
            return True
        else:
            return False


class Users(Resource, Validate):
    def get(self, id):
        try:
            conn = sqlite3.connect('curd.db')
            cursor = conn.cursor()
            if self._validate_id(id):
                query = cursor.execute("SELECT * FROM user WHERE id=?", [int(id), ])
                row = query.fetchone()
                if row:
                    return {'id': row[0], 'username': row[1], 'email': row[2]},200
                else:
                    return {'MESSAGE': 'USER NOT FOUND'}, 404
            else:
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except:
            return {'MESSAGE': 'INVALID INPUT'}, 400
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    def post(self):
        try:
            conn = sqlite3.connect('curd.db')
            cursor = conn.cursor()
            usr = request.get_json()
            username = usr['username']
            email = usr['email']
            if self._validate_username(username)is True and self._validate_email(email) is True:
                query = cursor.execute("SELECT * FROM user WHERE email=?", [email, ])
                row = query.fetchone()
                if row:
                    return {'MESSAGE': 'EMAIL ALREADY EXISTS'}, 400

                else:
                    cursor.execute("INSERT INTO user(username, email) VALUES(?,?)", [username, email])
                    query = cursor.execute("select last_insert_rowid()")
                    row = query.fetchone()
                    return {'response': 'CREATED SUCCESSFULLY','YOUR ID':row[0]},201
            else:
                 return {'MESSAGE': 'INVALID INPUT'}, 400
        except:
            return {'MESSAGE-1': 'Add KEY:CONTENT TYPE , VALUE:APLLICATION/JSON in header','MESSAGE-2':'CHECK THE INPUT'}, 400
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    def put(self, id):
        try:
            conn = sqlite3.connect('curd.db')
            cursor = conn.cursor()
            usr = request.get_json()
            updated_name = usr['username']
            updated_email = usr['email']
            if self._validate_id(id) and self._validate_username(updated_name) and self._validate_email(updated_email):
                query = cursor.execute("SELECT * FROM user WHERE id=?", [int(id), ])
                row = query.fetchone()
                if row:
                    cursor.execute("UPDATE user SET username = '" + str(updated_name) + "',email = '" + str(updated_email) + "' WHERE id = %d" % int(id))
                    return {'response': 'UPDATED SUCCESSFULLY'},200
                else:
                    return {'MESSAGE': 'USER NOT FOUND'}, 404
            else:
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except:
            return {'MESSAGE': 'INVALID INPUT'}, 400
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    def delete(self, id):
        try:
            conn = sqlite3.connect('curd.db')
            cursor = conn.cursor()
            if self._validate_id(id):
                query = cursor.execute("SELECT * FROM user WHERE id=?", [int(id), ])
                row = query.fetchone()
                if row:
                    conn.execute("DELETE FROM user WHERE id = %d" % int(id))
                    return {'response': 'DELETED SUCCESSFULLY'},200
                else:
                    return {'MESSAGE': 'USER NOT FOUND'}, 404
            else:
                return {'MESSAGE': 'INVALID INPUT'}, 400
        except:
            return {'MESSAGE': 'INVALID INPUT'}, 400
            conn.rollback()
        finally:
            conn.commit()
            conn.close()


api.add_resource(Users,'/user',methods=['POST'],endpoint='create_user')
api.add_resource(Users,'/user/<string:id>',methods=['GET','PUT','DELETE'],endpoint='user')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
