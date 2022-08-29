#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from app import app, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(255))
    # Defining relationship
    shows = db.relationship('Show', backref='venues', lazy=True)

    def __repr__(self) -> str:
      return f'<Venue:: ID: {self.id}, name: {self.name}\
        , city: {self.city}, state: {self.state}, address: {self.address},\
          genres: {self.genres}, seeking talent: {self.seeking_talent}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(255))

    def __repr__(self) -> str:
      return f'<Artist:: ID: {self.id}, name: {self.name}\
        , city: {self.city}, state: {self.state}, genres: {self.genres},\
          seeking talent: {self.seeking_venue}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__='show'
  
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  # Defining relationship
  artists = db.relationship('Artist', backref='shows')

  def __repr__(self) -> str:
      return f'<Show:: ID: {self.id}, venue ID: {self.venue_id}, Artist ID: {self.artist_id}, Start time: {self.start_time}>'

