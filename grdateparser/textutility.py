import re
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
rex = RegexpTokenizer('\s+', gaps=True)

replacement_patterns = [
    (r'won\'t', 'would not'),
    (r'can\'t', 'cannot'),
    (r'ain\'t', 'are not'),
    (r'wasn\'t', 'was not'),
    (r'wouldn\'t', 'would not'),
    (r'shouldn\'t', 'should not'),
    (r'doesn\'t', 'does not'),
    (r'couldn\'t', 'could not'),
    (r'didn\'t', 'did not'),
    (r'isn\'t', 'is not'),
    (r'aren\'t', 'are not'),
    (r'haven\'t', 'was not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would')
]

class Tokenize(object):

    def __init__(self, text=""):
        self.text = text
        self.words = rex.tokenize(text)

class Replacers(object):

    def __init__(self):
            self.patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]

    def process(self, word):
        replaced_word = ""
        for (pattern, repl) in self.patterns:
            if re.search(pattern, word):
                replaced_word = re.sub(pattern, repl, word)
                break
        return rex.tokenize(replaced_word) if replaced_word != "" else word

class POSTagger(object):
    def __init__(self, words=[]):
        self.words = words

    def tag(self):
        tagged_words = []
        for w in self.words:
            sent = (w, (pos_tag([w]))[0][1], 'O')
            tagged_words.append(sent)
        return  tagged_words