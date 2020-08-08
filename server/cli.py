"""
cli.py

CLI entrypoint for fetching, processing and compiling quote data.
"""

import logging
import os
import sys
import time
from typing import List, Tuple

import click
import enlighten
import requests

sys.path[0] += '\\..'
from server.process import get_episodes, get_filepath, sleep_from, verify_episode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cli')
logger.setLevel(logging.DEBUG)
manager = enlighten.get_manager()


@click.group()
def cli():
    """Base command group."""
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
    Fetches data from officequotes.net, placing them in unmodified UTF-8 HTML files.
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
                        with open(filepath, 'w', encoding='utf-8') as file:
                            file.write(resp.text)
                        logger.debug('Successfully fetched.')
                    else:
                        logger.error(f'Fetching failed. Erroneous response code {resp.status_code}.')
                pbar.update()
        logger.info('Fetching complete.')


@cli.command('process')
def process():
    """
    Processes manually processed raw quote data into JSON.
    """
    pass


@cli.group('build')
def build():
    """Data building command group."""
    pass


@build.command('algolia')
def algolia():
    """
    Generates algolia.json, a all encompassing file for Algolia's search index.
    """
    pass


@build.command('final')
def final():
    """Generates the latest application static data.json file, used by the backend API."""
    pass


if __name__ == "__main__":
    cli()
