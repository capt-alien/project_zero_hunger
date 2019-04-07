from db import db


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
