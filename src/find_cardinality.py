import re

import inflect
import nltk

from src.pre_process.common_nlp import lemmatizer, text_into_sentence
from src.identify_relationship import binary_relationship_dic_list, ternary_relationship_list, \
    unary_relationship_dic_list
from src.utils.file_manipulation import get_root_of_input_xml

one_to_one_relationship_list = []
one_to_many_relationship_list = []
many_to_many_relationship_list = []
binary_relation_list = []
ternary_relation_list = []
relation_list = []

p = inflect.engine()

print(ternary_relationship_list)


# remove the duplicate of binary relationship list
def remove_duplicate_of_relationship_list_binary():
    new_list = []
    for dic in binary_relationship_dic_list:

        member1 = dic.get('member1')
        member2 = dic.get('member2')
        lem_mem1 = lemmatizer.lemmatize(member1)
        lem_mem2 = lemmatizer.lemmatize(member2)
        index = binary_relationship_dic_list.index(dic)

        for new_dic in binary_relationship_dic_list:
            new_index = binary_relationship_dic_list.index(new_dic)
            if index == new_index:
                continue
            else:
                new_member1 = new_dic.get('member1')

                new_member2 = new_dic.get('member2')

                n_lem_mem1 = lemmatizer.lemmatize(new_member1)

                n_lem_mem2 = lemmatizer.lemmatize(new_member2)

                if (member1 == new_member1 and member2 == new_member2) or \
                        (member1 == n_lem_mem1 and member2 == n_lem_mem2) or \
                        (lem_mem1 == new_member1 and lem_mem2 == new_member2) or \
                        (member2 == new_member1 and member1 == new_member2) or \
                        (member2 == n_lem_mem1 and member1 == n_lem_mem2) or \
                        (lem_mem2 == new_member1 and lem_mem1 == new_member2) or (
                        lem_mem1 == new_member2 and member2 == n_lem_mem1):
                    tokenize_member1 = nltk.word_tokenize(member1)
                    tag_member1 = nltk.pos_tag(tokenize_member1)
                    tokenize_member2 = nltk.word_tokenize(member2)
                    tag_member2 = nltk.pos_tag(tokenize_member2)
                    new_tokenize_member1 = nltk.word_tokenize(new_member1)
                    new_tag_member1 = nltk.pos_tag(new_tokenize_member1)
                    new_tokenize_member2 = nltk.word_tokenize(new_member2)
                    new_tag_member2 = nltk.pos_tag(new_tokenize_member2)

                    if tag_member1[0][1] == 'NNS' or tag_member2[0][1] == 'NNS':
                        binary_relationship_dic_list.remove(new_dic)
                    elif new_tag_member1[0][1] == 'NNS' or new_tag_member2[0][1] == 'NNS':
                        binary_relationship_dic_list.remove(dic)
                    else:
                        binary_relationship_dic_list.remove(dic)

    # print(relationship_dic_list)
    return binary_relationship_dic_list


