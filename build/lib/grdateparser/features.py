ACTION_REFERNECE  = {'this': 0, 'present': 0, 'current': 0 , 'active': 0,
                   'last' : -1, 'previous' : -1, 'before': -1,
                   'next' : 1, 'upcoming' : 1, 'after' : 1, 'future': 1 , 'new' : 1, 'old' : -1,
                    'newer': 1, 'older': -1, 'ago': -1, 'past': -1
                   }

NAMES_OF_DAYS     = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
NAMES_OF_MONTHS   = ['jan', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
WORDS_REF_DAYS    = ['today', 'tomorrow', 'yesterday']
QUARTER_NO_WORDS  = ['q1', 'q2', 'q3', 'q4']
DAY_WORDS         = ['day', 'days']
WEEK_WORDS        = ['week', 'weeks']
MONTH_WORDS       = ['month', 'months']
QUARTER_WORDS     = ['quarter', 'quarters']
YEAR_WORDS        = ['year', 'years']
WORD_MIDDLERS     = ['between', 'from', 'to', 'and', 'in', 'upto']

from .textutility import Tokenize, Replacers, POSTagger
import pickle
import os
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "data", "DATE_WORDS.p")
DATE_WORDS = pickle.load(open(DATA_PATH,"rb"))

#print(DATE_WORDS)

def is_monthname(word):
    return True if word in NAMES_OF_MONTHS else False

def is_dayname(word):
    return True if word in NAMES_OF_DAYS else False

def is_actionref(word):
    return True if word in ACTION_REFERNECE else False

def is_wordref(word):
    return True if word in WORDS_REF_DAYS else False

def is_quarter_no_words(word):
    return True if word in QUARTER_NO_WORDS else False

def is_word_middlers(word):
    return True if word in WORD_MIDDLERS else False

def is_unknown_word(word):
    return False if word in DATE_WORDS else True

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isdigit()': word.isdigit(),
        'word.ismonthname()': is_monthname(word),
        'word.isdayname()': is_dayname(word),
        'word.isactionref()': is_actionref(word),
        'word.is_quarter_no_words()': is_quarter_no_words(word),
        'word.is_word_middlers()': is_word_middlers(word),
        'word.is_unknown_word()': is_unknown_word(word),
        'word.is_wordref()': is_wordref(word),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]

class FeatureExtractor:
    def __init__(self, stext=""):
        if stext == "":
            raise "Empty text"

        self.TEXT = stext

    def cleanup(self):
        t = Tokenize(self.TEXT)
        r = Replacers()
        self.WORDS = []
        for w in t.words:
            temp = r.process(w)
            #print(temp)
            if isinstance(temp, list):
                self.WORDS.extend(temp)
            else:
                self.WORDS.append(temp)

    def tag(self):
        p = POSTagger(self.WORDS)
        self.TAGGED_WORDS = p.tag()

    def extract(self):
        self.cleanup()
        self.tag()
        self.features = [sent2features(self.TAGGED_WORDS)]
        return self.features