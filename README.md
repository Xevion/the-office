# the-office

A Vue.js and Flask Web Application designed to provide a quick way to search for quotes from NBC's "The Office".

## Screenshots

![Episode Script](episode.png)
![Search Result Highlighting](search_results.png)

## Features

- Vue.js based, providing fast SPA functionality
    - Setup via Vue CLI
    - Vue Router
    - Vue Bootstrap
    - Axios
    - Vue Instantsearch (Algolia)
- Backend API provided by Flask
- Instant Search provided Algolia
- Sleek, responsive design that is easy on the eyes

## Quote Data

### Credit

Credit to [officequotes.net/](https://www.officequotes.net/) for providing all quote data.

Credit to [imdb.com](https://www.imdb.com/title/tt0386676/) for episode descriptions.

### Processing

Quotes are scraped directly from the website as of this moment.

This repository will hold the current pre-processed raw quote data, but the application has the ability to fetch and parse
HTML pages directly as needed.

```
python server/cli.py fetch
    --season SEASON          Fetches all episodes from a specific season.
    --episode EPISODE        Fetches a specific episode. Requires SEASON to be specified.
    --all                    Fetches data for every episode from every season.
    --skip SEASON:EPISODE    When specified, it will skip a given episode.
```

The data has to be parsed, but due to high irregularity (at least too much for me to handle), the files will have to be
inspected and manually processed.

```python server/cli.py preprocess
    -s --season SEASON     Pre-processes all episodes from a specific season.
    -e --episode EPISODE   Pre-processes a specific episode. Requires SEASON to be specified.
    -a --all               Pre-processes all episodes from every season.
    -o --overwrite         DANGER: Will overwrite files. May result in manually processed files to be lost forever.
```

From then on, once all files have been pre-processed, you will have to begin the long, annoying process of editing them into my custom format.

These raw pre-processed files are located in `'./server/data/processed/`

Each section (barring the first) is pre-pended by a .hyphen.

```
CharacterName: Text that character says.
OtherCharacter: More text that other character says..
-
ThirdCharacter: Text that character says in a second scene/section.
-!1
Fourth Character With Spaces In Name: Text that fourth character says in a deleted scene.
Fifth-Character: Which deleted scene? Deleted scene number one.
```

Deleted scenes are marked by a initial exclamation mark, and then a number of digits marking which deleted scene they are a part of.

Please note that extra text like 'Deleted Scenes 3' might appear before a hyphen - this is expected and is helpful when deciding
which scene goes with which Deleted Scene ID. If you don't know, do what I did - go look at the web page it's based on.
Otherwise, I read the quotes and figure out based on context.

This concept is rather loose, slow, and dumb, it simply allows me to mark what deleted scenes go together while working
with a incredibly inconsistent, human curated data format.

To ease text processing, I did come up with RegEx expressions for search and replacement:

```
^([\w\s]+\-*[\w\s]*):\s+
$1|
```

From then on, the process becomes much simpler, 95% of the work needed to process quotes is already done.

Now that quotes are in a consistent (although custom) format, they need to be processed into individual episodes. In reality,
they are just the JSON format of the previous stage.

```
python server/cli.py process
    -s --season SEASON     Processes all episodes from a specific season.
    -e --epsiode EPISODE   Processes a specific episode. Requires SEASON to be specified.
    -a --all               Processes all episodes from all seasons.
```

Now that they're all in individual files, the final commands can be ran to compile them into one file, a static
'database' or something. Technically, they could be kept scattered, but I decided to make it simpler with just 1 big file.

This also is where Algolia comes in.

```
python server/cli.py build [algolia|final]
```

Each command is ran with no special arguments (as of now), generating a `algolia.json` or `data.json` in the `./server/data/` folder.

This `data.json` file is loaded by the Flask server and the `algolia.json` can be uploaded to your primary index.

For every command mentioned, you can read all arguments with `--help`:

```
$ python cli.py preprocess --help
Usage: cli.py preprocess [OPTIONS]

  Pre-processes raw HTML files into mangled custom quote data.

  Custom quote data requires manual inspection and formatting, making it a
  dangerous operation that may overwrite precious quote data.

Options:
  -s, --season INTEGER          Season to be fetched. Without --episode, will
                                download all episodes in a season.

  -e, --episode INTEGER         Specific episode to be fetched. Requires
                                --season to be specified.

  --all                         Fetch all episodes, regardless of previous
                                specifications.

  -o, --overwrite               Overwrite if a file already exists.
  -ss, --silent-skip            Skip missing/existing files silently
  -ssm, --silent-skip-missing   Skip missing files silently
  -sse, --silent-skip-existing  Skip overwrite skips silently
  --help                        Show this message and exit.
```

## Setup

This project was built on Python 3.7 and Node v12.18.3 / npm 6.14.6.

### Installation

To install all Node/NPM dependencies, run

```
npm install
```

To install Python's dependencies, run

```
pip install -r ./requirements.txt
```

I recommend that you use a virtualenv in order to keep dependencies separate from other projects, as I do.
Personally, I use PyCharm Professional to maintain virtualenvs, just because it's easy to start, use, update and maintain
them.

### Running

- Vue.js can be ran via `npm run serve`.
    - Run this in `./client/`.
- Flask can be ran via `flask run`.
    - Run this in `./server/`.
    - Add `--host=0.0.0.0` to the end to allow connections from LAN.
    
Note: Readying this application for Production and wider-development is still in progress.

**Don't try to run this application just yet.**

## To-do

Small to-do list to complete.

- Font Awesome Icons
    - SeasonList Chevron
    - Quote Permalink
- Attempt Algolia Query Suggestions
    - Redirect to SearchResults page on Enter press
- Process all quote data
- Site Meta Tags
- Better Mobile Season List
    - Smaller, collapsible?
- Heroku Production Deployment
    - Possible solution via Docker
- Axios 'Fetch' Error Handling
- Navigation Bar
    - Navbar Logo (?)
- Overall Responsiveness Improvements
- Algolia Clickthrough Events
    - Search Results Page
- Character List
- Quote Permalink
- Deleted Scenes Marker
    - Possible 'Flashback' Scene Marker
- Season List Episode Modal Popover
    - Preview Image, Description, Episode Stats
- Quote Likes Database
    - Requires difficult implementation of Flask controlled Postgres database
    - Requires funding, longterm free hosting not possible with database requirements
