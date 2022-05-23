import copy
import imghdr
import json
import logging
import os
import re
import shutil
import subprocess
from collections import Counter, OrderedDict
from typing import Any, Dict, List, Optional, Tuple, Union

import click
import requests
import rich.progress
from dotenv import load_dotenv
from helpers import clean_string, get_close_matches_indexes, marked_item_merge
from lxml import etree
from rich.logging import RichHandler
from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn, TimeElapsedColumn, track

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]",
                    handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger('normalization.main')
logger.setLevel(logging.DEBUG)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRUTH_DIR = os.path.join(CUR_DIR, 'truth')
CHARACTERS_DIR = os.path.join(CUR_DIR, 'characters')
EPISODES_DIR = os.path.join(TRUTH_DIR, 'episodes')
COMPILE_DIR = os.path.join(CUR_DIR, 'compile')
RAW_DIR = os.path.join(CUR_DIR, 'raw')
BUILD_DIR = os.path.join(CUR_DIR, 'build')
IMG_DIR = os.path.join(CUR_DIR, 'img')
IMG_EPISODES_DIR = os.path.join(IMG_DIR, 'episodes')
IMG_CHARACTERS_DIR = os.path.join(IMG_DIR, 'characters')

RAW_FILES = os.listdir(RAW_DIR)
EPISODE_COUNTS = [6, 22, 23, 14, 26, 24, 24, 24, 23]


def abslistdir(path: str) -> List[str]:
    return [os.path.join(path, item) for item in os.listdir(path)]


@click.group()
def cli():
    pass


@cli.group()
def build():
    """The last stage of data processing, building the JSON files used by the application & Algolia indexing."""


class Constants:
    """Filename constants and such."""
    SPEAKER_MAPPING_XML = 'speaker_mapping.xml'
    IDENTIFIERS_XML = 'identifiers.xml'
    CHARACTERS_XML = 'characters.xml'
    META_JSON = 'meta.json'
    EPISODE_DESCRIPTION_JSON = 'episode_descriptions.json'
    CHARACTER_DESCRIPTION_JSON = 'character_descriptions.json'


class ConstantPaths:
    """Fully resolved paths to constant files containing parseable information."""
    SPEAKER_MAPPING = os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML)
    IDENTIFIERS = os.path.join(CHARACTERS_DIR, Constants.IDENTIFIERS_XML)
    CHARACTERS = os.path.join(TRUTH_DIR, Constants.CHARACTERS_XML)
    META = os.path.join(TRUTH_DIR, Constants.META_JSON)
    EP_DESC = os.path.join(CUR_DIR, Constants.EPISODE_DESCRIPTION_JSON)
    CHAR_DESC = os.path.join(CUR_DIR, Constants.CHARACTER_DESCRIPTION_JSON)


