"""
cli.py

CLI entrypoint for fetching, processing and compiling quote data.
"""
import logging
import os
import re
import sys
import time
from typing import List, Tuple, Union

import click
import enlighten
import requests
from bs4 import BeautifulSoup

sys.path[0] += '\\..'
from server.process import DATA_DIR, get_characters, get_episodes, get_filepath, load_file, \
    save_file, sleep_from, \
    verify_episode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cli')
logger.setLevel(logging.DEBUG)
manager = enlighten.get_manager()


@click.group()
def cli():
    pass


@cli.command('fetch')
@click.option('-s', '--season', type=int,
              help='Season to be fetched. Without --episode, will download all episodes in a season.')
@click.option('-e', '--episode', type=int, help='Specific episode to be fetched. Requires --season to be specified.')
@click.option('-d', '--delay', type=float, default=0.5, help='Delay between each request')
@click.option('--all', is_flag=True, help='Fetch all episodes, regardless of previous specifications.')
@click.option('-o', '--overwrite', is_flag=True, help='Overwrite if a file already exists.')
@click.option('-ss', '--silent-skip', is_flag=True, help='Skip existing files silently')
def fetch(season: int, episode: int, delay: float, all: bool, overwrite: bool, silent_skip: bool):
    """
    Downloads raw quote pages from 'officequotes.net'.

    Fetches quote pages, placing them in 'html' folder in unmodified UTF-8 HTML files.
    """
    episodes: List[Tuple[int, int]]

    if all:
        episodes = list(get_episodes())
    elif season:
        if episode:
            if verify_episode(season, episode):
                episodes = [(season, episode)]
            else:
                logger.error(f'Season {season}, Episode {episode} is not a valid combination.')
                return
        else:
            episodes = list(get_episodes(season=season))
            logger.info(f'Fetching Season {season}...')
    else:
        if episode:
            logger.info('You must specify more than just an episode.')
        else:
            logger.info('You must specify which episodes to fetch.')
        logger.info('Check --help for more information on this command.')
        return

    logger.debug(f'Ready to start fetching {len(episodes)} quote page{"s" if len(episodes) > 1 else ""}')
    session = requests.Session()
    last_request = time.time() - delay

    with enlighten.Manager() as manager:
        with manager.counter(total=len(episodes), desc='Fetching...', unit='episodes') as pbar:
            for _season, _episode in episodes:

                filepath = get_filepath(_season, _episode, 'html')

                # Check if HTML file exists
                if not overwrite and os.path.exists(filepath):
                    if not silent_skip:
                        logger.debug(f'Skipping Season {_season}, Episode {_episode}: File already exists.')
                else:
                    logger.info(f'Fetching Season {_season}, Episode {_episode}...')

                    # Generate link, make request
                    link = f"http://officequotes.net/no{_season}-{str(_episode).zfill(2)}.php"

                    sleep_from(delay, last_request, manager)  # Sleep at least :delay: seconds.

                    resp = session.get(link)
                    last_request = time.time()
                    if resp.ok:
                        # Write data to file
                        save_file(filepath, resp.text, False)
                        logger.debug('Successfully fetched & saved.')
                    else:
                        logger.error(f'Fetching failed. Erroneous response code {resp.status_code}.')
                pbar.update()
        logger.info('Fetching complete.')


@cli.command('preprocess')
@click.option('-s', '--season', type=int,
              help='Season to be fetched. Without --episode, will download all episodes in a season.')
