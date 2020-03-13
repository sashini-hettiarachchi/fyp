import random
import re
from time import sleep

import nltk

from src.pre_process.common_nlp import stopWords, text_into_sentence, sentences_into_word, lemmatizer
from src.utils.file_manipulation import get_root_of_input_xml

filtered_sentence_list = []
relationship_identified_sentence_list = []
sentence_list_has_entities = []
binary_relationship_dic_list = []
unary_relationship_dic_list = []
ternary_relationship_list = []

new_word_list = []

# regular expressions for verbs identify
regex_for_verb_tags = r"VB[GDPNZP]?"


# find the sentences which has entities_extractor
def find_entities(word):
    root = get_root_of_input_xml()
    for entity_ref in root.findall('entity'):
        entity = entity_ref.get('name')
        # print(entity)
        entity_singular = lemmatizer.lemmatize(entity)
        word_singular = lemmatizer.lemmatize(word)
        if word == entity or word == entity_singular or word_singular == entity_singular:
            return word


# entities_extractor and related sentence return
def entity_combined_with_scenario():
    sentences = text_into_sentence()
    sleep(10)
    for sentence in sentences:
        entity_list = []
        word_list = nltk.word_tokenize(sentence)
        # print(sentence)
        for word in word_list:
            word_new = find_entities(word)
            if word_new is not None:
                sentence_list_has_entities.append(sentence)
                entity_list.append(word_new)

        # Remove duplicates in entity list
        if len(entity_list) >= 2:
            sleep(10)
            duplicate_removed_entity_list = list(set(entity_list))
            if len(duplicate_removed_entity_list) >= 2:
                for entity in duplicate_removed_entity_list:
                    lem_entity = lemmatizer.lemmatize(entity)
                    new_list = duplicate_removed_entity_list[
                               duplicate_removed_entity_list.index(entity) + 1: len(entity_list)]
                    print(new_list)
                    for entity_1 in new_list:
                        lem_entity_1 = lemmatizer.lemmatize(entity_1)
                        if entity_1 == lem_entity:
                            duplicate_removed_entity_list.remove(lem_entity)
                            break
                        elif entity == lem_entity_1:
                            duplicate_removed_entity_list.remove(entity)
                            break
            # duplicate_removed_entity_list = list(set(entity_list))
            find_relationship(duplicate_removed_entity_list, sentence)
            print("+++++++++")