@cli.command('truth')
def truth():
    """Step 1: Builds raw files into truth files."""
    logger.info("Processing all raw files into normalized truth files.")

    speakers = Counter()
    for raw_file in RAW_FILES:
        raw_path = os.path.join(RAW_DIR, raw_file)

        truth_filename = raw_file.replace('txt', 'xml')

        with open(raw_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()

            root = etree.Element('SceneList')
            try:
                for section_num, raw_section in enumerate(re.split('^-', raw_data, flags=re.MULTILINE), start=1):
                    sceneElement = etree.SubElement(root, 'Scene')

                    scene_data = list(raw_section.strip().split('\n'))
                    if scene_data[0].startswith('!'):
                        # Notate that scene is deleted on Scene Element Attributes
                        sceneElement.attrib['deleted'] = re.search(r'!(\d+)', scene_data.pop(0)).group(1)

                    # Process quotes in each scene
                    for quote in scene_data:
                        quoteElement = etree.SubElement(sceneElement, 'Quote')
                        speaker, text = quote.split('|', 1)
                        speaker, text = clean_string(speaker), clean_string(text)
                        speakers[speaker] += 1

                        if len(speaker) <= 1:
                            raise Exception("Speaker text had less than two characters.")
                        elif len(text) <= 1:
                            raise Exception("Quote text had less than two characters.")

                        rootSpeakerElement = etree.SubElement(quoteElement, 'Speaker')
                        rootSpeakerElement.text = speaker
                        textElement = etree.SubElement(quoteElement, "Text")
                        textElement.text = text
            except Exception:
                logger.exception(f'Skipped {raw_file}: Malformed data.')
                if quote:
                    logger.info(
                            f'Last quote seen "{quote if type(quote) is str else "|".join(quote)}" in section {section_num}')
            else:
                truth_path = os.path.join(EPISODES_DIR, truth_filename)
                with open(truth_path, 'w') as truth_file:
                    etree.indent(root, space=" " * 4)
                    truth_file.write(etree.tostring(root, encoding=str, pretty_print=True))

    logger.debug(f"{len(speakers)} unique speakers identified.")

    if not os.path.exists(speaker_mapping_path):
        root = etree.Element("SpeakerMappings")

        for speaker, count in sorted(speakers.items(), key=lambda item: item[1], reverse=True):
            rootSpeakerElement = etree.SubElement(root, "Mapping", count=str(count))
            sourceElement = etree.SubElement(rootSpeakerElement, "Source")
            sourceElement.text = speaker
            destinationElement = etree.SubElement(rootSpeakerElement, "Destination")
            destinationElement.text = speaker

        with open(ConstantPaths.SPEAKER_MAPPING, 'w', encoding='utf-8') as speaker_file:
            etree.indent(root, space=" " * 4)
            speaker_file.write(etree.tostring(root, encoding=str, pretty_print=True))
    else:
        logger.warning('Skipped exporting speakers; delete "speaker_mapping.xml" prior to export next time.')


@cli.command('merge')
def merge():
    """Step 2: Merge all Speaker Mappings from source into one file."""
    speaker_list = Counter()

    truth_files: List[str] = os.listdir(EPISODES_DIR)
    logger.debug(f"{len(truth_files)} truth files available.")

    for truth_filename in track(truth_files):
        truth_path = os.path.join(EPISODES_DIR, truth_filename)
        with open(truth_path, 'r') as truth_file:
            root = etree.parse(truth_file)
            for speaker in root.xpath('//SceneList/Scene/Quote/Speaker/text()'):
                speaker_list[speaker] += 1

    logger.debug('Speakers acquired from Truth files.')

    speaker_mapping = OrderedDict()
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as speaker_mapping_file:
        root_mapping_element: etree.ElementBase = etree.parse(speaker_mapping_file)
        for mappingElement in root_mapping_element.xpath('//SpeakerMappings/Mapping'):
            source, destination = mappingElement.xpath('.//Source/text()')[0], \
                                  mappingElement.xpath('.//Destination/text()')[0]
            speaker_mapping[source] = destination

    logger.debug('Mappings loaded.')

    root = etree.Element('CharacterList')
    seen = set()

    logger.debug('Merging Speaker Mappings...')
    for speaker in track(speaker_list.keys(), 'Merging Map...'):
        while speaker_mapping.get(speaker) is not None:
            if speaker_mapping.get(speaker) == speaker:
                break
            else:
                speaker = speaker_mapping[speaker]

        if speaker not in seen:
            seen.add(speaker)
            character_element = etree.SubElement(root, 'Character')
            character_element.text = speaker

    logger.debug("Speaker mappings merged. Exporting to `characters.xml`")

    with open(ConstantPaths.CHARACTERS, 'w') as character_file:
        etree.indent(root, space=" " * 4)
        character_file.write(etree.tostring(root, encoding=str, pretty_print=True))


def valuify(value: str) -> str:
    """
    Simplifies character names into slug-like identifiers.

    Woman #4 -> woman
    Woman From Buffalo -> woman-from-buffalo
    Edward R. Meow -> edward-r-meow
    """
    value = re.sub(r'\s+', '-', value.lower().strip())
    value = re.sub(r'#\d+', '', value)
    value = re.sub(r'\d+(?:st|nd|rd|th)', '', value)
    value = re.match(r'^-*(.+[^-])-*$', value).group(1)
    value = re.sub(r'[.\[\],;\'\"]', '', value)
    return value


@cli.command('ids')
def ids():
    """Step 3: Builds an XML file for identifying character id mappings"""

    logger.info("Building ID Character mapping file...")

    with open(ConstantPaths.CHARACTERS, 'r') as characters_file:
        characters: List[str] = etree.parse(characters_file).xpath('//CharacterList/Character/text()')
        logger.debug('Characters parsed.')

    logger.debug(f'{len(characters)} characters parsed.')

    if not os.path.exists(CHARACTERS_DIR):
        os.makedirs(CHARACTERS_DIR)
        logger.info('`characters` directory created.')

    pre_existing: Dict[str, etree.Element] = None
    if os.path.exists(ConstantPaths.IDENTIFIERS):
        logger.debug('Identifier file exists already. Pre-existing Speakers will be kept.')

        with open(ConstantPaths.IDENTIFIERS, 'r') as identifier_file:
            pre_identifiers: etree.ElementBase = etree.parse(identifier_file)

        pre_existing = OrderedDict()
        for speaker in pre_identifiers.xpath('//SpeakerList/Speaker'):
            speaker_name = speaker.xpath('./RawText/text()')[0]
            pre_existing[speaker_name] = speaker

    root = etree.Element('SpeakerList')
    split_patterns: List[str] = [r'\s*,\s*',
                                 r'\s*&\s*',
                                 r'\s+and,?(?:\s+|$)',
                                 r'\s*[\\/]\s*']
    split_pattern: str = '|'.join(split_patterns)

    existing_characters_count: int = 0
    new_characters_count: int = 0

    # Pre-existing character identifiers are kept at the top, in order.
    for speaker_name in characters:
        if pre_existing is not None:
            if speaker_name in pre_existing.keys():
                root.append(pre_existing[speaker_name])
                del pre_existing[speaker_name]
                existing_characters_count += 1
                continue
            else:
                logger.debug(f'New speaker: `{speaker_name}`')
                new_characters_count += 1

        # New speaker to insert
        speaker_element = etree.SubElement(root, 'Speaker', annotated="false")
        raw_text_element = etree.SubElement(speaker_element, "RawText")
        raw_text_element.text = speaker_name

        split_text: List[str] = re.split(split_pattern, speaker_name)
        split_text = [split for split in split_text if re.match(r'\w{2,}', split) is not None]

        is_compound: bool = len(split_text) > 1
        is_background: bool = re.search(r'#\d', speaker_name) is not None  # Not fool-proof, but filters some out.

        if is_compound:
            speaker_element.attrib['annotated'] = "true"
            annotated_text_element = etree.SubElement(speaker_element, 'AnnotatedText')
            characters_element = etree.SubElement(speaker_element, 'Characters')
            annotated_text_element.text = speaker_name
            for sub_character in split_text:
                subcharacter_element = etree.SubElement(characters_element, 'Character')
                subcharacter_element.text = valuify(sub_character)
                subcharacter_element.attrib['type'] = 'null'
        else:
            character_element = etree.SubElement(speaker_element, 'Character')
            character_element.attrib['type'] = 'background' if is_background else 'null'
            character_element.text = valuify(speaker_name)

    logger.debug(
            f'{new_characters_count} new speaker elements added. {existing_characters_count} speaker elements preserved.')

    if pre_existing is not None:
        unseen_chars = list(pre_existing.keys())
        if len(unseen_chars) > 0:
            for unseen in unseen_chars:
                root.append(pre_existing[unseen])
                logger.debug(f'Character preserved but not seen: `{unseen}`')

    logger.debug('Exporting identifiers file.')
    with open(ConstantPaths.IDENTIFIERS, 'w') as identifier_file:
        etree.indent(root, space=" " * 4)
        identifier_file.write(etree.tostring(root, encoding=str, pretty_print=True))


@cli.command('meta')
def meta() -> None:
    """Step 4: Creates a meta file for storing each character identifier's meta meaning (main/recurring/background/meta)"""
    logger.debug('Creating meta.json')

    with open(ConstantPaths.IDENTIFIERS, 'r') as identifiers_file:
        speakers: List[str] = etree.parse(identifiers_file).xpath('//SpeakerList/Speaker')
        logger.debug(f'{len(speakers)} speakers parsed.')

    meta_data: OrderedDict[str, Optional[str]]
    if os.path.exists(ConstantPaths.META):
        with open(ConstantPaths.META, 'r') as meta_file:
            meta_data = OrderedDict(json.load(meta_file))

        possible_values = [None, 'main', 'recurring', 'background', 'meta']
        for character_id, character_type in meta_data.items():
            if character_type not in possible_values:
                logger.warning(f'Unexpected value for `{character_id}` = `{character_type}`')
    else:
        meta_data = OrderedDict()

    for speaker in speakers:
        characters = speaker.xpath('./Characters/Character') or speaker.xpath('./Character')
        for character in characters:
            name = character.text
            meta_type = character.attrib['type']
            if meta_type == 'null':
                meta_type = None

            if meta_type is not None or name not in meta_data.keys():
                meta_data[name] = meta_type

    logger.debug(f'Writing {len(meta_data.keys())} character values to disk.')
    with open(ConstantPaths.META, 'w') as meta_file:
        json.dump(meta_data, meta_file, indent=4)
    logger.debug('Meta file written.')


@cli.command('run_all')
@click.option('--confirm', is_flag=True, help='Force confirm through the confirmation prompt')
def run_all(confirm: bool) -> None:
    """Runs all commands in order one after another."""
    logger.warning('`all` command running...')
    if confirm or click.confirm("This command can be very destructive to unstaged/uncommitted data, are you sure?"):
        logger.debug('Running `truth`')
        truth()
        logger.debug('Running `merge`')
        merge()
        logger.debug('Running `ids`')
        ids()
        logger.debug('Running `meta`')
        meta()
    else:
        logger.info('Canceled.')


@cli.command('similar')
@click.argument('text')
@click.option('-d', '--destination', is_flag=True, help='Search Destination mapping instead of Source.')
@click.option('-n', '--results', type=int, default=5, help='Specify the number of results to be returned.')
@click.option('--no-merge', is_flag=True, help='Don\'t merge similar items together to make things easier.')
@click.option('-r', '--reversed', is_flag=True,
              help='Reverse the results direction to help readability in the console.')
def similar(text: str, destination: Optional[bool], results: int, reversed: bool, no_merge: bool) -> None:
    """Locates the most similar character name in speaker mappings. Searches <Source> by default."""
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as mapping_file:
        root: etree.ElementBase = etree.parse(mapping_file)

    mapping_type: str = "Source"
    if destination:
        mapping_type = "Destination"

    counts: Union[List[int], List[str]] = list(
            map(int, root.xpath('//SpeakerMappings/Mapping/@count')))  # Parse counts into integers for merge
    speakers = root.xpath(f"//SpeakerMappings/Mapping/{mapping_type}/text()")
    if not no_merge: speakers, counts = marked_item_merge(speakers, counts)  # Merge identical speakers together
    if results == -1:
        results = len(speakers)

    result_indexes: List[int] = get_close_matches_indexes(text, speakers, results, 0)
    results = [f'{speakers[i]} ({counts[i]})' for i in result_indexes]
    results = [f'{i}. {item}' for i, item in enumerate(results, start=1)]
    if reversed: results.reverse()

    print('\n'.join(results))


@cli.command('compile')
def compile() -> None:
    logger.debug('Final compile started.')

    if not os.path.exists(COMPILE_DIR):
        os.makedirs(COMPILE_DIR)
        logger.debug('Compile directory created.')

    speaker_mapping: Dict[str, str] = OrderedDict()
    logger.debug('Parsing speaker mappings...')
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as speaker_mapping_file:
        speaker_mapping_root: etree.ElementBase = etree.parse(speaker_mapping_file)
        for mapping_element in speaker_mapping_root.xpath('//SpeakerMappings/Mapping'):
            source = mapping_element.xpath('./Source/text()')[0]
            destination = mapping_element.xpath('./Destination/text()')[0]

            if source in speaker_mapping.keys():
                logger.warning(f'Key Source `{source}` overwritten.')

            speaker_mapping[source] = destination
    logger.debug(f'{len(speaker_mapping.keys())} speaker mappings parsed.')

    character_mappings: Dict[str, etree.ElementBase] = OrderedDict()
    logger.debug('Acquiring character identification mappings...')
    with open(ConstantPaths.IDENTIFIERS, 'r') as identifier_file:
        speaker_list_root: etree.ElementBase = etree.parse(identifier_file)

        for speaker in speaker_list_root.xpath('//SpeakerList/Speaker'):
            raw_text = speaker.find('RawText').text
            character_mappings[raw_text] = speaker

    episode_files = os.listdir(EPISODES_DIR)
    logger.debug(f'Beginning processing for {len(episode_files)} episode files.')

    for file in track(episode_files, 'Compiling Episodes'):
        file_path = os.path.join(EPISODES_DIR, file)
        output_path = os.path.join(COMPILE_DIR, file)

        compile_root = etree.Element('SceneList')

        try:
            with open(file_path, 'r') as ep_file:
                episode_root: etree.ElementBase = etree.parse(ep_file)

                for truth_scene in episode_root.xpath('//SceneList/Scene'):
                    compile_scene = etree.SubElement(compile_root, 'Scene')

                    # Deleted scene marker handling
                    if truth_scene.attrib.get("deleted", False):
                        compile_scene.attrib["deleted"] = "true"
                        compile_scene.attrib["deleted_scene"] = str(int(truth_scene.attrib["deleted"]))

                    for truth_quote in truth_scene.xpath('./Quote'):
                        truth_speaker: str = truth_quote.find('Speaker').text
                        truth_text: str = truth_quote.find('Text').text

                        # parent compiled Quote element
                        compile_quote = etree.SubElement(compile_scene, 'Quote')

                        # The text actually said in the quote
                        quote_text_element = etree.SubElement(compile_quote, 'QuoteText')
                        quote_text_element.text = truth_text

                        # Speaker Parent Element
                        speaker_element = etree.SubElement(compile_quote, 'Speaker')

                        # This is the (possibly annotated) list of characters referenced by this quote's raw speaker.
                        character_mapping: etree.ElementBase = character_mappings[speaker_mapping[truth_speaker]]
                        is_annotated = character_mapping.attrib.get("annotated", "false") == "true"

                        # Speaker Text - the text displayed, annotated or not, that shows who exactly is speaking
                        speaker_text_element = etree.SubElement(speaker_element, "SpeakerText")
                        speaker_text_element.attrib["annotated"] = "true" if is_annotated else "false"
                        if is_annotated:
                            speaker_text_element.text = character_mapping.find('AnnotatedText').text
                        else:
                            speaker_text_element.text = character_mapping.find('RawText').text

                        # The constituent referenced characters in the SpeakerText element
                        characters_element = etree.SubElement(speaker_element, 'Characters')
                        has_multiple = character_mapping.find("Characters") is not None

                        if has_multiple:
                            for character in character_mapping.xpath('./Characters/Character'):
                                characters_element.append(copy.deepcopy(
                                        character
                                ))
                        else:
                            characters_element.append(copy.deepcopy(
                                    character_mapping.find('Character')
                            ))
        except Exception as e:
            logger.error(f"Failed while processing `{file}`", exc_info=e)

        with open(output_path, 'w') as compile_file:
            etree.indent(compile_root, space=" " * 4)
            compile_file.write(etree.tostring(compile_root, encoding=str, pretty_print=True))

    logger.info('Completed episode data compiling.')


@cli.command('meta-update')
def meta_update() -> None:
    """Update identifiers.xml with type meta data from meta.json"""

    with open(ConstantPaths.META, 'r') as meta_file:
        meta_data = json.load(meta_file)

    null_count: int = len(list(filter(lambda v: v is None, meta_data.values())))
    if null_count > 0:
        logger.warning(f"{null_count} characters still have null values.")

    with open(ConstantPaths.IDENTIFIERS, 'r') as identifier_file:
        identifiers = etree.parse(identifier_file)

    for character in identifiers.xpath('//SpeakerList/Speaker/Character'):
        character.attrib["type"] = meta_data.get(character.text) or "null"

    for character in identifiers.xpath('//SpeakerList/Speaker/Characters/Character'):
        character.attrib["type"] = meta_data.get(character.text) or "null"

    with open(ConstantPaths.IDENTIFIERS, 'w') as identifier_file:
        etree.indent(identifiers, space=" " * 4)
        identifier_file.write(etree.tostring(identifiers, encoding=str, pretty_print=True))


@cli.command('check')
@click.option('-v', '--verbose', is_flag=True, help='Show verbose results of where errors are found.')
def check(verbose: bool) -> None:
    """Check all files for errors or possible errors in output."""

    with open(ConstantPaths.IDENTIFIERS, 'r') as identifier_file:
        identifiers = etree.parse(identifier_file)

    # Check that identifier RawText does not contain brackets
    logger.debug('Checking RawText for issues.')
    for raw_text in identifiers.xpath('//SpeakerList/Speaker/RawText/text()'):
        if '{' in raw_text or '}' in raw_text:
            logger.warning(f'Character `{raw_text}` contains a bracket in the <RawText> element.')

    # Check that each character has AnnotatedText if annotated = true, same with reverse
    logger.debug('Checking AnnotatedText elements for issues.')
    for character in identifiers.xpath('//SpeakerList/Speaker'):
        annotate_state: str = character.attrib.get("annotated")
        speaker_name: str = character.find('RawText').text

        if annotate_state is None:
            logger.warning(f'Missing annotation on `{speaker_name}`')
        elif annotate_state == "true":
            if character.find('AnnotatedText') is None:
                logger.warning(f'Missing AnnotatedText on `{speaker_name}`')
        elif annotate_state == "false":
            if character.find('AnnotatedText') is not None:
                logger.warning(f'False annotation on `{speaker_name}`')
        else:
            logger.warning(f"Unexpected annotation state `{annotate_state}` on `{speaker_name}`")

    # TODO: Check for values in meta.json that are null
    # TODO: Check for values in meta.json that are not referenced anywhere in identifiers.xml
    # TODO: Check for character IDs in identifiers.xml that don't look correct (voice--on-phone)


@cli.command('images')
def images() -> None:
    """Requests all images from episoes as available on themoviedb.org"""

    API_KEY = os.getenv('THEMOVIEDB_API_KEY')

    API_URL = 'https://api.themoviedb.org/3'
    GET_CONFIGURAITON = API_URL + '/configuration'
    GET_EPISODE_IMAGES = API_URL + '/tv/{tv_id}/season/{season_number}/episode/{episode_number}/images'

    the_office = 2316

    # Get image still sizes & base url
    configuration = requests.get(GET_CONFIGURAITON, {'api_key': API_KEY}).json()
    IMG_BASE_URL = configuration['images']['secure_base_url']
    STILL_SIZE = 'original'

    with rich.progress.Progress() as progress:
        season_task = progress.add_task('Overall', total=sum(EPISODE_COUNTS))
        episode_task = progress.add_task('Season ?')

        for season in range(9):
            s = season + 1
            progress.update(episode_task, description=f'Season {s}', total=EPISODE_COUNTS[season], completed=0)

            for episode in range(EPISODE_COUNTS[season]):
                e = episode + 1

                episode_dir_path = os.path.join(IMG_EPISODES_DIR, f'{s:02}', f'{e:02}')
                if not os.path.exists(episode_dir_path):
                    logger.debug('Creating directory: {}'.format(
                            os.path.relpath(IMG_DIR, episode_dir_path)
                    ))
                    os.makedirs(episode_dir_path)

                logger.debug(f'Acquiring images for S{s}E{e}')
                request_url = GET_EPISODE_IMAGES.format(tv_id=the_office,
                                                        season_number=season + 1,
                                                        episode_number=episode + 1)
                logger.debug(request_url)
                episode_images = requests.get(request_url, params={'api_key': API_KEY}).json()

                if len(episode_images['stills']) < 1:
                    logger.warning(f'No stills found for S{s}E{e}')
                else:
                    stills = episode_images['stills']
                    logger.debug(f'{len(stills)} stills received for S{s}E{e}.')

                    for i, still in enumerate(stills, start=1):
                        file_extension = still['file_path'].split('.')[-1]
                        image_path = os.path.join(episode_dir_path, f'{i:02}.{file_extension}')
                        still_url = IMG_BASE_URL + STILL_SIZE + still["file_path"]

                        if os.path.exists(image_path):
                            head_response = requests.head(still_url)

                            content_length = int(head_response.headers['Content-Length'])
                            existing_file_size = os.stat(image_path).st_size
                            if content_length == existing_file_size:
                                logger.debug(f'Skipping already downloaded file ({content_length / (1024):.2f} KB).')
                                continue
                            else:
                                logger.warning(
                                        'Image at {} will be overwritten.'.format(os.path.relpath(IMG_DIR, image_path)))

                        logger.debug(
                                'Downloading {}x{} image @ {}'.format(still['width'], still['height'], still['file_path']))

                        img_rsp = requests.get(still_url, stream=True)
                        if img_rsp.status_code == 200:
                            with open(image_path, 'wb') as f:
                                img_rsp.raw.decode_content = True
                                shutil.copyfileobj(img_rsp.raw, f)
                            logger.debug('Image downloaded to {}'.format(
                                    os.path.relpath(IMG_DIR, image_path)
                            ))
                        else:
                            logger.warning('Failed to download image!')

                progress.update(episode_task, advance=1)
                progress.update(season_task, advance=1)


@build.command('app')
@click.option('--path', type=str, default=BUILD_DIR, help='The output path for the application data files.')
@click.option('--mega', type=click.Path(file_okay=False, exists=True), default=None, help='The output path for the "mega episode file".')
@click.option('--make-dir', is_flag=True, help='Create the output directory if it does not exist.')
def app(path: str, mega: str, make_dir: bool) -> None:
    """Build the data files used by the application."""
    logger.debug('Build process called for "app".')
    logger.debug(f'Output Directory: "{os.path.relpath(path, os.getcwd())}"')

    with open(ConstantPaths.EP_DESC, 'r') as episode_desc_file:
        episode_desc = json.loads(episode_desc_file.read())

    with open(ConstantPaths.CHAR_DESC, 'r') as character_desc_file:
        character_desc = json.loads(character_desc_file.read())

    if not os.path.exists(path):
        if path == BUILD_DIR or make_dir:
            os.makedirs(BUILD_DIR)
            logger.debug('Build directory did not exist; it has been created.')
        else:
            logger.error('The output directory given does not exist.',
                         click.BadOptionUsage("path", "Path supplied does not exist."))
    elif not os.path.isdir(path):
        logger.error("The output directory given is not a directory.",
                     click.BadOptionUsage("path", "Path supplied is not a directory."))

    episode_files = os.listdir(COMPILE_DIR)
    logger.debug(f'Beginning processing of {len(episode_files)} compiled episode directories.')

    progress = Progress(SpinnerColumn('dots10'), *Progress.get_default_columns(), MofNCompleteColumn(),
                        TimeElapsedColumn())

    all_season_data: List[List[dict]] = [[] for _ in episode_desc]

    no_char_data = OrderedDict()
    all_appearances = Counter()

    with progress:
        for episodeFile in progress.track(episode_files, description='Building Episodes', update_period=0.01):
            with open(os.path.join(COMPILE_DIR, episodeFile), 'r') as ep_file:
                episode_root: etree.ElementBase = etree.parse(ep_file)

            seasonNum, episodeNum = map(int, re.match(r'(\d+)-(\d+)\.xml', episodeFile).groups())
            description = episode_desc[seasonNum - 1][episodeNum - 1]

            # Count character appearances
            characters = Counter()
            all_characters = episode_root.xpath('./Scene/Quote/Speaker/Characters/Character')
            for character in all_characters:
                character_type = character.attrib['type']
                if character_type in ['main', 'recurring']:
                    characters[character.text] += 1

            episode_characters: Dict[str, Dict[str, Union[str, int]]] = {}
            for character_id, count in sorted(characters.items(), key=lambda item: item[1], reverse=True):
                if character_id in character_desc.keys():
                    character_name = character_desc[character_id]['name']
                else:
                    print(f'No character description: {character_id}')
                    character_name = f'\"{character_id.capitalize()}\"'
                    no_char_data[character_id] = None

                episode_characters[character_id] = {
                    'name': character_name,
                    'appearances': count
                }

            scenes = []
            for scene in episode_root.xpath('./Scene'):
                quotes = []

                for quote in scene.xpath('./Quote'):
                    speaker_text = quote.xpath('./Speaker/SpeakerText')[0]
                    is_annotated = speaker_text.attrib['annotated'] == 'true'
                    quote_text = quote.find('QuoteText').text

                    quote_json = {
                        'speaker': speaker_text.text,
                        'text': quote_text,
                        "isAnnotated": is_annotated
                    }

                    if is_annotated:
                        character_elements = quote.xpath('./Speaker/Characters/Character')
                        split_speaker_text: List[str] = re.split(r'({[^}]+})', speaker_text.text)
                        if len(split_speaker_text[0]) == 0: del split_speaker_text[0]
                        if len(split_speaker_text[-1]) == 0: del split_speaker_text[-1]
                        text_start: int = 0 if split_speaker_text[0].startswith('{') else 1

                        # {Jim}, {Dwight}, and {Andy}'s Computer
                        # [jim, dwight, andy]
                        # -> {jim}, {dwight}, and {andy}'s Computer

                        quote_json['characters'] = {
                            character.text: None for character in character_elements
                        }

                        for i, character in enumerate(character_elements):
                            index = text_start + (i * 2)
                            quote_json['characters'][character.text] = split_speaker_text[index][1:-1]
                            split_speaker_text[index] = '{' + character.text + '}'

                        quote_json['speaker'] = ''.join(split_speaker_text)
                    else:
                        quote_json['character'] = quote.xpath('./Speaker/Characters/Character/text()')[0]

                    quotes.append(quote_json)
                scenes.append({'quotes': quotes})

            all_season_data[seasonNum - 1].append({
                'title': description['title'],
                'description': description['description'],
                'characters': episode_characters,
                'seasonNumber': seasonNum,
                'episodeNumber': episodeNum,
                "scenes": scenes
            })

            all_appearances += characters

    season_episode_data: List[Tuple[int, int, Any]] = []
    for season_data in all_season_data:
        for episode_data in season_data:
            season, episode = episode_data['seasonNumber'], episode_data['episodeNumber']
            season_episode_data.append((season, episode, episode_data))

    mega_file_data: List[List[Any]] = [[None for _ in range(count)] for count in EPISODE_COUNTS]

    with progress:
        for season, episode, episode_data in progress.track(season_episode_data, description='Saving episode data...',
                                                            update_period=0.1):
            mega_file_data[season - 1][episode - 1] = episode_data

            season_directory = os.path.join(path, f'{season:02}')
            if not os.path.exists(season_directory):
                os.makedirs(season_directory)

            episode_path = os.path.join(season_directory, f'{episode:02}.json')

            with open(episode_path, 'w') as episode_file:
                json.dump(episode_data, episode_file)

    if mega is not None:
        with open(os.path.join(mega, 'data.json'), 'w') as mega_file:
            json.dump(mega_file_data, mega_file)
        logger.debug('Mega data file written.')

    episodes_path = os.path.join(path, 'episodes.json')
    included: List[str] = ['characters', 'description', 'title', 'episodeNumber', 'seasonNumber']
    basic_episode_data = [[None for _ in range(count)] for count in EPISODE_COUNTS]
    for season, episode, episode_data in season_episode_data:
        basic_episode_data[season - 1][episode - 1] = {key: episode_data[key] for key in included}

    with open(episodes_path, 'w') as episodes_file:
        json.dump(basic_episode_data, episodes_file)

    character_path = os.path.join(path, 'characters.json')
    character_folder = os.path.join(path, 'character')

    def merge(a, b) -> dict:
        return {**a, **b}

    character_data = {
        id: merge(data, {'appearances': all_appearances.get(id, 0)})
        for id, data in character_desc.items()
    }

    with open(character_path, 'w') as character_file:
        json.dump(character_data, character_file)

    # Ensure character folder exists before writing files
    if not os.path.exists(character_folder):
        os.makedirs(character_folder)

    for id, data in character_data.items():
        character_path = os.path.join(path, 'character', id + '.json')
        with open(character_path, 'w') as file:
            json.dump(data, file)


@build.command('media')
@click.option('--suppress/--no-suppress', default=True, help='Disable stdout suppression for image magick commandline output.')
@click.option('--copy/--no-copy', default=True, help='Complete the copying stage.')
@click.option('--thumbnail/--no-thumbnail', default=True, help='Complete the thumbnailing stage.')
@click.argument('path', type=click.Path(file_okay=False))
def media(path: str, suppress: bool, copy: bool, thumbnail: bool) -> None:
    def get_fullsize_args(input_path: str, output_path: str) -> List[str]:
        return ['magick',
                input_path,
                '-gravity', 'Center',
                '-crop', '1:1+0+0',
                '+repage',
                '-quality', '95',
                '-interlace', 'none',
                '-colorspace', 'sRGB',
                '-strip',
                output_path]

    def get_thumbnailing_args(input_path: str, output_path: str, geometry: str = '156') -> List[str]:
        return [
            'magick',
            input_path,
            '-gravity', 'Center',
            '-crop', '1:1+0+0',
            '+repage',
            '-filter', 'Triangle',
            '-define', 'filter:support=2',
            '-thumbnail', geometry,
            '-unsharp', '0.25x0.25+8+0.065',
            '-dither', 'None',
            '-posterize', '136',
            '-quality', '82',
            '-define', 'jpeg:fancy-upsampling=off',
            '-define', 'png:compression-filter=5',
            '-define', 'png:compression-level=9',
            '-define', 'png:compression-strategy=1',
            '-define', 'png:exclude-chunk=all',
            '-interlace', 'none',
            '-colorspace', 'sRGB',
            '-strip',
            output_path,
        ]

    if not (copy or thumbnail):
        logger.error('Both copy and thumbnail stages are disabled. Quitting early.')
        return

    with open(ConstantPaths.CHAR_DESC, 'r') as character_desc_file:
        descriptions = json.load(character_desc_file)

    character_ids = list(descriptions.keys())
    operations: List[Tuple[str, str, List[str]]] = []

    # /img/episode/03/04/full.jpeg
    all_episodes: List[Tuple[int, int]] = [(season + 1, episode + 1) for season in range(9) for episode in range(EPISODE_COUNTS[season])]

    progress = Progress(SpinnerColumn('dots10'), *Progress.get_default_columns(), MofNCompleteColumn(),
                        TimeElapsedColumn())

    with progress:
        for season, episode in progress.track(all_episodes, description='Preparing epsiode image operations...'):
            # Find what images are available, select the one with the lowest integer
            episode_dir = os.path.join(IMG_EPISODES_DIR, f'{season:02}', f'{episode:02}')
            if not os.path.exists(episode_dir):
                os.makedirs(episode_dir)
            images_available = os.listdir(episode_dir)
            images_available.sort(key=lambda x: int(x.split('.')[0]))

            input_path: str = os.path.join(episode_dir, images_available[0])
            output_dir: str = os.path.abspath(os.path.join(path, f'{season:02}', f'{episode:02}'))

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_full_path: str = os.path.join(output_dir, 'full.jpeg')
            output_thumb_path: str = os.path.join(output_dir, 'thumbnail.jpeg')

            if copy:
                args = get_fullsize_args(input_path, output_full_path)
                operations.append((input_path, output_full_path, args))
            if thumbnail:
                args = get_thumbnailing_args(input_path, output_thumb_path)
                operations.append((input_path, output_thumb_path, args))

    character_folders: List[str] = abslistdir(IMG_CHARACTERS_DIR)
    filetype_preference: List[str] = ['jpeg', 'jpg', 'png', 'webp', 'gif', 'bmp']

    def select_by_preference(x: str) -> int:
        """A simple function for sorting files by the preferred extensions."""
        extension = os.path.splitext(x)[1][1:]
        try:
            index: int = filetype_preference.index(extension)
            return index
        except ValueError:
            return len(filetype_preference)

    with progress:
        for character_folder in progress.track(character_folders, description='Preparing & selecting character images...'):
            character_id = os.path.split(character_folder)[1]
            if character_id not in character_ids:
                logger.warning(f'"{character_id}" is not a valid character identifier. Please check the character list.')
                continue

            character_files = os.listdir(character_folder)
            character_files.sort(key=select_by_preference)
            full_file: Optional[str] = None
            face_file: Optional[str] = None

            # Find full file
            for file in character_files:
                if file.startswith('full'):
                    full_file = file
                    break

                if file.startswith('face'):
                    face_file = file
                    break

            # Check what was found, use the files found as best as possible.
            if face_file is None:
                if full_file is None:
                    if len(character_files) > 0:
                        for file in character_files:
                            file_path = os.path.join(character_folder, file)
                            filetype = imghdr.what(file_path)
                            logger.debug(f'[{character_id}] File: "{file}" -> Filetype: {filetype}')
                            if filetype in filetype_preference:
                                full_file = file
                                face_file = file
                                break

                        if full_file is not None:
                            logger.warning(f'[{character_id}] No face nor full files could be located, but "{file}" has been selected automatically.')
                        else:
                            logger.warning(f'[{character_id}] Neither face nor full files could be located.')
                    else:
                        logger.warning(f'[{character_id}] No files available.')
                else:
                    logger.debug(f'[{character_id}] Full file will be used as face file.')
                    face_file = full_file
            elif full_file is None:
                logger.debug(f'[{character_id}] Face file will be used as full file.')
                full_file = face_file

            if full_file is None and face_file is None:
                logger.warning(f'[{character_id}] Skipping due to no files found.')
                continue

            if full_file is not None:
                full_file = os.path.join(character_folder, full_file)
            if face_file is not None:
                face_file = os.path.join(character_folder, face_file)

            output_dir: str = os.path.abspath(os.path.join(path, character_id))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if copy:
                output_full_path: str = os.path.join(output_dir, 'full.jpeg')
                output_face_path: str = os.path.join(output_dir, 'face.jpeg')

                full_args = get_fullsize_args(full_file, output_full_path)
                face_args = get_fullsize_args(face_file, output_face_path)

                operations.append((full_file, output_full_path, full_args))
                operations.append((face_file, output_face_path, face_args))

            if thumbnail:
                output_full_thumb_path: str = os.path.join(output_dir, 'full_thumb.jpeg')
                output_face_thumb_path: str = os.path.join(output_dir, 'face_thumb.jpeg')

                full_thumb_args = get_thumbnailing_args(full_file, output_full_thumb_path)
                face_thumb_args = get_thumbnailing_args(face_file, output_face_thumb_path)

                operations.append((full_file, output_full_thumb_path, full_thumb_args))
                operations.append((face_file, output_face_thumb_path, face_thumb_args))

    logger.debug(f'Starting {len(operations)} operations.')
    sp_kwargs = {'capture_output': True, 'text': True} if suppress else {}

    with progress:
        logger.debug('Beginning "smart copying"...')
        task = progress.add_task(description='Wait...', total=len(operations))

        for input, output, args in operations:
            try:
                rel_output = os.path.relpath(output, start=path)
                progress.update(task, description=rel_output, advance=1)
                completed = subprocess.run(args, **sp_kwargs, check=True)
            except Exception as e:
                logger.error('Failed to process operation.', exc_info=e)
                logger.error(f'Input: "{input}"')
                logger.error(f'Output: "{output}"')
                logger.error(f'Args: "{" ".join(args)}"')
                if type(e) is subprocess.CalledProcessError:
                    logger.error(f'Stdout: "{e.stdout.rstrip()}"')
                    logger.error(f'Stderr: "{e.stderr.rstrip()}"')

    with progress:
        output_paths = [y for x, y, z in operations]

        file_sizes = []
        for path in progress.track(output_paths, description='Acquiring sizes...'):
            file_sizes.append(os.stat(path).st_size)


if __name__ == '__main__':
    cli()
