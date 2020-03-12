import nltk
primaryKeyWord=["no","number","ssn"]

def clearlist(attribute_dic):
    noAttributeEntities=0
    for e in attribute_dic:
        if len(attribute_dic[e])==0:
            noAttributeEntities=noAttributeEntities+1
    if noAttributeEntities>0 :
        for x in range(0, noAttributeEntities):
            for e in attribute_dic:
                if len(attribute_dic[e]) == 0:
                    del attribute_dic[e]
                    break
    return attribute_dic

def clearAttributelist(attribute_dic):
    attributelist = []
    valuelist = []
    newattributedic={}
    for a in attribute_dic:
        attributelist.append(a)
        valuelist.append(attribute_dic[a])
    for x in range(len(attributelist)):
        word=nltk.pos_tag(nltk.word_tokenize(attributelist[x]))
    if len(attribute_dic)>0:
        if valuelist.count("pk")==0:
            for w in primaryKeyWord:
                if w in attributelist:
                    valuelist[attributelist.index(w)]="pk"
                else:
                    attributelist.append("number")
                    valuelist.append("pk")
        if valuelist.count("pk")>0:
            count=valuelist.count("pk")
            for x in range(count-1):
                valuelist[valuelist.index("pk")]="none"
    for x in range(len(attributelist)):
        newattributedic[attributelist[x]]=valuelist[x]
    return newattributedic
