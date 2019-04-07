from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


#resources liberaies to be removed when busted out

#mods
from db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required



#app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = 'alien'  # could do app.config['JWT_SECRET_KEY'] if we prefer
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

    def __init__(self, name, address):
        self.name = name
        self.address = address
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
    quantity = db.Column(db.Integer)
    # Forign keys
    # doner_id = db.Column(db.Integer, db.ForeignKey('doner.id'))
    # doner = db.relationship('DonerModel')

    def __init__(self, name, quantity, doner_id):
        self.name = name
        self.quantity = quantity
        self.doner_id = doner_id

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
    parser = reqparse.RequestParser()
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

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
        data = Doner.parser.parse_args()
        doner = DonerModel(name, **data)
        # print("test", doner['name'], doner['address'])
        # store in db
        try:
            doner.save_to_db()
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
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('doner_id',
                        type=int,
                        required=True,
                        help="Every item needs a doner_id."
                        )

    # @jwt_required  # No longer needs brackets
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    # @jwt_required
    def delete(self, name):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.quantity = data['quantity']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire item list.
        Otherwise we just return the item names.
        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
            }, 200



# ************************************************

#Routes
api.add_resource(Doner, '/doner/<string:name>')
api.add_resource(DonerList, '/')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
