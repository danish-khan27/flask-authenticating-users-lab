from flask import Flask, request, session, jsonify, make_response
from flask_migrate import Migrate
from models import db, User, UserSchema

app = Flask(__name__)
app.secret_key = b'some-secret-key'   # keep this consistent
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    session['user_id'] = user.id
    return jsonify(UserSchema().dump(user)), 200


# ---------- LOGOUT ----------
@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return '', 204


# ---------- CHECK SESSION ----------
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')

    if not user_id:
        return '', 401

    user = User.query.get(user_id)
    if not user:
        return '', 401

    return jsonify(UserSchema().dump(user)), 200


if __name__ == '__main__':
    app.run(port=5555)
