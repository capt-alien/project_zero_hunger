from flask_restful import Resource, reqparse
from models.organizations import OrgModel

# Doner Resource
class Organization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        organization = OrgModel.find_by_name(name)
        if organization:
            return organization.json()
        return{'message':'Org not found'}, 404


    def post(self, name):
        # Check to see if doner is in DB
        if OrgModel.find_by_name(name):
            return {'message': "a organization with name '{}'' already exists.".format(name)}, 400
            # if not instantiate it
        data = Organization.parser.parse_args()
        organization = OrgModel(name, **data)
        try:
            organization.save_to_db()
        except:
            return {"message": "An error occurred creting the organization."}, 500
        return organization.json(), 201


    def delete(self, name):
        organization = OrgModel.find_by_name(name)
        if organization:
            organization.delete_from_db()

        return {'message': "organization deleted"}

class OrgList(Resource):
    def get(self):
        return {'Organizations': [x.json() for x in OrgModel.find_all()]}
