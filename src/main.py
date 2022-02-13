from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, sha256, readTag
from models import db, users
import os
from werkzeug.utils import secure_filename 

UPLOAD_FOLDER = '/src/img'

app = Flask(__name__)
app.config.from_object("config")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)
CORS(app)

# create all the table first.
@app.before_first_request
def create_tables():
    db.create_all()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Welcome Samir, Backend running...</h1><img src='https://cdn.pixabay.com/photo/2020/01/10/15/11/nude-4755496_1280.jpg' width='80%' /></div>"

@app.route('/tag', methods=['POST'])
def handle_tagReader():

    if request.method == 'POST':
        file = request.files['image']
        # save file            
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img_path = file_path

        if file.filename == "":
            return jsonify({
                    'msg': 'error',
                    'mess': 'Please select a file'
                })
        else:
            myTag = readTag(img_path)
            return jsonify({
                'msg': 'success',
                'tag': myTag
            })

@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    user = users.query.filter_by(password=sha256(body['password'])).first()
    # if testing without sha256
    # user = users.query.filter_by(password=body['password']).first()

    if not user:
        return 'User not found', 404

    return jsonify({
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

@app.route('/signup', methods=['POST'])
def handle_signup():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)

    if 'firstname' not in body and 'lastname' not in body:
        raise APIException("You need to specify the first name and last name", status_code=400)
    if 'password' not in body and 'email' not in body:
        raise APIException("You need to specify the password and email", status_code=400)
    if 'firstname' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'lastname' not in body:
        raise APIException('You need to specify the last name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'appID' not in body:
        raise APIException('You need to specify the application ID', status_code=400)
    if 'birthdate' not in body:
        raise APIException('You need to specify the birth date', status_code=400)
    if 'gender' not in body:
        raise APIException('You need to specify the gender', status_code=400)
    if 'address' not in body:
        raise APIException('You need to specify the address', status_code=400)
    if 'city' not in body:
        raise APIException('You need to specify the city', status_code=400)
    if 'state' not in body:
        raise APIException('You need to specify the state', status_code=400)
    if 'zipCode' not in body:
        raise APIException('You need to specify the zipCode', status_code=400)
    if 'phone' not in body:
        raise APIException('You need to specify the phone', status_code=400)
    if 'admin' not in body:
        raise APIException('You need to specify the admin number', status_code=400)
    
    
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