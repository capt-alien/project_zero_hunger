from flask_restful import Resource, reqparse
from models.doners import DonerModel

# Doner Resource
class Organization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        organization = DonerModel.find_by_name(name)
        if organization:
            return organization.json()
        return{'message':'Doner not found'}, 404


    def post(self, name):
        # Check to see if doner is in DB
        if OrganizationModel.find_by_name(name):
            return {'message': "a Doner with name '{}'' already exists.".format(name)}, 400
            # if not instantiate it
        data = Organization.parser.parse_args()
        organization = OrganizationModel(name, **data)
        try:
            organization.save_to_db()
        except:
            return {"message": "An error occurred creting the doner."}, 500
        return organization.json(), 201


    def delete(self, name):
        organization = OrganizationModel.find_by_name(name)
        if organization:
            organization.delete_from_db()

        return {'message': "Doner deleted"}

class OrganizationList(Resource):
    def get(self):
        return {'Organizations': [x.json() for x in OrganizationModel.find_all()]}
