from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
    
user_args =  reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="name of the user is required")
user_args.add_argument("email", type=str, required=True, help="email of the user is required")

userfields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userfields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userfields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'],email=args['email'])
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.all()
        return user,201
    
class User(Resource):        
    @marshal_with(userfields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Could not find the user with that id")
        return user
    
    @marshal_with(userfields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Could not find the user with that id")
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user
    
    @marshal_with(userfields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Could not find the user with that id")
        db.session.delete(user)
        db.session.commit()
        return user
     

    
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/users/<id>")

@app.route('/')
def home():
    return "<h1>HelloFlask!!!</h1>"

if  __name__ == "__main__":
    app.run(debug=True)
