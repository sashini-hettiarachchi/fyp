import nltk
import inflect
import re


stopAttributes = ["no", "number", "date","code", "volume", "type", "name", "id", "address", "birth","s","'","location", "gender"]
stopWords = ["database", "information", "system", "record"]
visited = set()
p = inflect.engine()

input_text = None
simpleScenario = None
sent_list=[]
postxt=[]
wordsFilter = []
commonNouns = []
attributeFilter1 = []
attributeFilter2 = []
singularNouns = []
nouns=[]
output = []

def preprocess_data(scenario):
    simpleScenario=scenario.lower()
    sent_list=nltk.sent_tokenize(simpleScenario)
    words=nltk.word_tokenize(simpleScenario)
    postxt=nltk.pos_tag(words)
    for w in postxt:
        if w[0] not in stopWords:
            wordsFilter.append(w)

    for w in wordsFilter:
        if w[1] == "NN" or w[1] == "NNS":
            commonNouns.append(w[0])

    for w in commonNouns:
        if w not in stopAttributes:
            attributeFilter1.append(w)
    for attribute in attributeFilter1:
        for sentence in sent_list:
            regex1 = r"each "+re.escape(attribute)+" "
            regex2 = r""+re.escape(attribute)+" (are|is)"
            regex3 = r"each ("+re.escape(attribute)+")"
            regex4 = r"("+re.escape(attribute)+") (have|has) (.*)"
            regex5 = r"each (.*) ("+re.escape(attribute)+"),"
            if re.search(regex1, sentence):
                matches = re.finditer(regex1, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    e=match.group().split()
                    if not e in attributeFilter2:
                        attributeFilter2.append(e[1])
            if re.search(regex2, sentence):
                matches = re.finditer(regex2, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    e=match.group().split()
                    if not e in attributeFilter2:
                        attributeFilter2.append(e[0])
            if re.search(regex3, sentence):
                matches = re.finditer(regex3, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    e=match.group().split()
                    if not e in attributeFilter2:
                        attributeFilter2.append(e[1])
            if re.search(regex4, sentence):
                matches = re.finditer(regex4, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    e=match.group().split()
                    if not e in attributeFilter2:
                        attributeFilter2.append(e[0])
            if re.search(regex5, sentence):
                matches = re.finditer(regex5, sentence, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    e=match.group().split()
                    if not e in attributeFilter2:
                        attributeFilter2.append(e[2])

    outputfromhuristics = list(dict.fromkeys(attributeFilter2))
    tag=nltk.pos_tag(outputfromhuristics)

    for i in tag:
        if i[1] == "NNS":
            singularNouns.append((p.singular_noun(i[0]), i[1]))
        else:
            singularNouns.append(i)

    for i in singularNouns:
        if i[1]=="NN" or i[1]=="JJ" or i[1]=="NNS":
            nouns.append(i[0])

    output = list(dict.fromkeys(nouns))

    return output
