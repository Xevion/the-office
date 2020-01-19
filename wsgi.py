from app import app, db
from app.models import Season, Episode, Section, Quote

@app.shell_context_processor
def make_shell_context():
        return {
            'db' : db,
            'Season' : Season,
            'Episode' : Episode,
            'Section' : Section,
            'Quote' : Quote
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0")
