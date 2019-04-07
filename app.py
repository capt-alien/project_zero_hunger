from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


#resources liberaies to be removed when busted out

#mods
from db import db
from flask_restful import Resource, reqparse


#app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
# app.secret_key = 'alien'  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


# ************************************************

#Doner model
class DonerModel(db.Model):
    __tablename__ = 'doners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(300), nullable = False)
    # email = db.Column(db.String(120), unique=True, nullable=False)

#nested resources
    # items = db.relationship(ItemModel, lazy='dynamic')
    def __init__(self, name):
        self.name = name
        # self.address = address
        # self.email = email


    def json(self):
        return {
        'id': self.id,
        'name': self.name,
        'address': self.address
        # 'email': self.email
        # 'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# ************************************************

# item model
class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.column(db.Intiger, required=True)
    # Forign keys
    doner_id = db.Column(db.Integer, db.ForeignKey('doner.id'))
    doner = db.relationship('DonerModel')

    def json(self):
        return {
            'id': self.id,
            'name':self.name,
            'quantity': self.quantity,
            'doner_id': self.doner_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# *************************************

# Doner Resource
class Doner(Resource):
    def get(self, name):
        doner = DonerModel.find_by_name(name)
        if doner:
            return doner.json()
        return{'message':'Doner not found'}, 404


    def post(self, name):
        # Check to see if doner is in DB
        if DonerModel.find_by_name(name):
            return {'message': "a Doner with name '{}'' already exists.".format(name)}, 400
            # if not instantiate it
        doner = DonerModel(name)
        print("test", doner)
        # store in db
        try:
            doner.save_to_db()
            print("test:  saved to DB")
        except:
            return {"message": "An error occurred creting the doner."}, 500
        return doner.json(), 201


    def delete(self, name):
        doner = DonerModel.find_by_name(name)
        if doner:
            doner.delete_from_db()

        return {'message': "Doner deleted"}

class DonerList(Resource):
    def get(self):
        return {'doners': [x.json() for x in DonerModel.find_all()]}

# ************************************************
# item Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."





# ************************************************

#Routes
api.add_resource(Doner, '/doner/<string:name>')
api.add_resource(DonerList, '/')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