# find sentences match with particular binary entity list
def get_sentences_match_with_entities_binary(member1, member2, relationship):
    matching_sentences_list = []
    sentence_list = text_into_sentence()

    lem_member1 = lemmatizer.lemmatize(member1)
    lem_member2 = lemmatizer.lemmatize(member2)
    new_relationship_list = relationship.split('_')
    if len(new_relationship_list) > 1:
        correct_relationship = new_relationship_list[1]
    else:
        correct_relationship = new_relationship_list[0]

    relationship_lem = lemmatizer.lemmatize(correct_relationship, pos="v")

    # regular expressions for find relevant sentences
    regex_1 = r"" + re.escape(member1) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(member2)
    regex_2 = r"" + re.escape(member1) + "(.*)" + re.escape(relationship_lem) + "(.*)" + re.escape(member2)
    regex_3 = r"" + re.escape(lem_member1) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(member2)
    regex_4 = r"" + re.escape(lem_member1) + "(.*)" + re.escape(relationship_lem) + "(.*)" + re.escape(member2)
    regex_5 = r"" + re.escape(lem_member1) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(lem_member2)
    regex_6 = r"" + re.escape(member2) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(member1)
    regex_7 = r"" + re.escape(member2) + "(.*)" + re.escape(relationship_lem) + "(.*)" + re.escape(member1)
    regex_8 = r"" + re.escape(lem_member2) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(member1)
    regex_9 = r"" + re.escape(lem_member2) + "(.*)" + re.escape(relationship_lem) + "(.*)" + re.escape(member1)
    regex_10 = r"" + re.escape(lem_member2) + "(.*)" + re.escape(correct_relationship) + "(.*)" + re.escape(lem_member1)

    for sentence in sentence_list:
        if re.search(regex_1, sentence, re.MULTILINE | re.IGNORECASE) or re.search(regex_2, sentence,
                                                                                   re.MULTILINE | re.IGNORECASE) or re.search(
            regex_3, sentence, re.MULTILINE | re.IGNORECASE) or re.search(regex_4, sentence,
                                                                          re.MULTILINE | re.IGNORECASE) or re.search(
            regex_5, sentence, re.MULTILINE | re.IGNORECASE) \
                or re.search(regex_6, sentence, re.MULTILINE | re.IGNORECASE) or re.search(regex_7, sentence,
                                                                                           re.MULTILINE | re.IGNORECASE) or re.search(
            regex_8, sentence, re.MULTILINE | re.IGNORECASE) or re.search(regex_9, sentence,
                                                                          re.MULTILINE | re.IGNORECASE) or re.search(
            regex_10, sentence, re.MULTILINE | re.IGNORECASE):
            print(sentence)
            matching_sentences_list.append(sentence)

    return matching_sentences_list


def get_nouns_list(sentence):
    pos_tag_list = nltk.pos_tag(sentence)
    noun_list = []
    # print(pos_tag_list)
    for data in pos_tag_list:
        if data[1] == 'NN' or data[1] == 'NNS':
            noun_list.append(data[0])
    # print(noun_list)
    return noun_list


def find_primary_key(member):
    root = get_root_of_input_xml()
    lem_member = lemmatizer.lemmatize(member)
    for entity_ref in root.findall('entity'):
        entity = entity_ref.get('name')
        if entity == member or entity == lem_member:
            for attri_ref in entity_ref.findall('attribute'):
                if attri_ref.get('value') == "primary_key":
                    return attri_ref.get('name')


def get_binary_cardinality_list():
    new_relationship_dic_list_binary = remove_duplicate_of_relationship_list_binary()
    for dic in new_relationship_dic_list_binary:
        plural_member1 = dic.get('member1')
        # print(member1)

        plural_member2 = dic.get('member2')
        # print(member2)
        relationship = dic.get('relationship')
        # print(relationship)
        sentence_list = get_sentences_match_with_entities_binary(plural_member1, plural_member2, relationship)
        sentence_set = list(set(sentence_list))
        # print(sentence_set)
        member1_primary_key = find_primary_key(plural_member1)
        member2_primary_key = find_primary_key(plural_member2)
        # print(member1, " primary key is : ", member1_primary_key)
        # print(member2, " primary key is : ", member2_primary_key)

        singular_member1 = lemmatizer.lemmatize(plural_member1)
        singular_member2 = lemmatizer.lemmatize(plural_member2)

        if find_cardinality_many(plural_member1, sentence_set):

            if find_cardinality_many(plural_member2, sentence_set):

                binary_relation_list.append({"@name": relationship, "@degree": "binary", "@type": "many_to_many",
                                             "member1": {"@name": singular_member1, "@cardinality": "many",
                                                         "@primary_key": member1_primary_key},
                                             "member2": {"@name": singular_member2, "@cardinality": "many",
                                                         "@primary_key": member2_primary_key}})
            elif find_cardinality_one(plural_member2, sentence_set, relationship):
                binary_relation_list.append(
                    {"@name": relationship, "@degree": "binary", "@type": "one_to_many",
                     "member1": {"@name": singular_member1, "@cardinality": "many",
                                 "@primary_key": member1_primary_key},
                     "member2": {"@name": singular_member2, "@cardinality": "one",
                                 "@primary_key": member2_primary_key}})
        elif find_cardinality_one(plural_member1, sentence_set, relationship):
            if find_cardinality_many(plural_member2, sentence_set):
                singular_member1 = lemmatizer.lemmatize(plural_member1)
                singular_member2 = lemmatizer.lemmatize(plural_member2)
                binary_relation_list.append(
                    {"@name": relationship, "@degree": "binary", "@type": "one_to_many",
                     "member1": {"@name": singular_member1, "@cardinality": "one", "@primary_key": member1_primary_key},
                     "member2": {"@name": singular_member2, "@cardinality": "many",
                                 "@primary_key": member2_primary_key}})
            elif find_cardinality_one(plural_member2, sentence_set, relationship):
                binary_relation_list.append(
                    {"@name": relationship, "@degree": "binary", "@type": "one_to_one",
                     "member1": {"@name": singular_member1, "@cardinality": "one", "@primary_key": member1_primary_key},
                     "member2": {"@name": singular_member2, "@cardinality": "one",
                                 "@primary_key": member2_primary_key}})

        #     ...............................

        if find_cardinality_many(plural_member1, sentence_set):
            if find_cardinality_many(plural_member2, sentence_set):
                many_to_many_relationship_list.append(
                    {'member1': plural_member1, 'member2': plural_member2, 'relationship': relationship})
            elif find_cardinality_one(plural_member2, sentence_set, relationship):
                one_to_many_relationship_list.append(
                    {'member1': plural_member1, 'member2': plural_member2, 'relationship': relationship})
        elif find_cardinality_one(plural_member1, sentence_set, relationship):
            if find_cardinality_many(plural_member2, sentence_set):
                one_to_many_relationship_list.append(
                    {'member1': plural_member1, 'member2': plural_member2, 'relationship': relationship})
            elif find_cardinality_one(plural_member2, sentence_set, relationship):
                one_to_one_relationship_list.append(
                    {'member1': plural_member1, 'member2': plural_member2, 'relationship': relationship})

    # print("1 2 1", one_to_one_relationship_list)
    # print("1 2 M", one_to_many_relationship_list)
    # print("M 2 M", many_to_many_relationship_list)
    print("rel", binary_relation_list)
    return binary_relation_list


