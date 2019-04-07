from db import db

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
