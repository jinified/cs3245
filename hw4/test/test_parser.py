#!/usr/bin/env python3

from ..parser import parse_xml

# Filepaths
QUERY1_PATH = "q1.xml"


def test_parse_query1():
    query1 = parse_xml(QUERY1_PATH) 
    assert query1['title'] == 'Washers that clean laundry with bubbles'
