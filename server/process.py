import json
import os
import re
import time
import traceback
from collections import defaultdict
from math import ceil
from typing import Iterable, Tuple

import enlighten
import requests
from bs4 import BeautifulSoup

session = requests.Session()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

folder_exts = {'html': 'html', 'processed': 'json', 'raw': 'txt'}
episode_counts = [6, 22, 23, 14, 26, 24, 24, 24, 23]


def get_filename(season: int, episode: int, extension: str) -> str:
    """Get filename for any given episode in standardized format"""
    return f'{season}-{str(episode).zfill(2)}.{extension}'


def get_filepath(season: int, episode: int, folder: str) -> str:
    """Get full filepath for a episode's datafile for a given folder."""
    if folder:
        return os.path.join(DATA_DIR, folder, get_filename(season, episode, folder_exts.get(folder, 'json')))
    return os.path.join(DATA_DIR, get_filename(season, episode, 'json'))


def load_file(filepath: str, parse_json: bool):
    """Shortcut function for loading file from filepath, with JSON parsing flag."""
    if parse_json:
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        with open(filepath, 'r') as file:
            return file.read()


def get_episodes(season: int = None) -> Iterable[Tuple[int, int]]:
    """
    Yields a list of Episode & Season tuples.
    If Season is specified, it yields
    """
    if season:
        if 1 <= season <= 9:
            for episode in range(1, episode_counts[season - 1]):
                yield season, episode
    else:
        for season, ep_count in enumerate(episode_counts, start=1):
            for episode in range(1, ep_count + 1):
                yield season, episode


def verify_episode(season: int, episode: int = None) -> bool:
    """
    Verifies that a Season or Season + Episode is valid.
    """
    return 1 <= season <= 9 and (episode is None or 1 <= episode <= episode_counts[season])


def sleep_from(wait_time: float, moment: float, manager: enlighten.Manager = None) -> float:
    """
    Sleeps for a specific amount of time, accordingly to a previous moment.

    :param wait_time: The minimum amount of time that must be waited since the specified moment.
    :param moment: Epoch time.
    :param manager: Progressbar Manager
    """
    passed = time.time() - moment
    time_slept = wait_time - passed
    if time_slept > 0.01:
        if manager:
            time_slept = round(time_slept, 2)
            total, delay = ceil(time_slept * 100), time_slept / 100
            bar = manager.counter(total=total, desc='Sleeping...', leave=False)
            for _ in range(total):
                time.sleep(delay)
                bar.update()
            bar.close()
        else:
            time.sleep(time_slept)
        return time_slept
    else:
        return 0


def get_raw(season, episode):
    html_filename = f'{season}-{str(episode).zfill(2)}.html'
    html_filepath = os.path.join(DATA_DIR, 'html', html_filename)

    # If .html file exists, read
    if os.path.exists(html_filepath):
        # print('Reading from disk...')
        with open(html_filepath, 'r', encoding='utf-8') as file:
            page_data = file.read()
    # If not, write to disk for later usage
    else:
        link = f"http://officequotes.net/no{season}-{str(episode).zfill(2)}.php"
        resp = session.get(link)
        if resp.ok:
            page_data = resp.text
            with open(html_filepath, 'w', encoding='utf-8') as file:
                file.write(page_data)
        else:
            raise Exception(f'HTTPError: {resp.status_code} at "{resp.url}"')

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

    with open(os.path.join(DATA_DIR, 'raw', f'{season}-{str(episode).zfill(2)}.txt'), 'w',
              encoding='utf-8') as file:
        file.write('\n'.join(data))


def episodes():
    ep_nums = [6, 22, 23, 14, 26, 24, 24, 24, 23]
    for season_num, ep_count in enumerate(ep_nums, start=1):
        for episode_num in range(1, ep_count + 1):
            yield season_num, episode_num


def download_all_raw():
    for season_num, episode_num in episodes():
        print(f'{season_num}-{str(episode_num).zfill(2)}')
        try:
            get_raw(season_num, episode_num)
        except Exception as exception:
            print(f'Failed to process Season {season_num} Episode {episode_num} - ({type(exception).__name__})')
            traceback.print_exc()


def process(season, episode):
    with open(os.path.join(DATA_DIR, 'raw', f'{season}-{str(episode).zfill(2)}.txt'), 'r',
              encoding='utf-8') as file:

        sections = []
        for s in re.split('^-', file.read(), flags=re.MULTILINE):
            section = {
                'quotes': []
            }

            section_data = list(s.strip().split('\n'))
            if section_data[0].startswith('!'):
                section['deleted'] = int(re.search('!(\d+)', section_data.pop(0)).group(1))

            for q in section_data:
                quote = q.split('|', 1)
                print(quote)
                section['quotes'].append(
                    {
                        'speaker': quote[0],
                        'text': quote[1]
                    }
                )
            sections.append(section)

        with open(os.path.join(DATA_DIR, 'processed', f'{season}-{str(episode).zfill(2)}.json'), 'w',
                  encoding='utf-8') as file:
            json.dump(sections, file, indent=4, ensure_ascii=False)

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

        print(f'{quote_count} quotes.')
        print(f'{deleted_count[0]} different deleted sections, {len(deleted_count[1])} unique.')
        print(f'{len(speakers)} Speakers:')
        print(', '.join(speakers))


def generate_algolia():
    data = []
    quote_num = 0
    for season, episode in episodes():
        try:
            with open(os.path.join(DATA_DIR, 'processed', f'{season}-{str(episode).zfill(2)}.json'), 'r',
                      encoding='utf-8') as file:
                episode_data = json.load(file)
        except FileNotFoundError:
            print(f'No JSON data for Season {season} Episode {episode}')
        else:
            for section_num, section in enumerate(episode_data, start=1):
                for quote in section['quotes']:
                    quote_num += 1
                    quote['quote'] = quote_num
                    quote['section'] = section_num
                    quote['episode'] = episode
                    quote['season'] = season

                    quote['is_deleted'] = 'deleted' in section.keys()
                    quote['deleted_section'] = section.get('deleted')

                    data.append(quote)

    with open(os.path.join(DATA_DIR, 'algolia.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_episode_scenes(season, episode):
    filepath = os.path.join(DATA_DIR, 'processed', f'{season}-{str(episode).zfill(2)}.json')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return None


def get_characters(season, episode):
    scenes = get_episode_scenes(season, episode)
    if scenes is None:
        return None

    characters = defaultdict(int)
    for scene in scenes:
        for quote in scene['quotes']:
            characters[quote['speaker']] += 1
    characters = [{'name': character, 'appearances': appearances, 'id': '-'.join(character.split(' ')).lower()}
                  for character, appearances in characters.items()]
    return list(sorted(characters, key=lambda item: item['appearances'], reverse=True))


def generate_final():
    """Merge episode descriptions/titles and quotes into final JSON file."""
    with open(os.path.join(DATA_DIR, 'descriptions.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)

    output = []
    for season_id, season in enumerate(data, start=1):
        output.append({
            'season_id': season_id,
            'episodes': [
                {
                    'title': episode['title'].strip(),
                    'description': episode['description'].strip(),
                    'episode_id': episode_id,
                    'characters': get_characters(season_id, episode_id),
                    'scenes': get_episode_scenes(season_id, episode_id)
                }
                for episode_id, episode in enumerate(season, start=1)
            ]
        })

    with open(os.path.join(DATA_DIR, 'data.json'), 'w', encoding='utf-8') as file:
        json.dump(output, file, ensure_ascii=False, indent=4)


# generate_algolia()
# process(3, 10)
generate_final()
