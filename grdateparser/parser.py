from features import FeatureExtractor
from model import TaggerModel, DatesSettingsModel
from dateutility import  EnddateParser, EntityParser, RulesParser, DateAttributes

BASE_STEP = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
RULE_STEP = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"]

class DateParserFromText(object):

    def __init__(self, stext=""):
        self.TEXT = stext

    def getFeatures(self):
        fe = FeatureExtractor(self.TEXT)
        self.FEATURES = fe.extract()
        self.WORDS = fe.WORDS

    def getPatterns(self):
        tm = TaggerModel(self.FEATURES)
        self.PATTERNS = tm.predict()

    def getWordsandPatterns(self):
        self.NEW_WORDS    = []
        self.NEW_PATTERNS = []
        for i, p in enumerate(self.PATTERNS):
            if p == "UNK":
                continue

            if p in ["WORD_MIDDLE", "WM"] and len(self.NEW_PATTERNS) == 0:
                continue

            self.NEW_PATTERNS.append(p)
            self.NEW_WORDS.append(self.WORDS[i])
        print("New Patterns", self.NEW_PATTERNS, self.NEW_WORDS)

    def splitpatterns(self):
        self.SEGMENTS = []
        self.MIDDLERS = []
        self.IS_RANGE = False
        CONSTANTS = ["C_YEAR", "C_QUARTER", "C_MONTH", "C_WEEK", "C_DAY", "MONTHNAME", "DAYNAME", 'QUARTERNO', 'DIRECT_DATE']
        try:
            idx = self.NEW_PATTERNS.index("WORD_MIDDLE")
            print("WORD_MIDDLE")
            if self.NEW_PATTERNS[idx - 1] in CONSTANTS:
                print("SEGEMENT TRUE")
                self.IS_RANGE = True
                temp = []
                words = []
                for i, p in enumerate(self.NEW_PATTERNS):
                    if i < idx:
                        temp.append(p)
                        words.append(self.NEW_WORDS[i])

                self.SEGMENTS.append({ "patterns" : temp, "words": words })

                temp = []
                words = []
                for i, p in enumerate(self.NEW_PATTERNS):
                    if i > idx:
                        temp.append(p)
                        words.append(self.NEW_WORDS[i])

                self.SEGMENTS.append({"patterns": temp, "words": words})

            else:
                self.SEGMENTS.append({"patterns": self.NEW_PATTERNS, "words": self.NEW_WORDS})

        except:
            print( "Error Occured in Segmentation")
            self.SEGMENTS.append({"patterns": self.NEW_PATTERNS, "words": self.NEW_WORDS })


    def process(self):
        self.OUTPUT = {}
        print("SEGMENTS", self.SEGMENTS)
        for i, segment in enumerate(self.SEGMENTS):
            self.OUTPUT[i] = DateParser(segment["words"], segment["patterns"]).process()


    def parse(self):
        self.getFeatures()
        self.getPatterns()
        self.getWordsandPatterns()
        self.splitpatterns()
        self.process()
        START_DATE = END_DATE = ""
        START_DATE_TEXT = END_DATE_TEXT = ""
        for k, v in self.OUTPUT.items():
            try:
                if START_DATE == "":
                    START_DATE = v["START_DATE"]["DATE"]
                    START_DATE_TEXT = v["START_DATE"]["TEXT"]
                END_DATE = v["END_DATE"]["DATE"]
                END_DATE_TEXT = v["END_DATE"]["TEXT"]
            except:
                continue

        if START_DATE > END_DATE:
            START_DATE_TEXT, END_DATE_TEXT = END_DATE_TEXT, START_DATE_TEXT

        print(START_DATE, END_DATE)
        return { "START_DATE": START_DATE_TEXT, "END_DATE": END_DATE_TEXT }


class DateParser(object):

    def __init__(self, words=[], patterns=[]):
        self.WORDS = words
        self.PATTERNS = patterns

    def getDateSettings(self):
        ds = DatesSettingsModel(self.PATTERNS)
        self.DATESETTINGS = list(ds.predict()[0])
        print("DATE SETTINGS", self.DATESETTINGS )

        for settings in self.DATESETTINGS:
            if settings in BASE_STEP:
                self.BASE_STEP = settings
                continue
            if settings in RULE_STEP:
                self.RULE_STEP = settings
                continue

            self.END_RULE = settings

    def getEnityParser(self):
        ep = EntityParser(self.WORDS, self.PATTERNS)
        self.ENTITY = ep.parser()

    def getStartDate(self):
        rule = self.RULE_STEP if "RULE_STEP" in self.__dict__ else "R4"
        base = self.BASE_STEP if "BASE_STEP" in self.__dict__ else "B5"
        rs = RulesParser(step=base, rule=rule, **self.ENTITY)
        self.START_DATE = rs.parser()
        print("START DATE", self.START_DATE)

    def getEndDate(self):
        num = 0
        if "YEARS" in self.ENTITY:
            num = int(self.ENTITY["YEARS"])

        if "MONTHS" in self.ENTITY:
            num = int(self.ENTITY["MONTHS"])

        if "WEEKS" in self.ENTITY:
            num = int(self.ENTITY["WEEKS"])

        if "DAYS" in self.ENTITY:
            num = int(self.ENTITY["DAYS"])

        if "QUARTERS" in self.ENTITY:
            num = int(self.ENTITY["QUARTERS"])

        print("NUM", abs(num))
        erule = self.END_RULE if "END_RULE" in self.__dict__ else "0D"
        ep = EnddateParser(self.START_DATE, erule=erule, num=abs(num))
        self.END_DATE = ep.parser()
        print("ENDDATE", self.END_DATE)

    def prepareoutput(self):
        sdate_da = DateAttributes(self.START_DATE).getDA()
        edate_da = DateAttributes(self.END_DATE).getDA()

        data = {
            "START_DATE": {
                "TEXT": str(sdate_da["CURR.DAY"]) + "," + sdate_da["CURR.MONTHNAME"] + " " + str(sdate_da["CURR.YEAR"]),
                "DAY": sdate_da["CURR.DAYNAME"],
                "DATE": self.START_DATE
            },
            "END_DATE": {
                "TEXT": str(edate_da["CURR.DAY"]) + "," + edate_da["CURR.MONTHNAME"] + " " + str(edate_da["CURR.YEAR"]),
                "DAY": edate_da["CURR.DAYNAME"],
                "DATE": self.END_DATE
            }
        }
        print("PREPARE", data)
        return data

    def process(self):
        self.getDateSettings()
        self.getEnityParser()
        self.getStartDate()
        self.getEndDate()
        return self.prepareoutput()