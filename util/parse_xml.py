import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path
import sys

if len(sys.argv) > 1:
    XML_FILE = sys.argv[1]
else:
    XML_FILE = 'data/academia.stackexchange.com/Posts.xml'

class XML2DataFrame:

    def __init__(self, xml_file):
        tree = ET.parse(xml_file)
        self.root = tree.getroot()

    def parse_root(self, root):
        """Return a list of dictionaries from the text
         and attributes of the children under this XML root."""
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        """ Collect {key:attribute} and {tag:text} from the XML
         element and all its children into a single dictionary of strings."""
        if parsed is None:
            parsed = dict()

        for key in element.keys():
            if key not in parsed:
                parsed[key] = element.attrib.get(key)
            else:
                raise ValueError('duplicate attribute {0} at element {1}'.format(key, element.getroottree().getpath(element)))

        """ Apply recursion (Note: we technically don't need this because 
         the <row>s don't have children) """
        for child in list(element):
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        """ Initiate the root XML, parse it, and return a dataframe"""
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)

xml2df = XML2DataFrame(XML_FILE)
xml_dataframe = xml2df.process_data()
csv_file = Path(XML_FILE).with_suffix('').with_suffix('.csv') # remove suffix then add csv
xml_dataframe.to_csv(csv_file)
print('Saved data to %s' % csv_file)