@click.option('-e', '--episode', type=int, help='Specific episode to be fetched. Requires --season to be specified.')
@click.option('--all', is_flag=True, help='Fetch all episodes, regardless of previous specifications.')
@click.option('-o', '--overwrite', is_flag=True, help='Overwrite if a file already exists.')
@click.option('-ss', '--silent-skip', is_flag=True, help='Skip missing/existing files silently')
@click.option('-ssm', '--silent-skip-missing', is_flag=True, help='Skip missing files silently')
@click.option('-sse', '--silent-skip-existing', is_flag=True, help='Skip overwrite skips silently')
def preprocess(season: int, episode: int, all: bool, overwrite: bool, silent_skip: bool, silent_skip_missing: bool,
               silent_skip_existing: bool):
    """
    Pre-processes raw HTML files into mangled custom quote data.

    Custom quote data requires manual inspection and formatting, making it a dangerous operation that may overwrite
    precious quote data.
    """
    print(silent_skip_existing)
    episodes: List[Tuple[int, int]]

    if all:
        episodes = list(get_episodes())
    elif season:
        if episode:
            if verify_episode(season, episode):
                episodes = [(season, episode)]
            else:
                logger.error(f'Season {season}, Episode {episode} is not a valid combination.')
                return
        else:
            episodes = list(get_episodes(season=season))
            logger.info(f'Preprocessing Season {season}...')
    else:
        if episode:
            logger.info('You must specify more than just an episode.')
        else:
            logger.info('You must specify which episodes to pre-process.')
        logger.info('Check --help for more information on this command.')
        return

    for season, episode in episodes:
        # Overwrite protection
        save_path = get_filepath(season, episode, 'raw')
        if os.path.exists(save_path) and not overwrite:
            if (not silent_skip) or (not silent_skip_existing):
                logger.info(f'Skipping Season {season}, Episode {episode}, file already exists. Skipping processing.')
                continue

        try:
            page_data = load_file(get_filepath(season, episode, 'html'), False)
        except FileNotFoundError:
            if not silent_skip or not silent_skip_missing:
                logger.warning(f'No data for Season {season}, Episode {episode} available. Skipping processing.')
        else:
            soup = BeautifulSoup(page_data, "html.parser")
            data = []

            sections = soup.find_all(attrs={"class": "quote"})
            for section in sections:
                for br in section.find_all('br'):
                    br.replace_with("\n" + br.text)

                for line in section.get_text().split('\n'):
                    data.append(line.strip())

                data.append('-')
            data.pop(-1)

            data = '\n'.join(data)
            save_file(save_path, data, False)


@cli.command('process')
@click.option('-s', '--season', type=int,
              help='Season to be fetched. Without --episode, will download all episodes in a season.')
@click.option('-e', '--episode', type=int, help='Specific episode to be fetched. Requires --season to be specified.')
@click.option('--all', is_flag=True, help='Fetch all episodes, regardless of previous specifications.')
@click.option('-r', '--report', is_flag=True, help='Report quote statistics once processing completed')
def process(season: int, episode: int, all: bool, report: bool):
    """
    Processes manually processed raw quote data into JSON.
    """
    episodes: List[Tuple[int, int]]

    if all:
        episodes = list(get_episodes())
    elif season:
        if episode:
            if verify_episode(season, episode):
                episodes = [(season, episode)]
            else:
                logger.error(f'Season {season}, Episode {episode} is not a valid combination.')
                return
        else:
            episodes = list(get_episodes(season=season))
            logger.info(f'Processing Season {season}...')
    else:
        if episode:
            logger.info('You must specify more than just an episode.')
        else:
            logger.info('You must specify which episodes to process.')
        logger.info('Check --help for more information on this command.')
        return

    quote: Union[str, List[str]]
    section_num: int
    for _season, _episode in episodes:
        sections = []
        try:
            preprocessed_data = load_file(get_filepath(_season, _episode, 'raw'))
            for section_num, raw_section in enumerate(re.split('^-', preprocessed_data, flags=re.MULTILINE), start=1):
                section = {
                    'quotes': []
                }

                section_data = list(raw_section.strip().split('\n'))
                if section_data[0].startswith('!'):
                    section['deleted'] = int(re.search('!(\d+)', section_data.pop(0)).group(1))

                for quote in section_data:
                    quote = quote.split('|', 1)
                    section['quotes'].append(
                        {
                            'speaker': quote[0],
                            'text': quote[1]
                        }
                    )
                sections.append(section)
        except FileNotFoundError:
            logger.info(f'Skipped Season {_season}, Episode {_episode}, no file found.')
        except:
            logger.exception(f'Skipped Season {_season}, Episode {_episode}: Malformed data.')
            logger.info(
                f'Last quote seen "{quote if type(quote) is str else "|".join(quote)}" in section {section_num}')
        else:
            # Save processed data
            save_file(get_filepath(_season, _episode, 'processed'), sections, True)

        if report:
            deleted_count = [0, set()]
            quote_count = 0
            speakers = set()

            for section in sections:
                quote_count += len(section['quotes'])

                if 'deleted' in section.keys():
                    deleted_count[0] += 1
                    deleted_count[1].add(section['deleted'])

                for quote in section['quotes']:
                    speakers.add(quote['speaker'])

            logger.debug(f'{quote_count} quotes.')
            logger.debug(f'{deleted_count[0]} different deleted sections, {len(deleted_count[1])} unique.')
            logger.info(f'{len(speakers)} Speakers:')
            logger.info(', '.join(speakers))


