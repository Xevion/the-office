import requests
import json
import os

from bs4 import BeautifulSoup
from app import db, login

episodes = [
    5,
    6,
    22,
    23,
    14,
    26,
    24,
    24,
    24,
    23,
]  # Episode counts. Index 0 is for Webisodes.
quotePattern = r"([\w\s\.\',-\[\]\d&\"#]+):(.+)"
with open(os.path.join('app', 'static', 'titles.json'), 'r', encoding="utf-8") as file:
    titles = json.load(file)


class Season(db.Model):
    """
    Represents a complete season of The Office, complete with a variable number of Episode objects.
    As a a Database Object, it can be queried to attain all active instantiated Season objects.
    """

    id = db.Column(db.Integer, primary_key=True)
    episodes = db.relationship("Episode", backref="season", lazy="dynamic")

    def __init__(self, **kwargs):
        """
        Instantiates a Season object.

        :param kwargs: Requires a `id` paramter 0-9 inclusive, plus any relevant SQLAlchemy database arguments.
        """
        assert 0 <= kwargs.get("id") <= 9, "Season ID must be 0-9 inclusive"
        super(Season, self).__init__(**kwargs)

    def build(self, rebuild=False):
        """

        :param rebuild:
        """
        print(f"Running build() on Season {self.id}")
        for episode in range(1, episodes[self.id] + 1):
            ep = Episode.query.filter_by(season_id=self.id, number=episode).first()
            if ep is None:
                # Add the episode, then build
                print(f"Creating new Episode, Season {self.id}, Episode {episode}")
                ep = Episode(season_id=self.id, number=episode)
                db.session.add(ep)
                # I'm commiting early, which is a bit taboo, but I'm more worried about what the Episode object will need while building.
                db.session.commit()
                ep.build()
            else:
                if rebuild:
                    print(f"Rebuilding Season {self.id}, Episode {episode}")
                    ep.build()

    def download(self, force=False):
        episodes = Episode.query.filter_by(season_id=self.id).all()
        for ep in episodes:
            ep.rebuild()

    @staticmethod
    def create_all(build=True):
        """
        creates new Season objects and runs build() on them"""
        for i in range(1, 10):
            if Season.query.get(i) is None:
                s = Season(id=i)
                db.session.add(s)
                if build:
                    s.build()
        db.session.commit()

    @staticmethod
    def rebuild_all():
        """
        Runs .build() on all Season objects in database
        """
        for season in Season.query.all():
            season.rebuild()

    @property
    def characters(self, sort):
        """
        returns a List of all characters in this Season, built off the Episode's .characters() method
        """
        pass


