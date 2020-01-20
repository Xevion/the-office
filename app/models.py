import re

from app import db, login

episodes = [5, 6, 22, 23, 14, 26, 24, 24, 24, 23]

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episodes = db.relationship('Episode', backref='season', lazy='dynamic')

    def __init__(self, **kwargs):
        assert 0 >= kwargs.get('id') <= 9, "Season ID must be 0-9 inclusive"
        super(Season, self).__init__(**kwargs)

    def build(self):
        """runs build operations on every Episode under this season"""
        for episode in range(1, episodes[self.id - 1] + 1):
            ep = Episode.query.filter_by(season=self, number=episode).first()
            if ep is None:
                # Add the episode, then build
                print(f'Creating new Episode, Season {self.id}, Episode {episode}')
                ep = Episode(season=self, number=episode)
                db.session.add(ep)
                # I'm commiting early, which is a bit taboo, but I'm more worried about what the Episode object will need while building.
                db.session.commit()
            else:
                # Regardless of whether it existended before hand, the episode will be built.
                pass
            ep.build()

    @property
    def episodes(self):
        """returns a List of Episodes under this Season"""
        return Episode.query.filter_by(season=self).all()

    @property
    def characters(self, sort):
        """returns a List of Characters under this Season, sorted by number of spoken lines"""
        pass

class Episode(db.Model):
    """represents a Episode with underlying Sections (representing a specific cutscene or area"""    
    id = db.Column(db.Integer, primary_key=True) # arbitrary ID, should NOT be relied on to determine episode number or correlating season
    number = db.Column(db.Integer) # episode number
    season_id = db.Column(db.Integer, db.ForeignKey('season.id')) # correlating season number
    sections = db.relationship('Section', backref='episode', lazy='dynamic') # sections of quotes under this episode

    def build(self):
        """Downloads, processes, and automatically creates Sections and Quotes"""

    @property
    def scrapeURL(self):
        return f'http://officequotes.net/no{self.season_id}-{str(self.number).zfill(2)}.php'
    
class Section(db.Model):
    """represents a Section of Quotes, a specific scene with relevant dialog"""
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))
    quotes = db.relationship('Quote', backref='section', lazy='dynamic')

    def build(self, quotes):
        """given an List of unformatted script quotes, automatically creates Quotes"""
        for quote in quotes:
            match = re.match(r'()')
            assert match != None, "Quote '{}' could not be processed.".format(quote)

class Quote(db.Model):
    """represents a specific quote by a specific speaker"""
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    speaker = db.Column(db.String(32))
    text = db.Column(db.String(512))