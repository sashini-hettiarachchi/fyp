import re
from src.entities_extractor import entity
from src.attributes_extractor import attribute
from src.xml import xml_new

def convert_xml(finaloutput_dic):
    dict = finaloutput_dic
    er_dic = {}
    er_dic["@name"] = "ER_name"
    entity_list = []
    for e in dict:
        entity_dic = {}
        entity_dic["@name"] = e
        attribute_list = []
        for a in dict[e]:
            attribute_dic = {}
            if dict[e][a] == "pk":
                attribute_dic["@name"] = a
                attribute_dic["@value"] = "primary_key"
            elif dict[e][a] == "mv":
                attribute_dic["@name"] = a
                attribute_dic["@value"] = "multi-valued"
            elif dict[e][a] == "none":
                attribute_dic["@name"] = a
            else:
                attribute_dic["@name"] = a
                attribute_dic["@type"] = "composite_parent"
                childlist = re.findall(r"'(\w+)", dict[e][a])
                composite_attribute_list = []
                for c in childlist:
                    child = {}
                    child["@name"] = c
                    child["@type"] = "composite_child"
                    composite_attribute_list.append(child)
                attribute_dic["attribute"] = composite_attribute_list
            attribute_list.append(attribute_dic)
        entity_dic["attribute"] = attribute_list
        entity_list.append(entity_dic)
    er_dic["entity"] = entity_list
    xml_dic = {}
    xml_dic["er"] = er_dic
    return xml_dic

def intermediateLayer1(scenario):
    entitylist=entity.findEntities(scenario)
    return entitylist

def intermediateLayer2(scenario,entitylist):
    entity = entitylist.split(", ")
    regex = r"'(\w+)'"
    newentitylist=[]
    for e in entity:
        if re.search(regex, e):
            matches = re.finditer(regex, e, re.MULTILINE | re.IGNORECASE)
            for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum==1:
                            newentitylist.append(match.group(groupNum))

    attribute_dic = attribute.findAttributes(scenario, newentitylist)
    return attribute_dic

def intermediateLayer3(finallist):
    finaloutput_dic={}
    entity_list = finallist.split("}")
    for x in range(len(entity_list)-1):
        attribute_dic={}
        intermediate=entity_list[x].split("\t: ")
        entity=re.findall(r'\w+', intermediate[0])[0]
        regex1 = r"'(\w+)': "
        regex2 = r": ((\[(.*)\])|'(\w+)')"
        attributename = re.findall(regex1, intermediate[1], re.MULTILINE | re.IGNORECASE)
        attributetype = []
        matches2 = re.findall(regex2, intermediate[1], re.MULTILINE | re.IGNORECASE)
        for m in matches2:
            if m[2] is not "":
                attributetype.append(m[1])
            else:
                attributetype.append(m[3])
        for i in range(len(attributename)):
            attribute_dic[attributename[i]]=attributetype[i]
        finaloutput_dic[entity]=attribute_dic
    print(finaloutput_dic)
    xml_new.create_xml(convert_xml(finaloutput_dic))
    return finaloutput_dic



dict = {'department': {'name': 'none', 'number': 'none', 'department': 'none', 'location': 'pk'}, 'employee': {'name': "['first name', 'middle initials', 'last name']", 'number': 'pk', 'address': 'none', 'salary': 'none', 'gender': 'none', 'birth': 'none'}, 'project': {'name': 'none', 'number': 'pk', 'location': 'none'}, 'dependent': {'name': 'none', 'gender': 'none', 'birth': 'none', 'number': 'pk'}}
er_dic={}
er_dic["@name"]="ER_name"
entity_list=[]
for e in dict:
    entity_dic = {}
    entity_dic["@name"] = e
    attribute_list = []
    for a in dict[e]:
        attribute_dic = {}
        if dict[e][a]=="pk":
            attribute_dic["@name"]=a
            attribute_dic["@value"]="primary_key"
        elif dict[e][a]=="mv":
            attribute_dic["@name"] = a
            attribute_dic["@value"] = "multi-valued"
        elif dict[e][a]=="none":
            attribute_dic["@name"] = a
        else:
            attribute_dic["@name"]=a
            attribute_dic["@type"]="composite_parent"
            childlist = re.findall(r"'(\w+)", dict[e][a])
            composite_attribute_list=[]
            for c in childlist:
                child={}
                child["@name"]=c
                child["@type"]="composite_child"
                composite_attribute_list.append(child)
            attribute_dic["attribute"]=composite_attribute_list
            #print(attribute_dic)
        attribute_list.append(attribute_dic)
    #print(attribute_list)
    entity_dic["attribute"]=attribute_list
    #print(entity_dic)
    entity_list.append(entity_dic)
#print(entity_list)
er_dic["entity"]=entity_list
xml_dic={}
xml_dic["er"]=er_dic
print(xml_dic)