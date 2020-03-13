from time import sleep

from src.er_drawer import create_er_xml_file, draw_er
from src.relational_schema_creator import map_er_to_relational_schema
from src.relationships_extractor import identify_relationship
from src.features import main_cordinator


def generateEntities(scenario):
    try:
        finalEntity_list = main_cordinator.intermediateLayer1(scenario)
    except BaseException as e:
        print("Entity and Attributes extraction failed.", e)
        return e
    return finalEntity_list


def generateAttributes(scenario, entitylist):
    try:
        finalAttributes_dic = main_cordinator.intermediateLayer2(scenario, entitylist)
    except BaseException as e:
        print("Entity and Attributes extraction failed.", e)
        return e
    return finalAttributes_dic


def generateOutput(finallist):
    try:
        finalOutput_dic = main_cordinator.intermediateLayer3(finallist)
    except BaseException as e:
        print("Entity and Attributes extraction failed.", e)
        return e
    return finalOutput_dic


def create_er_diagram_xml_file():
    try:
        sleep(10)
        identify_relationship.entity_combined_with_scenario()
        # find_cardinality.find_cardinality()
        create_er_xml_file.create_output_xml_file()
    except BaseException as e:
        print("Er Diagram XML file creation error", e)
        return e


def create_relational_schema():
    try:
        map_er_to_relational_schema.build_output_xml_file()
    except BaseException as e:
        print("Relational Schema creation error", e)
        return e


def create_er_diagram_text_file():
    try:
        draw_er.create_draw_text_file()
    except BaseException as e:
        print("Er Diagram text file creation error", e)
        return e
