from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(50), nullable = False)
    

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
    

class Favorite_characters(db.Model):
    favoriteId = db.Column(db.Integer, primary_key = True)    
    #characterId = db.Column(db.Integer) db.ForeignKey("Characters.Uid")
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship("User")

    def __repr__(self):
        return '<User %r>' % self.userId

    def serialize(self):
        return {
            "id": self.favoriteId,
            "User Id": self.userId,
            "Character": self.characterId
        }
    

class Favorite_planets(db.Model):
    favoriteId = db.Column(db.Integer, primary_key = True)    
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship("User")

    def __repr__(self):
        return '<User %r>' % self.userId

    def serialize(self):
        return {
            "id": self.favoriteId,
            "User Id": self.userId,
        }


class Characters(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200), unique = True)
    name = db.Column(db.String(50))
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorite_characters.favoriteId"))
    favorite = db.relationship("Favorite_characters")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "Url": self.url,
            "Character": self.name
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200), unique = True)
    name = db.Column(db.String(50))
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorite_planets.favoriteId"))
    favorite = db.relationship("Favorite_planets")

    def __repr__(self):
        return '<<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "Url": self.url,
            "Character": self.name
        }