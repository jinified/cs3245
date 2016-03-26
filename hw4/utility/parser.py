#!/usr/bin/env python3
from lxml import etree


def parse_xml(filepath):
    ''' Return dictionary after parsing a XML file'''
    with open(filepath) as xml_file:
        return xml_to_dict(etree.parse(xml_file).getroot())


def xml_to_dict(root):
    if root.tag == 'query':
        return {e.tag: content_from_xml(e) for e in root}
    else:
        return {e.get('name'): content_from_xml(e) for e in root}


def content_from_xml(element):
    ''' Returns content of an XML element'''
    return element.text.strip().replace('\n', '') if element.text else ''


''' UNIT TESTS '''

QUERY1_PATH = '../test/q1.xml'
CORPUS1_PATH = '../test/EP0049154B2.xml'


def test_parse_query1():
    query1 = parse_xml(QUERY1_PATH)
    assert query1['title'] == 'Washers that clean laundry with bubbles'


def test_parse_corpus1():
    corpus1 = parse_xml(CORPUS1_PATH)
    assert 'EP0049154B2' == corpus1['Patent Number']
    assert '' == corpus1['1st Assignee Address']
