import logging
import os
import re
import sys
import enlighten
from collections import Counter, OrderedDict
from pprint import pprint
from typing import List, Optional

import click
from lxml import etree

sys.path[0] += '\\..\\..'
from server.helpers import clean_string, get_close_matches_indexes, marked_item_merge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('normalization.main')
logger.setLevel(logging.DEBUG)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRUTH_DIR = os.path.join(CUR_DIR, 'truth')
RAW_DIR = os.path.abspath(os.path.join(CUR_DIR, '..', 'data', 'raw'))
RAW_FILES = os.listdir(RAW_DIR)


@click.group()
def cli():
    pass


class Constants:
    SPEAKER_MAPPING_XML = 'speaker_mapping.xml'


@cli.command('truth')
def truth():
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
                truth_path = os.path.join(TRUTH_DIR, 'episodes', truth_filename)
                with open(truth_path, 'w') as truth_file:
                    etree.indent(root, space=" " * 4)
                    truth_file.write(etree.tostring(root, encoding=str, pretty_print=True))

    logger.debug(f"{len(speakers)} unique speakers identified.")
    speaker_mapping_path = os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML)
    if not os.path.exists(speaker_mapping_path):
        root = etree.Element("SpeakerMappings")

        for speaker, count in sorted(speakers.items(), key=lambda item: item[1], reverse=True):
            rootSpeakerElement = etree.SubElement(root, "Mapping", count=str(count))
            sourceElement = etree.SubElement(rootSpeakerElement, "Source")
            sourceElement.text = speaker
            destinationElement = etree.SubElement(rootSpeakerElement, "Destination")
            destinationElement.text = speaker

        with open(speaker_mapping_path, 'w', encoding='utf-8') as speaker_file:
            etree.indent(root, space=" " * 4)
            speaker_file.write(etree.tostring(root, encoding=str, pretty_print=True))
    else:
        logger.warning('Skipped exporting speakers; delete "speaker_mapping.xml" prior to export next time.')


@cli.command('merge')
def merge():
    """Merge all Speaker Mappings from source into one file."""
    speakerList = Counter()

    truth_files: List[str] = os.listdir(os.path.join(TRUTH_DIR, 'episodes'))
    logger.debug(f"{len(truth_files)} truth files available.")
    pbar = enlighten.Counter(total=len(truth_files), unit='Files')

    for truth_filename in truth_files:
        truth_path = os.path.join(TRUTH_DIR, 'episodes', truth_filename)
        with open(truth_path, 'r') as truth_file:
            root = etree.parse(truth_file)
            for speaker in root.xpath('//SceneList/Scene/Quote/Speaker/text()'):
                speakerList[speaker] += 1
        pbar.update()

    logger.debug('Speakers acquired from Truth files.')

    speakerMapping = OrderedDict()
    with open(os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML), 'r') as speaker_mapping_file:
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

    with open(os.path.join(TRUTH_DIR, 'characters.xml'), 'w') as character_file:
        etree.indent(root, space=" " * 4)
        character_file.write(etree.tostring(root, encoding=str, pretty_print=True))


@cli.command('ids')
def ids():
    """Builds an XML file for identifying character id mappings"""

    logger.info("Building ID Character mapping file...")
    with open(os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML), 'r') as mapping_file:
        root: etree.ElementBase = etree.parse(mapping_file)

    root = etree.Element("IdentifierList")
    # mappings =
    # for speaker in speakers:
    #     if speaker



@cli.command('all')
def all():
    """Runs all commands in order one after another."""
    truth()
    merge()
    ids()


@cli.command('similar')
@click.argument('text')
@click.option('-d', '--destination', is_flag=True, help='Search Destination mapping instead of Source.')
@click.option('-n', '--results', type=int, default=5, help='Specify the number of results to be returned.')
@click.option('--no-merge', is_flag=True, help='Don\'t merge similar items together to make things easier.')
@click.option('-r', '--reversed', is_flag=True, help='Reverse the results direction to help readability in the console.')
def similar(text: str, destination: Optional[bool], results: int, reversed: bool, no_merge: bool) -> None:
    """Locates the most similar character name in speaker mappings. Searches <Source> by default."""
    with open(os.path.join(TRUTH_DIR, Constants.SPEAKER_MAPPING_XML), 'r') as mapping_file:
        root: etree.ElementBase = etree.parse(mapping_file)

    mappingType: str = "Source"
    if destination:
        mappingType = "Destination"

    counts: List[int] | List[str] = list(map(int, root.xpath('//SpeakerMappings/Mapping/@count')))  # Parse counts into integers for merge
    speakers = root.xpath(f"//SpeakerMappings/Mapping/{mappingType}/text()")
    if not no_merge: speakers, counts = marked_item_merge(speakers, counts)  # Merge identical speakers together
    if results == -1:
        results = len(speakers)

    resultIndexes: List[int] = get_close_matches_indexes(text, speakers, results, 0)
    results = [f'{speakers[i]} ({counts[i]})' for i in resultIndexes]
    results = [f'{i}. {item}' for i, item in enumerate(results, start=1)]
    if reversed: results.reverse()

    print('\n'.join(results))


if __name__ == '__main__':
    cli()
