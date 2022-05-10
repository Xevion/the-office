import json
import logging
import os
import re
import sys
import copy
import enlighten
import coloredlogs
from collections import Counter, OrderedDict
from pprint import pprint
from typing import List, Optional, Union

import click
from lxml import etree
from helpers import clean_string, get_close_matches_indexes, marked_item_merge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('normalization.main')
logger.setLevel(logging.DEBUG)
coloredlogs.install(level=logger.level, logger=logger)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRUTH_DIR = os.path.join(CUR_DIR, 'truth')
CHARACTERS_DIR = os.path.join(CUR_DIR, 'characters')
EPISODES_DIR = os.path.join(TRUTH_DIR, 'episodes')
COMPILE_DIR = os.path.join(CUR_DIR, 'compile')
RAW_DIR = os.path.abspath(os.path.join(CUR_DIR, 'raw'))

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
    speaker_list = Counter()

    truth_files: List[str] = os.listdir(EPISODES_DIR)
    logger.debug(f"{len(truth_files)} truth files available.")
    pbar = enlighten.Counter(total=len(truth_files), unit='Files')

    for truth_filename in truth_files:
        truth_path = os.path.join(EPISODES_DIR, truth_filename)
        with open(truth_path, 'r') as truth_file:
            root = etree.parse(truth_file)
            for speaker in root.xpath('//SceneList/Scene/Quote/Speaker/text()'):
                speaker_list[speaker] += 1
        pbar.update()

    logger.debug('Speakers acquired from Truth files.')

    speaker_mapping = OrderedDict()
    with open(ConstantPaths.SPEAKER_MAPPING, 'r') as speaker_mapping_file:
        root_mapping_element: etree.ElementBase = etree.parse(speaker_mapping_file)
        for mappingElement in root_mapping_element.xpath('//SpeakerMappings/Mapping'):
            source, destination = mappingElement.xpath('.//Source/text()')[0], mappingElement.xpath('.//Destination/text()')[0]
            speaker_mapping[source] = destination

    logger.debug('Mappings loaded.')

    root = etree.Element('CharacterList')
    pbar = enlighten.Counter(total=len(speaker_list.keys()), unit='Speakers')
    seen = set()

    logger.debug('Merging Speaker Mappings...')
    for speaker in speaker_list.keys():
        while speaker_mapping.get(speaker) is not None:
            if speaker_mapping.get(speaker) == speaker:
                break
            else:
                speaker = speaker_mapping[speaker]

        if speaker not in seen:
            seen.add(speaker)
            character_element = etree.SubElement(root, 'Character')
            character_element.text = speaker
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

    logger.debug(f'{new_characters_count} new speaker elements added. {existing_characters_count} speaker elements preserved.')

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
@click.option('-r', '--reversed', is_flag=True, help='Reverse the results direction to help readability in the console.')
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

    pbar = enlighten.Counter(total=len(episode_files), unit='Episodes')

    for file in episode_files:
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

        pbar.update()

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


if __name__ == '__main__':
    cli()
