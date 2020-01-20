import requests
import re

from bs4 import BeautifulSoup
from app import db, login

episodes = [5, 6, 22, 23, 14, 26, 24, 24, 24, 23]
quotePattern = r'(\w+):.+'

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
        """downloads, processes, and automatically creates Sections and Quotes"""
        link = f'http://officequotes.net/no{self.season_id}-{str(self.episode).zfill(2)}.php'
        data = requests.get(link).text
        soup = BeautifulSoup(data, 'html.parser')

        sections = soup.find_all(attrs={'class' : 'quote'})
        for section in sections:
            quotes = []
            for quote in section.find_all("b"):
                quotes.append(quote.string + quote.next_sibling.string)
            deleted = quotes[0].startswith('Deleted Scene'):

    @property
    def scrapeURL(self):
        return f'http://officequotes.net/no{self.season_id}-{str(self.number).zfill(2)}.php'
    
class Section(db.Model):
    """represents a Section of Quotes, a specific scene with relevant dialog"""
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))
    deleted = db.Column(db.Boolean)
    quotes = db.relationship('Quote', backref='section', lazy='dynamic')

    def build(self, quotes, commit=False):
        """given an List of unformatted script quotes, automatically creates Quotes assigned to this Section"""
        for quote in quotes:
            if quote.lower().startswith('deleted scene'):
                raise Exception(f'Deleted Scene Quote passed to Section Builder: "{quote}"')
            match = re.match(quotePattern, quote)
            assert match != None, f"Quote '{quote}' could not be processed."
            q = Quote(section=self, speaker=match[1], text=match[2])
            db.session.add(q)
        if commit: db.session.commit()
        
class Quote(db.Model):
    """represents a specific quote by a specific speaker"""
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id')) # The section this quote belongs to.
    speaker = db.Column(db.String(32)) # The name of a character
    text = db.Column(db.String(512)) # The content of the Quote. Usually a sentence, sometimes more.
    section_index = db.Column(db.Integer) # The index of this quote in the section