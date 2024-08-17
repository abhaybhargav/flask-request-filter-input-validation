import re
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.security import generate_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class UserSchema(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    lastname = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=120))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates('password')
    def validate_password(self, value):
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character')

class UserSignup(Resource):
    def post(self):
        user_schema = UserSchema()
        try:
            data = user_schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {"error": "Email already registered"}, 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            age=data['age'],
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

api.add_resource(UserSignup, '/signup')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8880, debug=True)