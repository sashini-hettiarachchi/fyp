import xmltodict
import json
from src.utils.file_manipulation import PATH

def create_xml(xml_data):
    text=xmltodict.unparse(xml_data, pretty=True)
    with open(PATH+'\\input_xml.xml', 'w+') as xml_file:
        xml_file.write(text)