@cli.group('build')
def build():
    """Build final data files used by Algolia and the backend API."""
    pass


@build.command('algolia')
@click.option('-ss', '--silent-skip', is_flag=True, help='Skip existing files silently')
@click.option('--process', is_flag=True, help='Run processing before building final data.')
def algolia(silent_skip: bool):
    """
    Generates algolia.json, a all encompassing file for Algolia's search index.
    """
    data = []
    episode_num_abs, section_num_abs, quote_num_abs = 0, 0, 0
    for season, episode in get_episodes():
        episode_num_abs += 1
        try:
            episode_data = load_file(get_filepath(season, episode, 'processed'), True)
        except FileNotFoundError:
            if not silent_skip:
                logger.warning(f'Skipping Season {season}, Episode {episode}. No episode data file found.')
        else:
            for section_num_rel, section in enumerate(episode_data, start=1):
                section_num_abs += 1
                for quote_num_rel, quote in enumerate(section['quotes'], start=1):
                    quote_num_abs += 1

                    # Relative position
                    quote['quote_rel'] = quote_num_rel
                    quote['section_rel'] = section_num_rel
                    quote['episode_rel'] = episode
                    # Absolute position
                    quote['quote_abs'] = quote_num_abs
                    quote['section_abs'] = section_num_abs
                    quote['episode_abs'] = episode_num_abs

                    quote['season'] = season

                    quote['is_deleted'] = 'deleted' in section.keys()
                    quote['deleted_section'] = section.get('deleted')

                    data.append(quote)

    logger.info(f'Saving {len(data):,} quotes to algolia.json')
    save_file(os.path.join(DATA_DIR, 'algolia.json'), data, True)


@build.command('final')
@click.option('-ss', '--silent-skip', is_flag=True, help='Skip existing files silently')
@click.option('--process', is_flag=True, help='Run processing before building final data.')
def final(silent_skip: bool):
    """Generates the latest application static data.json file, used by the backend API."""
    descriptions = load_file(os.path.join(DATA_DIR, 'descriptions.json'), True)
    seasons = [{'season_id': season, 'episodes': []} for season in range(1, 10)]
    for season_id, episode_id in get_episodes():
        # Load data file
        try:
            episode_data = load_file(get_filepath(season_id, episode_id, 'processed'), True)
        except FileNotFoundError:
            if not silent_skip:
                logger.warning(f'No data for Season {season_id}, Episode {episode_id} available. Null data inserted.')
            episode_data = None

        description = descriptions[season_id - 1][episode_id - 1]
        seasons[season_id - 1]['episodes'].append(
            {
                'title': description['title'].strip(),
                'description': description['description'].strip(),
                'episode_id': episode_id,
                'characters': get_characters(season_id, episode_id),
                'scenes': episode_data
            }
        )

    logger.info('Saving to data.json')
    save_file(os.path.join(DATA_DIR, 'data.json'), seasons, True)


if __name__ == "__main__":
    cli()
