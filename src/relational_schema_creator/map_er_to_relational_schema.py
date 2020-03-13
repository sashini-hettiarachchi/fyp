import json
import xml.etree.ElementTree as ET
import xmltodict
from src.utils.file_manipulation import PATH

table = []


# create_er_xml_file.create_input_xml_file()


def xml_input_handling():
    tree = ET.parse(PATH + '\\first_output.xml')
    root = tree.getroot()
    # print(root)
    return root


def entities_mapping():
    root = xml_input_handling()

    for entity in root.findall('entity'):
        # print(entity.get('name'))
        if not entity.get('type') == 'weak':
            column = []
            for attribute in entity.findall('attribute'):
                type = attribute.get('type')
                value = attribute.get('value')
                if not type == 'multi-valued' and not type == 'derived' and not type == 'composite_parent':
                    # print(attribute.get('name'))
                    if value == 'primary_key':
                        new_primary_key = attribute.get('name')
                        column.append({'@name': new_primary_key, '@value1': 'primary_key'})
                        # print(column)
                    else:
                        column.append({'@name': attribute.get('name')})
                        # print(column)

            table_name = entity.get('name')

            # print(table_name)
            # print(column)
            table.append({'@name': table_name, 'column': column})
    # print(table)


def binary_one_to_one_relationship_mapping():
    root = xml_input_handling()

    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'binary':
            if relationship.get('type') == 'one_to_one':
                new_primary_key_member1 = ''
                for member1 in relationship.findall('member1'):
                    # print('member1' , member1.get('name'))
                    primary_key_member1 = member1.get('primary_key')
                    new_primary_key_member1 = primary_key_member1
                    # print(new_primary_key_member1)
                    # print('primary key of member 1' , primary_key_member1)
                for member2 in relationship.findall('member2'):
                    # print('member2', member2.get('name'))
                    # print(table)
                    for temp_table in table:
                        # print(temp_table)
                        temp_table_name = temp_table.get('@name')
                        # print(temp_table_name)
                        if member2.get('name') == temp_table_name:
                            temp_table_column_list = temp_table.get('column')
                            # print(new_primary_key_member1)
                            temp_table_column_list.append({'@name': new_primary_key_member1, '@value2': 'foreign_key',
                                                           '@ref': member1.get('name')})
                            # print(temp_table_column_list)
                            for attribute in relationship.findall('attribute'):
                                temp_table_column_list.append({'@name': attribute.get('name')})

    # print(table)


def binary_one_to_many_relationship_mapping():
    root = xml_input_handling()

    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'binary':
            if relationship.get('type') == 'one_to_many':
                foreign_key = ''
                for member1 in relationship.findall('member1'):
                    # print('member1' , member1.get('name'))
                    if member1.get('cardinality') == 'one':
                        primary_key_member1 = member1.get('primary_key')
                        foreign_key = primary_key_member1
                        # print(foreign_key)
                        # print('primary key of member 1', primary_key_member1)

                        for member2 in relationship.findall('member2'):
                            # print('member2', member2.get('name'))
                            for temp_table in table:
                                temp_table_name = temp_table.get('@name')
                                # print("tbl",temp_table_name)
                                if member2.get('name') == temp_table_name:
                                    temp_table_column_list = temp_table.get('column')
                                    # print(new_primary_key_member1)
                                    temp_table_column_list.append(
                                        {'@name': foreign_key, '@value2': 'foreign_key', '@ref': member1.get('name')})
                                    # print(temp_table_column_list)
                                    for attribute in relationship.findall('attribute'):
                                        temp_table_column_list.append({'@name': attribute.get('name')})
                    else:
                        for member2 in relationship.findall('member2'):
                            primary_key_member2 = member2.get('primary_key')
                            foreign_key = primary_key_member2
                            # print(foreign_key)

                        for temp_table in table:
                            temp_table_name = temp_table.get('@name')
                            if member1.get('name') == temp_table_name:
                                temp_table_column_list = temp_table.get('column')
                                # print(new_primary_key_member1)
                                temp_table_column_list.append(
                                    {'@name': foreign_key, '@value2': 'foreign_key', '@ref': member2.get('name')})
                                # print(temp_table_column_list)
                                for attribute in relationship.findall('attribute'):
                                    temp_table_column_list.append({'@name': attribute.get('name')})

    # print(table)


def binary_many_to_many_relationship_mapping():
    root = xml_input_handling()
    # column = []

    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'binary':
            if relationship.get('type') == 'many_to_many':
                column = []
                # print(relationship.get('name'))
                for member1 in relationship.findall('member1'):
                    primary_key_member1 = member1.get('primary_key')
                    new_primary_key_member1 = primary_key_member1
                    # print(new_primary_key_member1)
                    column.append({'@name': new_primary_key_member1, '@value1': 'primary_key', '@value2': 'foreign_key',
                                   '@ref': member1.get('name')})
                    # print("column", column)
                for member2 in relationship.findall('member2'):
                    primary_key_member2 = member2.get('primary_key')
                    new_primary_key_member2 = primary_key_member2
                    # print(new_primary_key_member2)
                    column.append({'@name': new_primary_key_member2, '@value1': 'primary_key', '@value2': 'foreign_key',
                                   '@ref': member2.get('name')})
                    # print(column)

                for attribute in relationship.findall('attribute'):
                    column.append({'@name': attribute.get('name')})

                # print(column)
                table.append({'@name': relationship.get('name'), 'column': column})
    # print(table)


