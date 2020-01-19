from app import db, login

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Season, self).__init__(**kwargs)


    @property
    def episodes(self):
        """returns a List of Episodes under this Season"""
        pass

    @property
    def characters(self, sort):
        """returns a List of Characters under this Season, sorted by number of spoken lines"""
        pass

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quotes = db.relationship('Quote', backref='section', lazy='dynamic')

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    speaker = db.Column(db.String(32))
    text = db.Column(db.String(512))