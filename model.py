"""Models and database functions for Peers @ Park project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime



# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of parks_checkin website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name =%s email=%s>" % (self.user_id, self.
                                               self.email)


class Kid(db.Model):
    """Kid on parks_checkin website."""

    __tablename__ = "kids"

    kid_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    name = db.Column(db.String(30))
    date_of_birth = db.Column(db.DateTime) # change to date instead of datetime
    gender = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #Define one to many relationship to user (one user can have many kids but each kid is related to only one user)
    user = db.relationship('User', backref='user_kid')

    
    # get date_of birth of an object and returns their age
    def age(self):
        today = date.today()
        dob = self.date_of_birth.date()
        age = today.year-dob.year 
        #check if kid had bday already
        had_bday = (today.month,today.day)>(dob.month,dob.day)
        # if they haven't had their bday substract 1 to age
        if not had_bday:
            age-=1

        return age


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Kid Kid id=%s name=%s>" % (self.kid_id,
                                                 self.name)

class Checkin(db.Model):
    """Checking at a park by a user."""

    __tablename__ = "checkins" 

    checkin_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    checkin_date = db.Column(db.DateTime)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    park_id = db.Column(db.String(50))


    #Define one to many relationship to user (one user can have many checkins but each checkin is related to only one user)
    # user = db.relationship('User', backref='parks_checkin')
    user = db.relationship('User', backref=db.backref('parks_checkin'))



    def __repr__(self):
        """Provide helpful representation when printed."""
# ?????????????????????????Park ID integer need to change to %s? 
        s = "<Checkin checkin_id=%s checking_date=%s user_id=%s arrival_time=%s departure_time=%s> park_id=%s>"
        return s % (self.checkin_id, self.checkin_date, self.user_id,
                    self.arrival_time, self.departure_time, self.park_id)

class Kid_checkin(db.Model):
    """Checking a specific kid at the park by a user."""

    __tablename__ = "kid_checkin"

    kid_checkin_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('checkins.checkin_id'))
    kid_id = db.Column(db.Integer, db.ForeignKey('kids.kid_id'))


    # Define relationship to check. Every checkin can have many many kid's checkins but each kid checkin is related on one checkin
    #************************ADDDDDDDD order by
    checkin = db.relationship('Checkin', backref='kid_checkin')

    #Define one to many relationship to kid (one kid can have many checkins but each kid checkin is related to only one kid)
    kid = db.relationship('Kid', backref='kid_checkin')
    

    def __repr__(self):
        """Provide helpful representation when printed."""

# Park ID integer need to change to %s? 
        s = "<Kid checkin checkin_id=%s checking_id=%s kid_id=%s >"
        return s % (self.kid_checkin_id, self.checkin_id, self.kid_id)




#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///parks'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

 


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB :)"
    db.create_all()
