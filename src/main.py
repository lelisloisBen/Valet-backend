from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, sha256
from models import db, users
# from flask_jwt_simple import JWTManager, jwt_required, create_jwt
import os

SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
# app.config.from_object("config")
db.init_app(app)
CORS(app)
# app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
# jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Welcome Samir, Backend running...</h1><img src='https://cdn.pixabay.com/photo/2020/01/10/15/11/nude-4755496_1280.jpg' width='80%' /></div>"

@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    # user = users.query.filter_by(password=sha256(body['password'])).first()
    user = users.query.filter_by(password=body['password']).first()

    if not user:
        return 'User not found', 404

    return jsonify({
            #   'token': create_jwt(identity=1),
              'id': user.id,
              'appID': user.appID,
              'email': user.email,
              'firstname': user.firstname,
              'lastname': user.lastname,
              'birthdate': user.birthdate,
              'gender': user.gender,
              'address': user.address,
              'city': user.city,
              'state': user.state,
              'zipCode': user.zipCode,
              'phone': user.phone,
              'admin': user.admin
              })

@app.route('/register', methods=['POST'])
def handle_register():

    body = request.get_json()

    # if body is None:
    #     raise APIException("You need to specify the request body as a json object", status_code=400)
    # if 'firstname' not in body and 'lastname' not in body:
    #     raise APIException("You need to specify the first name and last name", status_code=400)
    # if 'password' not in body and 'email' not in body:
    #     raise APIException("You need to specify the password and email", status_code=400)
    # if 'firstname' not in body:
    #     raise APIException('You need to specify the first name', status_code=400)
    # if 'lastname' not in body:
    #     raise APIException('You need to specify the last name', status_code=400)
    # if 'password' not in body:
    #     raise APIException('You need to specify the password', status_code=400)
    # if 'email' not in body:
    #     raise APIException('You need to specify the email', status_code=400)

    db.session.add(users(
        appID = body['appID'],
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        password = sha256(body['password']),
        birthdate = body['birthdate'],
        gender = body['gender'],
        address = body['address'],
        city = body['city'],
        state = body['state'],
        zipCode = body['zipCode'],
        phone = body['phone'],
        admin = body['admin']
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'Successfully Registered'
    })



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)