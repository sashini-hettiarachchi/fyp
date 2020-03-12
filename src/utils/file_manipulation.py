# open input text scenario
import xml.etree.ElementTree as ET
import os

PATH = "E:\\Integrated\\Flask_App\\data"

text_file = open(PATH+"\\input_text.txt", "r")

if text_file.mode == 'r':
    # Read the scenario and covert that text file into lowercase
    input_text_load = text_file.read()
    input_text = input_text_load.lower()
    print(input_text)


# Read input XML file
def get_root_of_input_xml():
    tree = ET.parse(PATH+"\\input_xml.xml")
    root = tree.getroot()
    return root


def get_root_of_er_xml():
    tree = ET.parse(PATH+'\\first_output.xml')
    root = tree.getroot()
    print(root)
    return root


def remove_files():
    if os.path.exists(PATH+"\\first_output.xml"):
        os.remove(PATH+"\\first_output.xml")
    else:
        print('first_output.xml does not exit')

    if os.path.exists(PATH+"\\er.csv"):
        os.remove(PATH+"\\er.csv")
    else:
        print('er.csv does not exit')

    if os.path.exists(PATH+"\\er.txt"):
        os.remove(PATH+"\\er.txt")
    else:
        print('er.txt does not exit')

    if os.path.exists(PATH+"\\output.json"):
        os.remove(PATH+"\\output.json")
    else:
        print('output.json does not exit')

    if os.path.exists(PATH+"\\output.xml"):
        os.remove(PATH+"\\output.xml")
    else:
        print('output.xml does not exit')

    if os.path.exists(PATH+"\\relation.json"):
        os.remove(PATH+"\\relation.json")
    else:
        print('relation.json does not exit')

    if os.path.exists(PATH+"\\relation.xml"):
        os.remove(PATH+"\\relation.xml")
    else:
        print('relation.xml does not exit')

    if os.path.exists(PATH+"\\intermediate_text.txt"):
        os.remove(PATH+"\\intermediate_text.txt")
    else:
        print('intermediate_text.txt does not exit')
