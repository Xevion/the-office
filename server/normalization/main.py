import json
import logging
import os
import re
import sys
import enlighten
import coloredlogs
from collections import Counter, OrderedDict
from pprint import pprint
from typing import List, Optional, Union

import click
from lxml import etree

sys.path[0] += '\\..\\..'
from server.helpers import clean_string, get_close_matches_indexes, marked_item_merge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('normalization.main')
logger.setLevel(logging.DEBUG)
coloredlogs.install(level=logger.level, logger=logger)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRUTH_DIR = os.path.join(CUR_DIR, 'truth')
CHARACTERS_DIR = os.path.join(CUR_DIR, 'characters')
EPISODES_DIR = os.path.join(TRUTH_DIR, 'episodes')
COMPILE_DIR = os.path.join(CUR_DIR, 'compile')
RAW_DIR = os.path.abspath(os.path.join(CUR_DIR, '..', 'data', 'raw'))

RAW_FILES = os.listdir(RAW_DIR)


@click.group()
def cli():
    pass


class Constants:
    SPEAKER_MAPPING_XML = 'speaker_mapping.xml'
    IDENTIFIERS_XML = 'identifiers.xml'
    CHARACTERS_XML = 'characters.xml'
    META_JSON = 'meta.json'


class ConstantPaths:
    SPEAKER_MAPPING = os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML)
    IDENTIFIERS = os.path.join(CHARACTERS_DIR, Constants.IDENTIFIERS_XML)
    CHARACTERS = os.path.join(TRUTH_DIR, Constants.CHARACTERS_XML)
    META = os.path.join(TRUTH_DIR, Constants.META_JSON)


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
                    logger.info(f'Last quote seen "{quote if type(quote) is str else "|".join(quote)}" in section {section_num}')
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
    speakerList = Counter()

    truth_files: List[str] = os.listdir(EPISODES_DIR)
    logger.debug(f"{len(truth_files)} truth files available.")
    pbar = enlighten.Counter(total=len(truth_files), unit='Files')

    for truth_filename in truth_files:
        truth_path = os.path.join(EPISODES_DIR, truth_filename)
        with open(truth_path, 'r') as truth_file:
            root = etree.parse(truth_file)
            for speaker in root.xpath('//SceneList/Scene/Quote/Speaker/text()'):
                speakerList[speaker] += 1
        pbar.update()

    logger.debug('Speakers acquired from Truth files.')

    speakerMapping = OrderedDict()
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as speaker_mapping_file:
        rootMappingElement: etree.ElementBase = etree.parse(speaker_mapping_file)
        for mappingElement in rootMappingElement.xpath('//SpeakerMappings/Mapping'):
            source, destination = mappingElement.xpath('.//Source/text()')[0], mappingElement.xpath('.//Destination/text()')[0]
            speakerMapping[source] = destination

    logger.debug('Mappings loaded.')

    root = etree.Element('CharacterList')
    pbar = enlighten.Counter(total=len(speakerList.keys()), unit='Speakers')
    seen = set()

    logger.debug('Merging Speaker Mappings...')
    for speaker in speakerList.keys():
        while speakerMapping.get(speaker) is not None:
            if speakerMapping.get(speaker) == speaker:
                break
            else:
                speaker = speakerMapping[speaker]

        if speaker not in seen:
            seen.add(speaker)
            characterElement = etree.SubElement(root, 'Character')
            characterElement.text = speaker
            pbar.update()

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
            preidentifiers: etree.ElementBase = etree.parse(identifier_file)

        pre_existing = OrderedDict()
        for speaker in preidentifiers.xpath('//SpeakerList/Speaker'):
            speakerName = speaker.xpath('./RawText/text()')[0]
            pre_existing[speakerName] = speaker

    root = etree.Element('SpeakerList')
    splitPatterns: List[str] = [r'\s*,\s*',
                                r'\s*&\s*',
                                r'\s+and,?(?:\s+|$)',
                                r'\s*[\\/]\s*']
    splitPattern: str = '|'.join(splitPatterns)

    existing_characters_count: int = 0
    new_characters_count: int = 0

    # Pre-existing character identifiers are kept at the top, in order.
    for speakerName in characters:
        if pre_existing is not None:
            if speakerName in pre_existing.keys():
                root.append(pre_existing[speakerName])
                del pre_existing[speakerName]
                existing_characters_count += 1
                continue
            else:
                logger.debug(f'New speaker: `{speakerName}`')
                new_characters_count += 1

        # New speaker to insert
        speaker_element = etree.SubElement(root, 'Speaker', annotated="false")
        raw_text_element = etree.SubElement(speaker_element, "RawText")
        raw_text_element.text = speakerName

        split_text: List[str] = re.split(splitPattern, speakerName)
        split_text = [split for split in split_text if re.match(r'\w{2,}', split) is not None]

        isCompound: bool = len(split_text) > 1
        isBackground: bool = re.search(r'#\d', speakerName) is not None  # Not fool-proof, but filters some out.

        if isCompound:
            speaker_element.attrib['annotated'] = "true"
            annotated_text_element = etree.SubElement(speaker_element, 'AnnotatedText')
            characters_element = etree.SubElement(speaker_element, 'Characters')
            annotated_text_element.text = speakerName
            for sub_character in split_text:
                subcharacter_element = etree.SubElement(characters_element, 'Character')
                subcharacter_element.text = valuify(sub_character)
                subcharacter_element.attrib['type'] = 'null'
        else:
            character_element = etree.SubElement(speaker_element, 'Character')
            character_element.attrib['type'] = 'background' if isBackground else 'null'
            character_element.text = valuify(speakerName)

    logger.debug(f'{new_characters_count} new speaker elements added. {existing_characters_count} speaker elements preserved.')

    if pre_existing is not None:
        unseen_chars = list(pre_existing.keys())
        if len(unseen_chars) > 0:
            for unseen in unseen_chars:
                root.append(pre_existing[unseen])
                logger.debug(f'Character preserved but not seen: {unseen}')

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