def multi_valued_attribute_mapping():
    root = xml_input_handling()
    new_primary_key = ''
    for entity in root.findall('entity'):
        # print(entity.get('name'))
        if not entity.get('type') == 'weak':

            for attribute in entity.findall('attribute'):

                type = attribute.get('type')

                value = attribute.get('value')
                if value == 'primary_key':
                    primary_key = attribute.get('name')
                    new_primary_key = primary_key
                    # print(new_primary_key)

                if type == 'multi-valued':
                    multi_valued_attribute = attribute.get('name')
                    # print(multi_valued_attribute)
                    table.append({'@name': multi_valued_attribute,
                                  'column': [{'@name': multi_valued_attribute, '@value1': 'primary_key'},
                                             {'@name': new_primary_key, '@value1': 'primary_key',
                                              '@value2': 'foreign_key', '@ref': entity.get('name')}]})
    # print(table)


def unary_one_to_one_relationship_mapping():
    root = xml_input_handling()
    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'unary':
            if relationship.get('type') == 'one_to_one':
                for member1 in relationship.findall('member1'):
                    for temp_table in table:
                        temp_table_name = temp_table.get('@name')
                        if member1.get('name') == temp_table_name:
                            temp_table_column_list = temp_table.get('column')

                            for member2 in relationship.findall('member2'):
                                temp_table_column_list.append({'@name': member2.get('name'), '@value2': 'foreign_key',
                                                               '@ref': member2.get('name')})

    # print(table)


def unary_one_to_many_relationship_mapping():
    root = xml_input_handling()
    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'unary':
            if relationship.get('type') == 'one_to_many':
                for member1 in relationship.findall('member1'):
                    for temp_table in table:
                        temp_table_name = temp_table.get('@name')
                        if member1.get('name') == temp_table_name:
                            temp_table_column_list = temp_table.get('column')
                            for member2 in relationship.findall('member2'):
                                temp_table_column_list.append({'@name': member2.get('name'), '@value2': 'foreign_key',
                                                               '@ref': member1.get('name')})

    # print(table)


def unary_many_to_many_relationship_mapping():
    root = xml_input_handling()
    column = []
    for relationship in root.findall('relation'):
        if relationship.get('degree') == 'unary':
            if relationship.get('type') == 'many_to_many':
                for member1 in relationship.findall('member1'):
                    primary_key_member1 = member1.get('primary_key')
                    new_primary_key_member1 = primary_key_member1
                    # print(new_primary_key_member1)
                    column.append({'@name': new_primary_key_member1, '@value1': 'primary_key', '@value2': 'foreign_key',
                                   '@ref': member1.get('name')})
                    # print(column)
                for member2 in relationship.findall('member2'):
                    primary_key_member2 = member2.get('primary_key')
                    new_primary_key_member2 = primary_key_member2
                    # print(new_primary_key_member2)
                    column.append({'@name': new_primary_key_member2, '@value1': 'primary_key', '@value2': 'foreign_key',
                                   '@ref': member2.get('name')})
                    # print(column)

                table.append({'@name': relationship.get('name'), 'column': column})
    # print(table)


def ternary_relationship_mapping():
    root = xml_input_handling()

    for relationship in root.findall('relation'):
        column = []
        if relationship.get('degree') == 'ternary':
            for member1 in relationship.findall('member1'):
                primary_key_member1 = member1.get('primary_key')
                new_primary_key_member1 = primary_key_member1
                # print(new_primary_key_member1)
                column.append({'@name': new_primary_key_member1, '@value1': 'primary_key', '@value2': 'foreign_key',
                               '@ref': member1.get('name')})
                # print(column)
            for member2 in relationship.findall('member2'):
                primary_key_member2 = member2.get('primary_key')
                new_primary_key_member2 = primary_key_member2
                # print(new_primary_key_member2)
                column.append({'@name': new_primary_key_member2, '@value1': 'primary_key', '@value2': 'foreign_key',
                               '@ref': member2.get('name')})
                # print(column)
            for member3 in relationship.findall('member3'):
                primary_key_member3 = member3.get('primary_key')
                new_primary_key_member3 = primary_key_member3
                # print(new_primary_key_member3)
                column.append({'@name': new_primary_key_member3, '@value1': 'primary_key', '@value2': 'foreign_key',
                               '@ref': member3.get('name')})
                # print(column)

            table.append({'@name': relationship.get('name'), 'column': column})
    # print(table)


def build_output_xml_file():
    root = xml_input_handling()
    entities_mapping()
    binary_one_to_one_relationship_mapping()
    binary_one_to_many_relationship_mapping()
    binary_many_to_many_relationship_mapping()
    multi_valued_attribute_mapping()
    unary_one_to_one_relationship_mapping()
    unary_one_to_many_relationship_mapping()
    unary_many_to_many_relationship_mapping()
    ternary_relationship_mapping()
    # print(root.get('name'))
    output_dic = {'database': {'@name': root.get('name'), 'table': table}}
    # print(output_dic)

    with open(PATH+'\\output.json', 'w+') as json_file:
        json.dump(output_dic, json_file, indent=4, sort_keys=True)

    output_xml = xmltodict.unparse(output_dic, pretty=True)

    with open(PATH+'\\output.xml', 'w+') as xml_file:
        xml_file.write(output_xml)

# build_output_xml_file()
