import requests
import re

from bs4 import BeautifulSoup
from app import db, login

episodes = [5, 6, 22, 23, 14, 26, 24, 24, 24, 23] # Episode counts. Index 0 is for Webisodes.
quotePattern = r'([\w\s\.\',-\[\]\d&\"#]+):(.+)'

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episodes = db.relationship('Episode', backref='season', lazy='dynamic')

    def __init__(self, **kwargs):
        assert 0 <= kwargs.get('id') <= 9, "Season ID must be 0-9 inclusive"
        super(Season, self).__init__(**kwargs)

    def build(self, rebuild=False):
        """runs build operations on every Episode under this season"""
        print(f'Running build() on Season {self.id}')
        for episode in range(1, episodes[self.id - 1] + 1):
            ep = Episode.query.filter_by(season_id=self.id, number=episode).first()
            if ep is None:
                # Add the episode, then build
                print(f'Creating new Episode, Season {self.id}, Episode {episode}')
                ep = Episode(season_id=self.id, number=episode)
                db.session.add(ep)
                # I'm commiting early, which is a bit taboo, but I'm more worried about what the Episode object will need while building.
                db.session.commit()
                ep.build()
            else:
                print(f'Rebuilding Season {self.id}, Episode {episode}')
                if rebuild:
                    ep.build()
                pass
        
    @staticmethod
    def create_all(build=True):
        """creates new Season objects and runs build() on them"""
        for i in range(1, 10):
            if Season.query.get(i) is None:
                s = Season(id=i)
                db.session.add(s)
                if build: s.build()
        db.session.commit()
    
    @staticmethod
    def rebuild_all():
        """runs build() on all Season objects in database"""
        for season in Season.query.all():
            season.build(rebuild=True)

    @property
    def episodes(self): 
        """returns a List of Episodes under this Season"""
        return Episode.query.filter_by(season_id=self.id).all()

    @property
    def characters(self, sort):
        """returns a List of Characters under this Season, sorted by number of spoken lines"""
        pass

class Episode(db.Model):
    """represents a Episode with underlying Sections (representing a specific cutscene or area"""    
    id = db.Column(db.Integer, primary_key=True) # arbitrary ID, should NOT be relied on to determine episode number or correlating season
    number = db.Column(db.Integer) # episode number
    season_id = db.Column(db.Integer, db.ForeignKey('season.id')) # correlating season number
    built = db.Column(db.Boolean, default=False)
    sections = db.relationship('Section', backref='episode', lazy='dynamic') # sections of quotes under this episode

    def build(self):
        """downloads, processes, and automatically creates Sections and Quotes"""
        link = f'http://officequotes.net/no{self.season_id}-{str(self.number).zfill(2)}.php'
        data = requests.get(link).text
        open('test.html', 'w+', encoding='utf-8').write(data)
        soup = BeautifulSoup(data, 'html.parser')

        sections = soup.find_all(attrs={'class' : 'quote'}) 
        deleted = 0

        for section in sections:
            isNewpeat = False
            quotes = []
            for quote in section.find_all('b'):
                if 'Newpeat' in quote.string:
                    quote = quote.next_sibling
                    isNewpeat = True
                if quote is None or quote.next_sibling is None:
                    print('Quote is None or next sibling is None')
                    continue
                quotes.append(quote.string + quote.next_sibling.string)
            if len(quotes) == 0:
                print(f'Section found with Zero quotes. Newpeat: {isNewpeat}')
                continue
            isDeletedScene = quotes[0].lower().startswith('deleted scene')
            if isDeletedScene:
                deleted += 1
            s = Section(episode_id=self.id, deleted=deleted if isDeletedScene else -1, newpeat=isNewpeat)
            s.build(quotes[1:] if isDeletedScene else quotes)
            db.session.add(s)
        self.built = True
        db.session.commit()

    def rebuild(self):
        """functions that clears relevant sections from this Episode"""
        self.clear()
        self.build()

    def clear(self):
        """delete all sections relevant to this episode in order to reprocess"""
        sections = Section.query.filter_by(episode_id=self.id).all()
        print(f'Clearing {len(sections)} Sections of Ep {self.number} Season {self.season_id}')
        for section in sections:
            section.clear(commit=False, delete=True)
        self.built = False
        db.session.commit()

    @staticmethod
    def clear_all():
        """runs clear() on every episode in the database"""
        for episode in Episode.query.all():
            episode.clear()

    def __repr__(self):
        sections = len(Section.query.filter_by(episode_id=self.id).all())
        return f'Episode(id={self.id} s={self.season_id} ep={self.number} sects=[{sections}...])'

class Section(db.Model):
    """represents a Section of Quotes, a specific scene with relevant dialog"""
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))
    deleted = db.Column(db.Integer, default=-1)
    newpeat = db.Column(db.Boolean, default=False)
    quotes = db.relationship('Quote', backref='section', lazy='dynamic')

    def build(self, quotes, commit=False, reset=False):
        """given an List of unformatted script quotes, automatically creates Quotes assigned to this Section"""
        for i, quote in enumerate(quotes):
            if quote.lower().startswith('deleted scene'):
                raise Exception(f'Deleted Scene Quote passed to Section Builder: "{quote}"')
            # match = re.match(quotePattern, quote)
            # assert match != None, f"Quote '{quote}' could not be processed."
            # q = Quote(section=self, speaker=match[1].strip(), text=match[2].strip())
            mark = quote.find(':')
            q = Quote(section=self, speaker=quote[:mark], text=quote[mark + 1:], section_index=i)
            db.session.add(q)
        if commit: db.session.commit()
        
    def clear(self, doprint=True, commit=True, delete=False):
        """delete all quotes relevant to this section"""
        quotes = Quote.query.filter_by(section_id=self.id).all()
        if doprint: print(f'Clearing {len(quotes)} quotes from Section ID {self.id}')
        for quote in quotes:
            db.session.delete(quote)
        if delete: db.session.delete(self)
        if commit: db.session.commit()

    def __repr__(self):
        season = Episode.query.get(self.episode_id).id
        quotes = len(Quote.query.filter_by(section_id=self.id).all())
        return f'Section(id={self.id} S-EP={season}/{self.episode_id} quotes=[{quotes}...])'

class Quote(db.Model):
    """represents a specific quote by a specific speaker"""
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id')) # The section this quote belongs to.
    speaker = db.Column(db.String(32)) # The name of a character
    text = db.Column(db.String(512)) # The content of the Quote. Usually a sentence, sometimes more.
    section_index = db.Column(db.Integer) # The index of this quote in the section

    def __repr__(self):
        return f"Quote(speaker='{self.speaker}' text='{self.text[:50]}{'...' if len(self.text) > 51 else ''}')"