def get_sentences_match_with_entities_ternary(member1, member2, member3, relation):
    match_ternary_sentence_list = []
    # regular expressions for find ternary relationships exist sentences
    regex = r"(" + re.escape(member1) + "|" + re.escape(member2) + "|" + re.escape(member3) + ")" + "(.*)" + re.escape(
        relation) + "(.*)" + "(" + re.escape(member1) + "|" + re.escape(member2) + "|" + re.escape(
        member3) + ")" + "(.*)" + "(" + re.escape(member1) + "|" + re.escape(member2) + "|" + re.escape(member3) + ")"
    print(regex)
    sentence_list = text_into_sentence()
    for sentence in sentence_list:
        if re.search(regex, sentence, re.MULTILINE | re.IGNORECASE):
            match_ternary_sentence_list.append(sentence)
            print("*************", sentence)

    return match_ternary_sentence_list


def get_ternary_cardinality_list():
    for dic in ternary_relationship_list:
        member1 = dic.get('member1')
        member2 = dic.get('member2')
        member3 = dic.get('member3')
        relation = dic.get('relationship')

        sentence_list = get_sentences_match_with_entities_ternary(member1, member2, member3, relation)

        member1_primary_key = find_primary_key(member1)
        member2_primary_key = find_primary_key(member2)
        member3_primary_key = find_primary_key(member3)

        singular_member1 = lemmatizer.lemmatize(member1)
        singular_member2 = lemmatizer.lemmatize(member2)
        singular_member3 = lemmatizer.lemmatize(member3)

        if find_cardinality_many(member1, sentence_list):

            if find_cardinality_many(member2, sentence_list):

                if find_cardinality_many(member3, sentence_list):

                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "many_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "many",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "many",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "many",
                                     "@primary_key": member2_primary_key}}),
                elif find_cardinality_one(member3, sentence_list, relation):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "many",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "one",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "many",
                                     "@primary_key": member2_primary_key}}),
            elif find_cardinality_one(member2, sentence_list, relation):
                if find_cardinality_many(member3, sentence_list):

                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "many",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "many",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "one",
                                     "@primary_key": member2_primary_key}}),
                elif find_cardinality_one(member3, sentence_list, relation):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "many",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "one",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "one",
                                     "@primary_key": member2_primary_key}})

        elif find_cardinality_one(member1, sentence_list, relation):
            if find_cardinality_many(member2, sentence_list):
                if find_cardinality_many(member3, sentence_list):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "one",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "many",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "many",
                                     "@primary_key": member2_primary_key}}),
                elif find_cardinality_one(member3, sentence_list, relation):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "one",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "one",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "many",
                                     "@primary_key": member2_primary_key}})
            elif find_cardinality_one(member2, sentence_list, relation):
                if find_cardinality_many(member3, sentence_list):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_many",
                         "member1": {"@name": singular_member1, "@cardinality": "one",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "many",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "one",
                                     "@primary_key": member2_primary_key}}),
                elif find_cardinality_one(member3, sentence_list, relation):
                    ternary_relation_list.append(
                        {"@name": relation, "@degree": "ternary", "@type": "one_to_one",
                         "member1": {"@name": singular_member1, "@cardinality": "one",
                                     "@primary_key": member1_primary_key},
                         "member3": {"@name": singular_member3, "@cardinality": "one",
                                     "@primary_key": member3_primary_key},
                         "member2": {"@name": singular_member2, "@cardinality": "one",
                                     "@primary_key": member2_primary_key}})
    return ternary_relation_list


