import glob
import json
import os
from xml.etree import ElementTree

import xmltodict

from src import find_cardinality
from src.utils.file_manipulation import PATH

table = []
folder = PATH


def run(folder):
    if os.path.exists(PATH + "\\first_output.xml"):
        os.remove(PATH + "\\first_output.xml")
    else:
        print('first_output.xml does not exit')

    files = glob.glob(folder + "/*.xml")
    first = None

    for filename in files:
        data = ElementTree.parse(filename).getroot()
        if first is None:
            first = data
        else:
            first.extend(data)
    if first is not None:
        config = ElementTree.tostring(first).decode()
        with open(PATH + "\\first_output.xml", "w+", encoding="utf-8") as h:
            h.write(config)


def create_output_xml_file():
    # print(relation)
    relation_list = find_cardinality.find_cardinality()
    print(relation_list)
    output_dic = {'er': {'relation': relation_list}}

    with open(PATH + '\\relation.json', 'w+') as json_file:
        json.dump(output_dic, json_file, indent=4, sort_keys=True)

    output_xml = xmltodict.unparse(output_dic, pretty=True)

    with open(PATH + '\\relation.xml', 'w+') as xml_file:
        xml_file.write(output_xml)

    run(folder)


# create_output_xml_file()


def recreate_relation_xml(er):
    global member1_name, member1_cardinality, member1_primary_key, member2_primary_key, member2_name, member2_cardinality
    print(er)
    relationships_list = []
    for dic in er:
        print(dic)
        relationship = dic.get("name")
        cardinality = dic.get("type")
        degree = dic.get("degree")
        entities = dic.get("entities")
        for entity in entities:
            if entity.get('id') == 1:
                member1_name = entity.get("name")
                member1_cardinality = entity.get("cardinality")
                member1_primary_key = entity.get("primaryKey")
            elif entity.get('id') == 2:
                member2_name = entity.get("name")
                member2_cardinality = entity.get("cardinality")
                member2_primary_key = entity.get("primaryKey")
            elif entity.get('id') == 3:
                member3_name = entity.get("name")
                member3_cardinality = entity.get("cardinality")
                member3_primary_key = entity.get("cardinality")

                if degree == 'binary' or degree == 'unary':
                    relationships_list.append({"@name": relationship, "@degree": degree, "@type": cardinality,
                                               "member1": {"@name": member1_name, "@cardinality": member1_cardinality,
                                                           "@primary_key": member1_primary_key},
                                               "member2": {"@name": member2_name, "@cardinality": member2_cardinality,
                                                           "@primary_key": member2_primary_key}})
                elif degree == 'ternary':
                    relationships_list.append({"@name": relationship, "@degree": degree, "@type": cardinality,
                                               "member1": {"@name": member1_name, "@cardinality": member1_cardinality,
                                                           "@primary_key": member1_primary_key},
                                               "member3": {"@name": member3_name, "@cardinality": member3_cardinality,
                                                           "@primary_key": member3_primary_key},
                                               "member2": {"@name": member2_name, "@cardinality": member2_cardinality,
                                                           "@primary_key": member2_primary_key}})

    print(relationships_list)
    output_dic = {'er': {'relation': relationships_list}}

    with open(PATH + '\\relation.json', 'w+') as json_file:
        json.dump(output_dic, json_file, indent=4, sort_keys=True)

    output_xml = xmltodict.unparse(output_dic, pretty=True)

    with open(PATH + '\\relation.xml', 'w+') as xml_file:
        xml_file.write(output_xml)

    run(folder)
