import pickle
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import os
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "data", "data.txt")

INPUT_ENCODER           = MultiLabelBinarizer()
OUTPUT_ENCODER          = MultiLabelBinarizer()
TAGGER_MODEL            = pickle.load(open(os.path.join(this_dir, "model","DateTimeNER.mdl"), "rb"))
DATES_MDL               = pickle.load(open(os.path.join(this_dir, "model","MULTI_TARGET_FOREST.mdl"), "rb"))


INPUT_ENCODER.classes_  = np.load(os.path.join(this_dir, "model","INPUT_ENCODER.npy"))
OUTPUT_ENCODER.classes_ = np.load(os.path.join(this_dir, "model","OUTPUT_ENCODER.npy"))

class TaggerModel(object):

    def __init__(self, features):
        self.features = features

    def predict(self):
        print(TAGGER_MODEL.predict(self.features))
        return TAGGER_MODEL.predict(self.features)[0]

class DatesSettingsModel(object):
    def __init__(self, patterns=[]):
        self.patterns = patterns

    def cleanup(self):
        temp = []
        for p in self.patterns:
            if p in ["UNK"]:
                continue
            else:
                q = p
                if p == "WORD_MIDDLE":
                    q = "WM"

                if p == "DAYWORDREF":
                    q = "DAYREF"

                if len(temp) == 0 and q == "WM":
                    continue

                temp.append(q)

        pads = ['BLANK' for _ in range(6 - len(temp))]
        self.features = temp + pads

    def predict(self):
        self.cleanup()
        print(self.features)
        X = INPUT_ENCODER.transform([self.features])
        #print(X)
        y = DATES_MDL.predict(X)
        #print(y)
        y_pred = OUTPUT_ENCODER.inverse_transform(y)
        #print(y_pred)
        return y_pred