import re
import nltk
import inflect
from pattern.en import pluralize, singularize

from src.attributes import clear_attribute_list

p = inflect.engine()
dict_entities={}

def findAttributes(scenario,new_entity_list):
    scenario = scenario.lower()
    sent_list = nltk.sent_tokenize(scenario)
    for entity in new_entity_list:
        attributeList = {}
        sigularEntity=entity
        pluralEntity=pluralize(entity)
        for sentence in sent_list:
            regex_1 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (.*) (has|have) (.*)(,) and (.*)."
            regex_2 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (is|are) identified by (.*) must be recorded."
            regex_3 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+"), (.*) must be recorded."
            regex_4 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (.*) (has|have) (.*)."
            regex_5 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+"), (.*) and (.*) must be recorded."
            regex_6 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (has|have) (.*)."
            regex_7 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+")'s (.* \(.*\)), (.*), and (.*)."
            regex_8 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+"), (.*) has (.*)."
            regex_9 = r"each ("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+")'s (.*) and (\w+)"
            regex_10 = r"(.*) of the ("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+")"
            regex_11 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (can be|are) characterized by (.*) and (.*)."
            regex_12 = r"(.*) \(e.g,(.*)\)"
            regex_13 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (is|are) identified by (.*) and has a (.*)."
            regex_14 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") has (a|an) (.*) and (.*)."
            regex_15 = r"(.*) for each ("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+")"

            regexPk_1 = r"(unique|uniquely) (.*)"
            regexPk_2 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (is|are) identified by (.*)."
            regexPk_3 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+"), which (is|are) identified by (.*)."
            regexPk_4 =  r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (is|are) identified (.*) by (.*) (when|which|what|that) "
            regexPk_5 = r"(.*) \((unique|uniquely|uncommon|specialized)\)"

            regexCo_1 = r"(.*) (\((.*)\))"
            regexCo_2 = r" ([a-z]*) ([(])(.*,.*)([)])"

            regexMv_1 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (.*) (have|has) several (\w+)"
            regexMv_2 = r"("+re.escape(sigularEntity)+"|"+re.escape(pluralEntity)+") (have|has) (.*) one or more (.*)"
            regexMv_3 = r"(" + re.escape(sigularEntity) + "|" + re.escape(pluralEntity) + ") (has|have) (.*) multiple (.*)"

            if re.search(regex_1, sentence):
                matches = re.finditer(regex_1, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum==6:
                            word=match.group(groupNum).split()
                            attributeList[word[-1]]="none"

            if re.search(regex_1, sentence):
                matches = re.finditer(regex_1, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum==4:
                            splitGroup=match.group(groupNum).split(", ")
                            for w in splitGroup:
                                if re.search(regexPk_1, w):
                                    matches=re.finditer(regexPk_1,w,re.MULTILINE | re.IGNORECASE)
                                    for matchNum,match in enumerate(matches, start=1):
                                        for groupNum1 in range(0, len(match.groups())):
                                            groupNum1 = groupNum1 +1
                                            if groupNum1==2:
                                                word = w.split()
                                                attributeList[word[-1]]="pk"
                                else:
                                    word=w.split()
                                    attributeList[word[-1]]="none"

            if re.search(regex_2, sentence):
                matches = re.finditer(regex_2, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word = w.split()
                                if w==splitGroup[0]:
                                    attributeList[word[-1]]="pk"
                                else:
                                    attributeList[word[-1]]="none"

            if re.search(regexPk_2, sentence):
                matches = re.finditer(regexPk_2, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split()
                            attributeList[splitGroup[-1]]="pk"

            if re.search(regex_3, sentence):
                matches = re.finditer(regex_3, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 2:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word=w.split()
                                attributeList[word[-1]]="none"

            if re.search(regex_4, sentence):
                matches = re.finditer(regex_4, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word=w.split()
                                attributeList[word[-1]]="none"

            if re.search(regex_5, sentence):
                matches = re.finditer(regex_5, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 2:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word=w.split()
                                attributeList[word[-1]]="none"
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split()
                            attributeList[splitGroup[-1]] = "none"

            if re.search(regex_6, sentence):
                matches = re.finditer(regex_6, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word = w.split()
                                attributeList[word[-1]] = "none"
            if re.search(regex_7, sentence):
                matches = re.finditer(regex_7, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 2:
                            if re.search(regexCo_1, sentence):
                                matches = re.finditer(regexCo_1, sentence, re.MULTILINE | re.IGNORECASE)
                                for matchNum, match in enumerate(matches, start=1):
                                    compositeP = ""
                                    compositeC = []
                                    for groupNum1 in range(0, len(match.groups())):
                                        groupNum1 = groupNum1 + 1
                                        if groupNum1==1:
                                            compositeP=match.group(groupNum1).split()[-1]
                                        if groupNum1==3:
                                            compositeC=match.group(groupNum1).split(", ")
                                    attributeList[compositeP] = compositeC

            if re.search(regex_7, sentence):
                matches = re.finditer(regex_7, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word = w.split()
                                attributeList[word[-1]] = "none"

            if re.search(regex_7, sentence):
                matches = re.finditer(regex_7, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            word = match.group(groupNum).split()
                            attributeList[word[-1]] = "none"

            if re.search(regex_8, sentence):
                matches = re.finditer(regex_8, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                if re.search(regexPk_1, w):
                                    matches = re.finditer(regexPk_1, w, re.MULTILINE | re.IGNORECASE)
                                    for matchNum, match in enumerate(matches, start=1):
                                        for groupNum in range(0, len(match.groups())):
                                            word = w.split()
                                            attributeList[word[-1]] = "pk"
                                else:
                                    word = w.split()
                                    attributeList[word[-1]]="none"

            if re.search(regex_9, sentence):
                matches = re.finditer(regex_9, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 2:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word = w.split()
                                attributeList[word[-1]] = "none"
                        if groupNum == 3:
                            attributeList[match.group(groupNum)] = "none"

            if re.search(regexMv_1, sentence):
                matches = re.finditer(regexMv_1, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            attributeList[match.group(groupNum)] = "mv"

            if re.search(regexPk_3, sentence):
                matches = re.finditer(regexPk_3, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            word = match.group(groupNum).split()
                            attributeList[word[-1]] = "pk"

            if re.search(regex_10, sentence):
                matches = re.finditer(regex_10, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 1:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                word=w.split(" and ")
                                for x in word:
                                    attributeList[x.split()[0]]="none"

            if re.search(regexPk_4, sentence):
                matches = re.finditer(regexPk_4, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            word = match.group(groupNum).split()
                            attributeList[word[-1]] = "pk"

            if re.search(regex_11, sentence):
                matches = re.finditer(regex_11, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup = match.group(groupNum).split(", ")
                            for w in splitGroup:
                                if re.search(regexPk_5, w):
                                    matches = re.finditer(regexPk_5, w, re.MULTILINE | re.IGNORECASE)
                                    for matchNum, match in enumerate(matches, start=1):
                                        for groupNum1 in range(0, len(match.groups())):
                                            groupNum1 = groupNum1 + 1
                                            if groupNum1 == 1:
                                                attributeList[match.group(groupNum1).split()[-1]]="pk"
                                elif re.search(regex_12, w):
                                    matches = re.finditer(regex_12, w, re.MULTILINE | re.IGNORECASE)
                                    for matchNum, match in enumerate(matches, start=1):
                                        for groupNum1 in range(0, len(match.groups())):
                                            groupNum1 = groupNum1 + 1
                                            if groupNum1 == 1:
                                                attributeList[match.group(groupNum1).split()[-1]]="none"
                                else:
                                    attributeList[w.split()[-1]]="none"

            if re.search(regex_11, sentence):
                matches = re.finditer(regex_11, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            word = match.group(groupNum).split()
                            attributeList[word[-1]]="none"

            if re.search(regex_13, sentence):
                matches = re.finditer(regex_13, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            if re.search(regex_12, match.group(groupNum)):
                                matches = re.finditer(regex_12, w, re.MULTILINE | re.IGNORECASE)
                                for matchNum, match in enumerate(matches, start=1):
                                    for groupNum1 in range(0, len(match.groups())):
                                        groupNum1 = groupNum1 + 1
                                        if groupNum1 == 1:
                                            attributeList[match.group(groupNum1).split()[-1]]="pk"

            if re.search(regex_13, sentence):
                matches = re.finditer(regex_13, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            word = match.group(groupNum).split(" and ")
                            for w in word:
                                attributeList[w.split()[-1]]="none"

            if re.search(regex_14, sentence):
                matches = re.finditer(regex_14, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 3:
                            splitGroup=match.group(groupNum).split(", ")
                            for x in splitGroup:
                                if re.search(regexPk_1, x):
                                    matches = re.finditer(regexPk_1, x, re.MULTILINE | re.IGNORECASE)
                                    for matchNum, match in enumerate(matches, start=1):
                                        for groupNum in range(0, len(match.groups())):
                                            groupNum = groupNum + 1
                                            if groupNum==2:
                                                word = x.split()
                                                attributeList[word[-1]] = "pk"
                                else:
                                    word = x.split()
                                    attributeList[word[-1]] = "none"

            if re.search(regex_14, sentence):
                matches = re.finditer(regex_14, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            splitGroup=match.group(groupNum).split(", ")
                            for x in splitGroup:
                                if re.search(regexPk_1, x):
                                    matches = re.finditer(regexPk_1, x, re.MULTILINE | re.IGNORECASE)
                                    for matchNum, match in enumerate(matches, start=1):
                                        for groupNum in range(0, len(match.groups())):
                                            groupNum = groupNum + 1
                                            if groupNum==2:
                                                word = x.split()
                                                attributeList[word[-1]] = "pk"
                                else:
                                    word = x.split()
                                    attributeList[word[-1]] = "none"

            if re.search(regexMv_2, sentence):
                matches = re.finditer(regexMv_2, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            splitGroup=match.group(groupNum).split()
                            attributeList[splitGroup[-1]] = "mv"

            if re.search(regexMv_3, sentence):
                matches = re.finditer(regexMv_3, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 4:
                            splitGroup=match.group(groupNum).split()
                            attributeList[splitGroup[-1]] = "mv"

            if re.search(regex_15, sentence):
                matches = re.finditer(regex_15, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 1:
                            splitGroup=match.group(groupNum).split()
                            attributeList[splitGroup[-1]] = "none"
        finalattributelist=clear_attribute_list.clearAttributelist(attributeList)
        dict_entities[entity]=finalattributelist
    attribute_entity_dic = clear_attribute_list.clearlist(dict_entities)
    return attribute_entity_dic

#scenario="We store employee's name (First Name, Middle Initials, Last Name), employee's number, address, salary, gender, and date of birth."
#new_entity_list=['company', 'department', 'employee', 'project', 'dependent']
#findAttributes(scenario,new_entity_list)