from db import # DEBUG:

# ************** USER MODEL****************
class UserModel(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Intiger, primary_key=True)
    username = db.Column(db.string(80))
    email = db.Column(db.string(80))
    password = db.Column(db.String(80))
    # Forign keys
    # doner_id = db.Column(db.Integer, db.ForeignKey('doner.id'))
    # doner = db.relationship('DonerModel')
    # org_id = db.Column(db.Integer, db.ForeignKey('org.id'))
    # org = db.relationship('OrgModel')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return{
            'id':self.id,
            'username': self.username,
            'email': self.email
                }

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()

        def delete_from_db(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def find_by_username(cls, username):
            return cls.query.filter_by(username=username).first()

        @classmethod
        def find_by_email(cls, email):
            return cls.query.filter_by(email=email).first()

        @classmethod
        def find_by_id(cls, _id):
            return cls.query.filter_by(id=id).first()
