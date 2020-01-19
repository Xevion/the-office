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
    """represents a Episode with underlying Sections (representing a specific cutscene or area"""    
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    sections = db.relationship('Section', backref='episode', lazy='dynamic')

class Section(db.Model):
    """represents a Section of Quotes, a specific scene with relevant dialog"""
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    quotes = db.relationship('Quote', backref='section', lazy='dynamic')

class Quote(db.Model):
    """represents a specific quote by a specific speaker"""
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    speaker = db.Column(db.String(32))
    text = db.Column(db.String(512))