# find the relationships
def find_relationship(entity_list, sentence):
    global ternary_relationship_list
    word_list = sentences_into_word(sentence)
    pos_tag_list = nltk.pos_tag(word_list)
    entity_and_index_list = []
    # Identify Unary relationships
    if len(entity_list) == 1:
            member = lemmatizer.lemmatize(entity_list[0])
            # Eliminate entity names as attributes_extractor
            regex_for_unary_1 = r"(.*)(" + re.escape(member) + ")(.*,.*,.*)(" + re.escape(member) + ")(.*)"
            regex_for_unary_2 = r"(.*)(" + re.escape(member) + ")(.*)(" + re.escape(member) + ")(.*)(,)(.*)(,)(.*)"
            regex_for_unary_3 = r"(.*)(" + re.escape(member) + ")(.*)(identified)(.*)(" + re.escape(member) + ")(.*)"
            print("Unary", entity_list, "sentence", sentence)
            if (not (re.search(regex_for_unary_1, sentence))) and (
                    not (re.search(regex_for_unary_2, sentence)) and (not (re.search(regex_for_unary_3, sentence)))):
                relationship_list = []
                for word in pos_tag_list:
                    if re.search(regex_for_verb_tags, word[1]):
                        relationship_list.append(word[0])
                if len(relationship_list) > 1:
                    relationship = random.choice(relationship_list)
                else:
                    relationship = relationship_list[0]
                unary_relationship_dic_list.append({"member": member, "relationship": relationship, "sentence": sentence})
                print("Unary Relationship List", unary_relationship_dic_list)
        # Identify Ternary Relationships
    elif len(entity_list) == 3:
        member1 = entity_list[0]
        member2 = entity_list[1]
        member3 = entity_list[2]

        regex_for_ternary_sentence_elimination = r"(.*)(" + re.escape(member1) + "|" + re.escape(
            member2) + "|" + re.escape(member3) + ".*)(,)(.*" + re.escape(member1) + "|" + re.escape(
            member2) + "|" + re.escape(member3) + ".*)(,)(.*)(" + re.escape(member1) + "|" + re.escape(
            member2) + "|" + re.escape(member3) + ")"

        if not (re.search(regex_for_ternary_sentence_elimination, sentence)):
            # find related sentences
            regex_3_for_identify_related_sentence_part = r"(" + re.escape(member1) + "|" + re.escape(
                member2) + "|" + re.escape(member3) + ")" + "(.*)" + "(" + re.escape(
                member1) + "|" + re.escape(member2) + "|" + re.escape(member3) + ")"
            matches = re.finditer(regex_3_for_identify_related_sentence_part, sentence,
                                  re.MULTILINE | re.IGNORECASE)
            verb_list = []
            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    print(match.group(2))

                    relationship_content_sentence_part = match.group(2)
                    word_list_1 = sentences_into_word(relationship_content_sentence_part)
                    pos_tag_list_1 = nltk.pos_tag(word_list_1)
                    print(pos_tag_list_1)
                    for word in pos_tag_list_1:
                        if re.search(regex_for_verb_tags, word[1]):
                            verb_list.append(word[0])

            # print(verb_list)
            verb_set = set(verb_list)
            without_duplicate_verb_list = list(verb_set)
            if len(without_duplicate_verb_list) > 1:
                for verb in without_duplicate_verb_list:
                    if verb == 'is' or verb == 'has' or verb == 'are' or verb == 'have':
                        without_duplicate_verb_list.remove(verb)
                # print(without_duplicate_verb_list)
                ternary_relationship = random.choice(without_duplicate_verb_list)
                # print(ternary_relationship)
                relationship_dic_1 = {'member1': member1,
                                      'relationship': ternary_relationship,
                                      'member2': member2,
                                      'member3': member3}
                ternary_relationship_list.append(relationship_dic_1)
            elif len(without_duplicate_verb_list) == 1:
                ternary_relationship = verb_list[0]
                relationship_dic_1 = {'member1': member1,
                                      'relationship': ternary_relationship,
                                      'member2': member2,
                                      'member3': member3}
                ternary_relationship_list.append(relationship_dic_1)
            else:
                for word in pos_tag_list:
                    if re.search(regex_for_verb_tags, word[1]):
                        verb_list.append(word[0])
                if len(verb_list) > 1:
                    ternary_relationship = random.choice(verb_list)
                elif len(verb_list) == 1:
                    ternary_relationship = verb_list[0]
                else:
                    ternary_relationship = "relate"
                relationship_dic_1 = {'member1': member1,
                                      'relationship': ternary_relationship,
                                      'member2': member2,
                                      'member3': member3}
                ternary_relationship_list.append(relationship_dic_1)
    else:
        for data in pos_tag_list:
            for entity in entity_list:
                if data[0] == entity or data[0] == lemmatizer.lemmatize(entity):
                    index = pos_tag_list.index(data)

                    entity_and_index_list.append({'member': entity, 'index': index})

                    if len(entity_and_index_list) == 2:
                        first_index = entity_and_index_list[0].get('index')
                        second_index = entity_and_index_list[1].get('index') + 1
                        first_member = entity_and_index_list[0].get('member')
                        second_member = entity_and_index_list[1].get('member')

                        regex_1_identify_entities = r"" + re.escape(first_member) + " (of each) " + re.escape(
                            second_member)
                        regex_2_identify_entities = r"" + re.escape(second_member) + " (of each) " + re.escape(
                            first_member)

                        temp_list = pos_tag_list[first_index: second_index]
                        relationship_list = []
                        count = 0
                        for data in temp_list:

                            if re.search(regex_for_verb_tags, data[1]):
                                relationship_list.append(data[0])
                                count = count + 1

                                if count < 2:
                                    relationship_identified_sentence_list.append(sentence)

                        if relationship_list:
                            if len(relationship_list) > 1:
                                relationship = relationship_list[0] + '_' + relationship_list[1]
                            else:
                                relationship = relationship_list[0]

                            member1 = entity_and_index_list[1].get('member')
                            member2 = entity_and_index_list[0].get('member')

                            relationship_dic = {'member1': member1,
                                                'relationship': relationship,
                                                'member2': member2}
                            binary_relationship_dic_list.append(relationship_dic)

                        elif re.search(regex_1_identify_entities, sentence, re.MULTILINE | re.IGNORECASE) or re.search(
                                regex_2_identify_entities, sentence,
                                re.MULTILINE | re.IGNORECASE):

                            member1 = entity_and_index_list[1].get('member')
                            member2 = entity_and_index_list[0].get('member')

                            relationship_dic = {'member1': member1,
                                                'relationship': "related_with",
                                                'member2': member2}
                            binary_relationship_dic_list.append(relationship_dic)

        print("Binary", binary_relationship_dic_list)
        print("Ternary", ternary_relationship_list)
        print("Unary", unary_relationship_dic_list)
        return binary_relationship_dic_list, ternary_relationship_list, unary_relationship_dic_list


def removing_stopwords(words):
    for w in words:
        if w not in stopWords:
            filtered_sentence_list.append(w)
            return filtered_sentence_list


def find_attributes():
    root = get_root_of_input_xml()
    for child in root:
        temp_root = child
        if temp_root.get('name') == 'driver':
            for tempChild in temp_root:
                print(tempChild.attrib.get('name'))

# entity_combined_with_scenario()
# find_relationship()
