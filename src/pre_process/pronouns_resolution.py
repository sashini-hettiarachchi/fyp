import spacy

nlp = spacy.load('en_core_web_sm')
import neuralcoref
from src.utils.file_manipulation import input_text, PATH


# neuralcoref.add_to_pipe(nlp,greedyness=0.52)
# doc = nlp("Students enroll courses. They follow some lectures. ")
# print(doc._.coref_resolved)


def pronouns_resolution():
    x = neuralcoref.add_to_pipe(nlp, greedyness=0.52)
    print(x)
    doc = nlp(input_text)
    pronouns_resolution_text = (doc._.coref_resolved)
    # print("This is the pronoun resolution text")
    # print(pronouns_resolution_text)

    with open(PATH + '\\intermediate_text.txt', "w+") as my_output_file:
        my_output_file.write(pronouns_resolution_text)
    return pronouns_resolution_text

# pronouns_resolution()
