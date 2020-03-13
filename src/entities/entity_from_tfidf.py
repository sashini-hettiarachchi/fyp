import nltk
import inflect
from sklearn.feature_extraction.text import CountVectorizer
import re

visited = set()
p = inflect.engine()


entity_tf_idf_model = []
common_words=[]
singularNouns=[]

def convert_singular(attributeFilter):
    for i in attributeFilter:
        if p.singular_noun(i) is False:
            singularNouns.append(i)
        else:
            singularNouns.append(p.singular_noun(i))
    remove_duplicates(singularNouns)

def remove_duplicates(singularNouns):
    for a in singularNouns:
        if not a in visited:
            visited.add(a)
            entity_tf_idf_model.append(a)
    return entity_tf_idf_model

def tfidf(scenario):
    sentences = list()
    with scenario as file:
        for line in file:
            for l in re.split(r"\.\s|\?\s|\!\s|\n",line):
                if l:
                    sentences.append(l)
    cvec = CountVectorizer(stop_words='english', min_df=2, max_df=0.9, ngram_range=(0,1))
    sf = cvec.fit_transform(sentences)
    common_words = cvec.get_feature_names()
    convert_singular(common_words)