class Episode(db.Model):
    """
    represents a Episode with underlying Sections (representing a specific cutscene in the show)
    also has some other attributes useful for identify the episode and displaying, as well as countless methods
    aimed at providing easy to access information using the database collection
    """

    id = db.Column(
        db.Integer, primary_key=True
    )  # arbitrary ID, should NOT be relied on to determine episode number or correlating season
    number = db.Column(db.Integer)  # episode number
    title = db.Column(db.String(32))
    season_id = db.Column(
        db.Integer, db.ForeignKey("season.id")
    )  # correlating season number
    built = db.Column(db.Boolean, default=False)
    sections = db.relationship(
        "Section", backref="episode", lazy="dynamic"
    )  # sections of quotes under this episode

    @property
    def link(self):
        return f"http://officequotes.net/no{self.season_id}-{str(self.number).zfill(2)}.php"

    @property
    def HTMLpath(self):
        """
        Returns the path for the HTML file with data for this episode.

        :return: A string c ontaining the path to this Episode's raw HTML file.
        """
        return os.path.join("app", "data", "raw", f"{self.season_id}-{self.number}.html")

    @property
    def HTMLdata(self) -> str:
        """
        Returns the path for the HTML file with data for this episode.

        :return: A string containing the raw HTML data for this Episode.
        """
        return open(self.HTMLpath, "r", encoding="utf-8").read()

    @property
    def JSONpath(self) -> str:
        """
        Returns the path for the JSON file with data for this episode

        :return: A string containing the path to this Episode's raw JSON file.
        """
        return os.path.join("app", "data", "preprocess", f"{self.season_id}-{self.number}.json")

    @property
    def JSONdata(self):
        """
        Returns the raw JSON data for this episode.

        :return: A string containing the raw JSON data for this Episode.
        """
        return open(self.JSONpath, "r", encoding="utf-8").read()

    @property
    def downloaded(self):
        """
        Checks whether the raw episode script data has been downloaded. Uses `os.path.exists`, and thus the check
         is limited to the existence of said file, not a correctly formatted, well formed, and relevant file.

        :return: A boolean stating whether the raw HTML data for this Episode has been deleted.
        """
        return os.path.exists(self.HTMLpath)

    def download(self, force=False):
        """
        Downloads the raw HTML data for this Episode. Will not download if the file already exists (`Episode.downloaded`)
        unless specified, and uses `utf-8` encoding to preserve special characters. All subsequent read and write operations
        using this data will require `utf-8` encoding.

        :param force: Downloads the file anyways, even if it is already downloaded. Defaults to False.
        """
        if not self.downloaded or force:
            print(f"Downloading e{self.number}/s{self.season_id} from {self.link}")
            data = requests.get(self.link).text
            open(self.HTMLpath, "w+", encoding="utf-8").write(data)

    @staticmethod
    def test():
        e = Episode.query.all()[0]
        e.preprocess()

    def preprocess(self):
        """
        Runs pre-processing on this Episode, which creates and automatically builds a JSON file full of the data
        required to create a Episode properly, right before the Developer edits a episode and then enters it into the
        database as a full fledged 'processed' episode.
        """
        print(f'Pre-processing data for {self}')
        print(f'Rebuilding s{self.season_id} e{self.number}')
        self.download()

        soup = BeautifulSoup(self.HTMLdata, "html.parser")
        sections = soup.find_all(attrs={"class": "quote"})
        deleted = 0

        root = []

        for section in sections:
            isNewpeat = False
            isDeleted = "deleted scene" in section.text.lower()
            if isDeleted:
                print(section)
            if isDeleted:
                deleted += 1

            quotes = []
            if not isDeleted:
                for quote in section.find_all("b"):
                    if "Newpeat" in quote.string:
                        quote = quote.next_sibling
                        isNewpeat = True
                    # if quote is None or quote.next_sibling is None:
                    #     print("Quote is None or next sibling is None")
                    #     continue
                    quotes.append(quote.string + quote.next_sibling.string)
            else:
                paragraph = section.parent.find_all("p")[-1]
                for quote in paragraph.find_all("b"):
                    quotes.append(quote.string + quote.next_sibling.string)

            if len(quotes) == 0:
                print(f"Section found with Zero quotes. Newpeat: {isNewpeat} Deleted: {isDeleted}")
                if not (isNewpeat or isDeleted):
                    continue

            sectionData = {'isNewpeat': isNewpeat, 'isDeleted': isDeleted, 'quotes': quotes}
            root.append(sectionData)

        with open(self.JSONpath, 'w+', encoding='utf-8') as file:
            json.dump(root, file, indent=4)

    def build(self):
        """
        Downloads, Processes, and Automatically creates Sections and Quotes
        """

        self.built = True
        self.title = titles[self.season_id][self.number - 1]
        print(self.title)
        db.session.commit()

    def rebuild(self):
        """
        Clears all sections from this Episode, then builds it.
        """
        print(f'Rebuilding s{self.season_id} e{self.number}')
        self.clear()
        self.build()

    def clear(self):
        """
        Completely delete all sections relevant to this Episode so that data can be re-entered into the database,
        removing the possibility of erroring data staying inside the Database.
        """
        sections = Section.query.filter_by(episode_id=self.id).all()
        if len(sections > 0):
            print(f"Clearing {len(sections)} Sections of Ep {self.number} Season {self.season_id}")
            for section in sections:
                section.clear(commit=False, delete=True)
            self.built = False
            db.session.commit()
        else:
            print(f'No sections for this episode (s{self.season_id}/e{self.number}) could be found.')

    @staticmethod
    def clear_all():
        """
        Runs `Episode.clear()` on every episode in the database.
        """
        print('Clearing all episodes in database.')
        for episode in Episode.query.all():
            episode.clear()

    def __repr__(self):
        sections = len(Section.query.filter_by(episode_id=self.id).all())
        return f"Episode(id={self.id} s={self.season_id} ep={self.number} sects=[{sections}...])"


class Section(db.Model):
    """represents a Section of Quotes, a specific scene with relevant dialog"""

    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"))
    deleted = db.Column(db.Integer, default=-1)
    newpeat = db.Column(db.Boolean, default=False)
    quotes = db.relationship("Quote", backref="section", lazy="dynamic")

    def build(self, quotes, commit=False, reset=False):
        """
        Given an List of unformatted script quotes, automatically creates Quotes assigned to this Section
        """
        for i, quote in enumerate(quotes):
            if quote.lower().startswith("deleted scene"):
                raise Exception(
                    f'Deleted Scene Quote passed to Section Builder: "{quote}"'
                )
            # match = re.match(quotePattern, quote)
            # assert match != None, f"Quote '{quote}' could not be processed."
            # q = Quote(section=self, speaker=match[1].strip(), text=match[2].strip())
            mark = quote.find(":")
            q = Quote(
                section=self,
                speaker=quote[:mark],
                text=quote[mark + 1:],
                section_index=i,
            )
            db.session.add(q)
        if commit:
            db.session.commit()

    def clear(self, doprint=False, commit=True, delete=False):
        """
        Delete all quotes relevant to this section.
        """
        quotes = Quote.query.filter_by(section_id=self.id).all()
        if doprint:
            print(f"Clearing {len(quotes)} quotes from Section ID {self.id}")
        for quote in quotes:
            db.session.delete(quote)
        if delete:
            db.session.delete(self)
        if commit:
            db.session.commit()

    def __repr__(self):
        season = Episode.query.get(self.episode_id).id
        quotes = len(Quote.query.filter_by(section_id=self.id).all())
        return f"Section(id={self.id} S-EP={season}/{self.episode_id} quotes=[{quotes}...])"


class Quote(db.Model):
    """represents a specific quote by a specific speaker"""

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer, db.ForeignKey("section.id")
    )  # The section this quote belongs to.
    speaker = db.Column(db.String(32))  # The name of a character
    text = db.Column(
        db.String(512)
    )  # The content of the Quote. Usually a sentence, sometimes more.
    section_index = db.Column(db.Integer)  # The index of this quote in the section

    def __repr__(self):
        return f"Quote(speaker='{self.speaker}' text='{self.text[:50]}{'...' if len(self.text) > 51 else ''}')"
