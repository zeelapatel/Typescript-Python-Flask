from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, 'name': self.name, 'email': self.email}


# Create all tables when app is first run
db.create_all()


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'The server is running'})


# Create a user
@app.route('/api/flask/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }), 201
    except Exception as e:
        return make_response(jsonify({'message': 'error', 'error': str(e)}), 500)


@app.route('/api/flask/user', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error', 'error': str(e)}), 500)


@app.route('/api/flask/user/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'message': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error', 'error': str(e)}), 500)


@app.route('/api/flask/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error', 'error': str(e)}), 500)


@app.route('/api/flask/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error', 'error': str(e)}), 500)

