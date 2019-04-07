from flask_restful import Resource, reqparse
from models.doners import DonerModel

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
