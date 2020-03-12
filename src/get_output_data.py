from src.utils import file_manipulation

relationship_dic_list = []


def get_relationship_list():
    global member1_name, member2_name, member1_cardinality, member1_primary_key, member2_cardinality, member2_primary_key, member3_name, member3_primary_key, member3_cardinality

    root = file_manipulation.get_root_of_er_xml()
    i = 1
    for rel in root.findall('relation'):
        for member1 in rel.findall('member1'):
            member1_name = member1.get('name')
            member1_primary_key = member1.get('primary_key')
            member1_cardinality = member1.get('cardinality')

        for member2 in rel.findall('member2'):
            member2_name = member2.get('name')
            member2_primary_key = member2.get('primary_key')
            member2_cardinality = member2.get('cardinality')

        if rel.findall('member3'):
            for member3 in rel.findall('member3'):
                member3_name = member3.get('name')
                member3_cardinality = member3.get('cardinality')
                member3_primary_key = member3.get('primary_key')

        else:
            member3_name = "none"
            member3_cardinality = "none"
            member3_primary_key = "none"

            # relationship_dic['entity3'] = member3_name
            # relationship_dic['entity3_cardinality'] = member3_cardinality
            # relationship_dic['entity3_primary_key'] = member3_primary_key

        relationship_dic = {'id': i,
                            'name': rel.get('name'),
                            'type': rel.get('type'),
                            'degree': rel.get('degree'),
                            'entities': [
                                {
                                    'id': 1,
                                    'name': member1_name,
                                    'cardinality': member1_cardinality,
                                    'primaryKey': member1_primary_key
                                },
                                {
                                    'id': 2,
                                    'name': member2_name,
                                    'cardinality': member2_cardinality,
                                    'primaryKey': member2_primary_key
                                },
                                {
                                    'id': 3,
                                    'name': member3_name,
                                    'cardinality': member3_cardinality,
                                    'primaryKey': member3_primary_key
                                }
                            ]
                            }

        relationship_dic_list.append(relationship_dic)
        i = i + 1
    print(relationship_dic_list)
    return relationship_dic_list

# get_relationship_list()
