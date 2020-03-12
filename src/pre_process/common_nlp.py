import nltk
from nltk.corpus import stopwords
# from utils.file_manipulation import input_text
from src.pre_process import pronouns_resolution
import os.path
from src.utils import file_manipulation
from src.utils.file_manipulation import PATH

stopWords = set(stopwords.words('english'))
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.PorterStemmer()

def get_intermediate_text():
    # if os.path.isfile(file_manipulation.PATH+'\\intermediate_text.txt'):
    if os.path.exists(PATH + "\\intermediate_text.txt"):
        # os.remove(PATH + "\\intermediate_text.txt")
        # print('intermediate_text.txt does not exit')
        # intermediate_text = pronouns_resolution.pronouns_resolution()
        f = open(file_manipulation.PATH + "//intermediate_text.txt", "r")
        if f.mode == 'r':
            intermediate_text = f.read()
            print("inside the reading test@@@@@@@@@@@@@@", intermediate_text)
            return intermediate_text
        # return intermediate_text
    else:
        print('%%%%%%5gjjv%%%%%')
        intermediate_text = pronouns_resolution.pronouns_resolution()
        return intermediate_text




def text_into_sentence():
    new_input_text = get_intermediate_text()
    nltk.sent_tokenize(new_input_text)
    print("***************************")
    print(new_input_text)
    return nltk.sent_tokenize(new_input_text)


def sentences_into_word(sentence):
    word = nltk.word_tokenize(sentence)
    return word