def get_unary_cardinality_list():
    unary_cardinality_list = []
    for dic in unary_relationship_dic_list:
        relation = dic.get('relationship')
        plural_member = dic.get("member")
        member = lemmatizer.lemmatize(plural_member)
        primary_key = find_primary_key(member)
        unary_cardinality_list.append({"@name": relation, "@degree": "unary", "@type": "one_to_one",
                                       "member1": {"@name": member, "@cardinality": "one",
                                                   "@primary_key": primary_key},
                                       "member2": {"@name": member, "@cardinality": "one",
                                                   "@primary_key": primary_key}})
    print(unary_cardinality_list)
    return unary_cardinality_list


def find_cardinality():
    binary_cardinality_list = get_binary_cardinality_list()
    ternary_cardinality_list = get_ternary_cardinality_list()
    unary_cardinality_list = get_unary_cardinality_list()

    print("### Binary ###", binary_cardinality_list)
    print("### Ternary ####", ternary_cardinality_list)
    print("### Unary ####", unary_cardinality_list)

    relation_list = binary_cardinality_list + ternary_cardinality_list + unary_cardinality_list

    print(relation_list)

    return relation_list


def find_cardinality_one(member, sentence_list, relationship):
    value = False
    # regular expressions for find cardinality one
    RE_4_1 = r'.*((only|exactly) one|uniquely|no.* more than one)(.*)' + re.escape(member)

    for line in sentence_list:
        for match in re.finditer(RE_4_1, line):
            value = True

            return value
    if not value:
        tokenize_member = nltk.word_tokenize(member)
        tag_member = nltk.pos_tag(tokenize_member)

        if tag_member[0][1] == 'NN':
            value = True

            return value
    if not value:
        value = is_singular_verb(relationship)

        if value:
            value = True
            return value


def is_singular_verb(relationship):
    new_relationship_list = relationship.split('_')

    if len(new_relationship_list) > 1:
        correct_relationship = new_relationship_list[1]
    else:
        correct_relationship = new_relationship_list[0]

    relationship_tok = nltk.word_tokenize(correct_relationship)
    tag_relationship = nltk.pos_tag(relationship_tok)

    if tag_relationship[0][1] == 'VBZ' or 'NNS':
        return True
    elif tag_relationship[0][1] == 'VBN':
        if new_relationship_list[0] == 'is':
            return True
    else:
        return False


def find_cardinality_many(member, sentence_list):
    value = False
    # regular expressions for find cardinality many
    RE_4_M = r".*(\bmore than one\b|\bmany\b|\bany\b|\bone or more\b|\bseveral\b|\bnumber of\b|\bat least one\b|\bmultiple\b|(\btwo\b|\bthree\b|\bfour\b|\bfive\b) \btype of\b).*" + re.escape(
        member)
    # for i, line in enumerate(open('data\\input2_text.txt')):
    for line in sentence_list:
        for match in re.finditer(RE_4_M, line):
            # print('Many : Found on line %s: %s' % (i + 1, match.group()))
            value = True
            # print(value)
            return value
    if not value:
        tokenize_member = nltk.word_tokenize(member)
        tag_member = nltk.pos_tag(tokenize_member)

        if tag_member[0][1] == 'NNS':
            value = True

            return value

        return value

# find_cardinality()