@cli.command('all')
@click.option('--confirm', is_flag=True, help='Force confirm through the confirmation prompt')
def all(confirm: bool) -> None:
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
@click.option('-r', '--reversed', is_flag=True, help='Reverse the results direction to help readability in the console.')
def similar(text: str, destination: Optional[bool], results: int, reversed: bool, no_merge: bool) -> None:
    """Locates the most similar character name in speaker mappings. Searches <Source> by default."""
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as mapping_file:
        root: etree.ElementBase = etree.parse(mapping_file)

    mappingType: str = "Source"
    if destination:
        mappingType = "Destination"

    counts: Union[List[int], List[str]] = list(
            map(int, root.xpath('//SpeakerMappings/Mapping/@count')))  # Parse counts into integers for merge
    speakers = root.xpath(f"//SpeakerMappings/Mapping/{mappingType}/text()")
    if not no_merge: speakers, counts = marked_item_merge(speakers, counts)  # Merge identical speakers together
    if results == -1:
        results = len(speakers)

    resultIndexes: List[int] = get_close_matches_indexes(text, speakers, results, 0)
    results = [f'{speakers[i]} ({counts[i]})' for i in resultIndexes]
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
        speakering_mapping_root: etree.ElementBase = etree.parse(speaker_mapping_file)
        for mapping_element in speakering_mapping_root.xpath('//SpeakerMappings/Mapping'):
            source = mapping_element.xpath('./Source/text()')[0]
            destination = mapping_element.xpath('./Destination/text()')[0]

            if source in speaker_mapping.keys():
                logger.warning(f'Key Source `{source}` overwritten.')

            speaker_mapping[source] = destination
    logger.debug(f'{len(speaker_mapping.keys())} speaker mappings parsed.')

    episode_files = os.listdir(EPISODES_DIR)
    logger.debug(f'Beginning processing for {len(episode_files)} episode files.')

    for file in episode_files:
        file_path = os.path.join(EPISODES_DIR, file)
        output_path = os.path.join(COMPILE_DIR, file)

        compile_root = etree.Element('SceneList')

        try:
            with open(file_path, 'r') as ep_file:
                episode_root: etree.ElementBase = etree.parse(ep_file)

                for scene in episode_root.xpath('//SceneList/Scene'):
                    for quote in scene.xpath('./Quote'):
                        pass

        except Exception as e:
            logger.error(f"Failed while processing `{file}`", exc_info=e)

        with open(output_path, 'w') as compile_file:
            etree.indent(compile_root, space=" " * 4)
            # compile_file.write(etree.tostring(compile_root, encoding=str, pretty_print=True))

    logger.info('Completed episode data compiling.')


if __name__ == '__main__':
    cli()
