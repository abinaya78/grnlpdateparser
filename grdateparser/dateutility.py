import itertools
import datetime
import math
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import SU, MO, TU, WE, TH, FR, SA
from dateutil import parser
import calendar
import re

## replace functions
def replace(day=0, month=0, year=0, gdate=datetime.date.today()):
    rdate = gdate

    if day > 0:
        rdate = rdate.replace(day=day)

    if month > 0:
        rdate = rdate.replace(month=month)

    if year > 0:
        rdate = rdate.replace(year=year)

    return rdate

## delta functions
def delta(gdate=datetime.date.today(), **kwargs):
    rdate = gdate
    if "days" in kwargs:
        rdate = rdate + relativedelta(days=+kwargs["days"])

    if "weeks" in kwargs:
        rdate = rdate + relativedelta(weeks=+kwargs["weeks"])

    if "months" in kwargs:
        rdate = rdate + relativedelta(months=+kwargs["months"])

    if "years" in kwargs:
        rdate = rdate + relativedelta(years=+kwargs["years"])

    return rdate


#### Date Attributes #####
class DateAttributes(object):

    q = {1:(1,3), 2: (4,6), 3: (7,9), 4: (10,12)}

    def __init__(self, given_date=datetime.date.today()):
        self.given_date = given_date

    def getDA(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        mcal = c.monthdatescalendar(self.given_date.year, self.given_date.month)
        da = {}
        counter = 0
        da["CURR.DATE"] = self.given_date
        da["CURR.DAY"] = self.given_date.day
        da["CURR.DAYNAME"] = self.given_date.strftime("%A")
        da["CURR.DAYINDEX"] = self.given_date.weekday()
        da["CURR.WEEK"] = self.given_date.isocalendar()[1]
        da["CURR.WEEK_START"] = self.given_date - timedelta(days=self.given_date.weekday())
        da["CURR.WEEK_END"] = self.given_date - timedelta(days=self.given_date.weekday()) + relativedelta(days=6)
        da["CURR.MONTHNAME"] = self.given_date.strftime("%B")
        da["CURR.MONTH"] = self.given_date.month
        da["CURR.MONTH_DAYS"] = calendar.monthrange(self.given_date.year, self.given_date.month)[1]
        da["CURR.MONTH_START"] = self.given_date.replace(day=1)
        da["CURR.MONTH_END"] = self.given_date.replace(day=calendar.monthrange(self.given_date.year, self.given_date.month)[1])
        da["CURR.QUARTER"] = math.ceil(self.given_date.month / 3.)
        da["CURR.QUARTER_BEGIN"] = self.q[math.ceil(self.given_date.month / 3.)][0]
        da["CURR.QUARTER_END"] = self.q[math.ceil(self.given_date.month / 3.)][1]
        da["CURR.YEAR"] = self.given_date.year
        da["CURR.YEARS_DAYS"] = 366 if calendar.isleap(self.given_date.year) else 365
        da["FIRST.MONDAY"] = [day for week in mcal for day in week if \
                day.weekday() == calendar.MONDAY and \
                day.month == self.given_date.month][0]
        da["FIRST.SUNDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.SUNDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.MONDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.MONDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.TUESDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.TUESDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.WEDNESDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.WEDNESDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.THURSDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.THURSDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.FRIDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.FRIDAY and \
                              day.month == self.given_date.month][0]
        da["FIRST.SATURDAY"] = [day for week in mcal for day in week if \
                              day.weekday() == calendar.SATURDAY and \
                              day.month == self.given_date.month][0]
        da["COUNT.SUNDAY"] = sum([counter+1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                              if day.weekday() == 6 and day.month == self.given_date.month])

        da["COUNT.MONDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 0 and day.month == self.given_date.month])

        da["COUNT.TUESDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 1 and day.month == self.given_date.month])

        da["COUNT.WEDNESDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 2 and day.month == self.given_date.month])

        da["COUNT.THURSDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 3 and day.month == self.given_date.month])

        da["COUNT.FRIDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 4 and day.month == self.given_date.month])

        da["COUNT.SATURDAY"] = sum([counter + 1 for day in c.itermonthdates(self.given_date.year, self.given_date.month) \
                                  if day.weekday() == 5 and day.month == self.given_date.month])

        return da

#### Class for BaseStep Parsers ########
class BaseStepParser(object):
    def __init__(self, gdate=datetime.date.today(), step="", **data):
        self._gdate = gdate
        self._step = step
        self._da = DateAttributes(self._gdate).getDA()
        self._kwargs = data

    def definitions(self):
        steps = {}
        steps["B1"] = {"d": 1, "m": 1, "y": "CURR.YEAR"}
        steps["B2"] = {"d": 1, "m": 1, "y": "YEAR"}
        steps["B3"] = {"d": 1, "m": "CURR.MONTH", "y": "CURR.YEAR"}
        steps["B4"] = {"d": 1, "m": "MONTH", "y": "CURR.YEAR"}
        steps["B5"] = {"d": "CURR.DAY", "m": "CURR.MONTH", "y": "CURR.YEAR"}
        steps["B6"] = {"d": "DATE", "m": "CURR.MONTH", "y": "CURR.YEAR"}
        steps["B7"] = {"d": "DATE", "m": "MONTH", "y": "CURR.YEAR"}
        steps["B8"] = {"d": "DATE", "m": "MONTH", "y": "YEAR"}
        return steps

    def getstep(self):
        steps = self.definitions()
        return steps[self._step] if self._step in steps else {}

    def parser(self):
        step = self.getstep()
        kwargs = self._kwargs

        for k, v in step.items():
            val = 0
            try:
                val = int(v)
            except:
                if v in self._da:
                    val = int(self._da[v])
                else:
                    if "DATE" in kwargs and k == "d":
                        val = int(kwargs["DATE"])

                    if "MONTH" in kwargs and k == "m":
                        val = int(kwargs["MONTH"])

                    if "YEAR" in kwargs and k == "y":
                        val = int(kwargs["YEAR"])

            if val == 0:
                continue

            if k == "d" and val > 0 and val < 32:
                self._gdate = self._gdate.replace(day=val)
                continue

            if k == "m" and val > 0 and val < 13:
                self._gdate = self._gdate.replace(month=val)
                continue

            if k == "y":
                self._gdate = self._gdate.replace(year=val)
                continue

        print("BASE STEP DATE: ", self._gdate)
        return self._gdate


#### Class for ENDDate Parsers ########
class EnddateParser:

    def __init__(self, gdate=datetime.date.today(), erule="", num=0):
        self.sdate = gdate
        self.erule = erule
        self.edate = gdate
        self.num = int(num)

    def parser(self):
        if self.erule == "3M":
            self.edate = delta(self.sdate, months=3) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "1Y":
            self.edate = delta(self.sdate, years=1) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "1M":
            self.edate = delta(self.sdate, months=1) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "1W":
            self.edate = delta(self.sdate, weeks=1) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "0D":
            self.edate = self.sdate
            #self.print_edate()

        if self.erule == "NUM+D":
            self.edate = delta(self.sdate, days=self.num) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "NUM+W":
            self.edate = delta(self.sdate, weeks=self.num) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "NUM+M":
            self.edate = delta(self.sdate, months=self.num) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "NUM+Y":
            self.edate = delta(self.sdate, years=self.num) - timedelta(days=1)
            #self.print_edate()

        if self.erule == "NUM+Q":
            self.edate = delta(self.sdate, months=self.num * 3) - timedelta(days=1)
            #self.print_edate()

        return self.edate

    def print_edate(self):
        print("EDATE:", self.edate)


#### RULE Parser Class #####
class RulesParser:

    def __init__(self, actions={}, gdate=datetime.date.today(), step="", rule="", **data):
        self.actions = actions
        self.odate = gdate
        self.BaseStep = BaseStepParser(step=step, **data)
        self.gdate = self.BaseStep.parser()
        self.rule = rule if rule != "" else ""
        self.kwargs = data

        print("ENTITY", data)

    def definitions(self):
        rules = {}
        rules["R1"]  = "R1_parser"
        rules["R2"]  = "R2_parser"
        rules["R3"]  = "R3_parser"
        rules["R4"]  = "R4_parser"
        rules["R5"]  = "R5_parser"
        rules["R6"]  = "R6_parser"
        rules["R7"]  = "R7_parser"
        rules["R8"]  = "R8_parser"
        rules["R9"]  = "R9_parser"
        rules["R10"] = "R10_parser"
        rules["R11"] = "R11_parser"
        rules["R12"] = "R12_parser"
        return rules

    def getrule(self):
        rules = self.definitions()
        return rules[self.rule] if self.rule in rules else ""

    def parser(self):
        rule = self.getrule()
        if rule != "":
            getattr(self, rule)()
            return self.START_DATE

    def R1_parser(self):
        self.START_DATE = self.gdate
        if "DAYS" in self.kwargs:
            self.START_DATE = delta(self.gdate, days=self.kwargs["DAYS"])

    def R2_parser(self):
        self.START_DATE = self.gdate
        if "YEARS" in self.kwargs:
            self.START_DATE = delta(self.gdate, years=self.kwargs["YEARS"])

    def R3_parser(self):
        self.START_DATE = self.gdate
        if "MONTHS" in self.kwargs:
            self.START_DATE = delta(self.gdate, months=self.kwargs["MONTHS"])

    def R4_parser(self):
        self.START_DATE = self.gdate

    def R5_parser(self):
        da = DateAttributes(self.gdate).getDA()
        self.gdate = replace(day=da['CURR.WEEK_START'].day)
        self.START_DATE = self.gdate
        print("RULE 5" , self.gdate)
        if "WEEKS" in self.kwargs:
            self.START_DATE = delta(self.gdate, weeks=self.kwargs["WEEKS"])

    def R6_parser(self):

        da = DateAttributes(self.gdate).getDA()
        self.gdate = replace(day=da['CURR.WEEK_START'].day)
        self.START_DATE = self.gdate
        if "DAYINDEX" in self.kwargs:
            self.START_DATE = delta(self.gdate, days=self.kwargs["DAYINDEX"] - 2)

    def R7_parser(self):

        self.START_DATE = self.gdate
        if "MONTHS" in self.kwargs:
            self.START_DATE = delta(self.START_DATE, months=self.kwargs["MONTHS"])

        if "DAYINDEX" in self.kwargs and "DAYNAME" in self.kwargs:
            if self.kwargs["DAYINDEX"] -2 == 0:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= MO(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 1:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= TU(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 2:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= WE(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 3:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= TH(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 4:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= FR(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 5:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= SA(self.kwargs["DAYNAME"]))
            if self.kwargs["DAYINDEX"] -2 == 6:
                self.START_DATE = self.START_DATE + relativedelta(day=1, weekday= SU(self.kwargs["DAYNAME"]))

    def R8_parser(self):
        da = DateAttributes(self.gdate).getDA()
        self.gdate = replace(day=da['CURR.WEEK_START'].day)
        self.START_DATE = self.gdate
        if "DAYINDEX" in self.kwargs:
            self.gdate = delta(self.gdate, days=self.kwargs["DAYINDEX"] - 2)

        if "DAYNAME" in self.kwargs:
            self.START_DATE = delta(self.gdate, weeks=self.kwargs["DAYNAME"])

    def R9_parser(self):
        print(self.gdate, self.odate)
        da = DateAttributes(self.odate).getDA()
        self.gdate = replace(gdate=self.gdate, month=da['CURR.QUARTER_BEGIN'])
        self.START_DATE = self.gdate
        if "QUARTERS" in self.kwargs:

            self.START_DATE = delta(self.gdate, months=(self.kwargs["QUARTERS"]) * 3)

    def R10_parser(self):
        self.START_DATE = self.gdate
        if "QUARTERNOMONTH" in self.kwargs:
            self.gdate = replace(gdate=self.gdate, month=self.kwargs["QUARTERNOMONTH"])

        if "YEARS" in self.kwargs:
            self.START_DATE = delta(self.gdate, years=self.kwargs["YEARS"])

    def R11_parser(self):
        self.START_DATE = self.gdate
        if "WEEKS" in self.kwargs:
            self.START_DATE = delta(self.gdate, weeks=self.kwargs["WEEKS"])

    def R12_parser(self):
        print(self.gdate, self.odate)
        da = DateAttributes(self.odate).getDA()
        self.gdate = replace(gdate=self.gdate, month=da['CURR.QUARTER_BEGIN'])
        self.START_DATE = self.gdate
        if "QUARTERS" in self.kwargs:
            self.START_DATE = delta(self.gdate, months=3)


### Entity Parser ######
class EntityParser(object):
    NAMES_OF_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                       'november', 'december']
    NAMES_OF_DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    ACTIONS = {'this': 0, 'present': 0, 'current': 0, 'active': 0,
               'last': -1, 'previous': -1, 'before': -1,
               'next': 1, 'upcoming': 1, 'after': 1, 'future': 1, 'new': 1, 'old': -1,
               'newer': 1, 'older': -1, 'ago': -1, 'past': -1
               }
    DAY_REFERENCE = {"today": 0, "yesterday": -1, "tomorrow": 1}

    def __init__(self, w=[], p=[]):
        if len(w) != len(p):
            raise "Invalid word and pattern lengths"

        self.w = w
        self.p = p

    def parser(self):
        pass

    def isMonthName(self):
        if "MONTHNAME" in self.p:
            self.MONTH = self.NAMES_OF_MONTHS.index(self.w[self.p.index("MONTHNAME")]) + 1

    def isDayName(self):
        if "DAYNAME" in self.p:
            self.DAYINDEX = self.NAMES_OF_DAYS.index(self.w[self.p.index("DAYNAME")]) + 1

    def getNumber(self, w=""):
        val = 0
        rex = re.search(r"\d+(st|nd|rd|th)", str(w).strip().lower())
        if rex:
            rex = re.search(r"\d+", str(w).strip().lower())
            val = int(rex.group())
        else:
            try:
                val = int(w)
            except:
                val = 0

        return val

    def getQuarterNumber(self, w=""):
        val = 0
        q = {1: 1, 2: 4, 3: 7, 4: 10}
        rex = re.search(r"(q|Q)\d+", str(w).strip().lower())

        if rex:
            rex = re.search(r"\d+", str(w).strip().lower())
            val = int(rex.group())
        else:
            try:
                val = int(w)
            except:
                val = 0

        if val > 0:
            val = q[val]

        return val

    def actionCounter(self):
        PARAMS = {}
        CONSTANTS = ["C_YEAR", "C_QUARTER", "C_MONTH", "C_WEEK", "C_DAY", "MONTHNAME", "DAYNAME", 'QUARTERNO']
        CLASSES = ['DATE', 'YEAR', 'UNK', 'DAYWORDREF', 'DIRECT_DATE']
        VALUE_CLASSES = ['DATE', 'YEAR', 'UNK', 'DAYWORDREF', 'DIRECT_DATE', 'QUARTERNO']
        for i, c in enumerate(CONSTANTS):
            try:
                idx = self.p.index(c)
                inc = 0
                num_found = False
                if c == "MONTHNAME":
                    self.isMonthName()

                if c == "DAYNAME":
                    self.isDayName()

                for x in reversed(range(len(self.p))):
                    if x < idx:
                        #print(x, idx, self.w[x], self.p[x])

                        if self.p[x] in ["ACTION"]:
                            if num_found:
                                inc = inc * self.ACTIONS[self.w[x]]
                            else:
                                inc = inc + self.ACTIONS[self.w[x]]

                        if self.p[x] in ["NUM"]:
                            n = self.getNumber(self.w[x])
                            inc = inc * n if inc != 0 else n
                            num_found = True

                        if self.p[x] in CLASSES or self.p[x] in CONSTANTS:
                            PARAMS[c] = {}
                            PARAMS[c]["inc"] = inc
                            break

                    PARAMS[c] = {}
                    PARAMS[c]["inc"] = inc

            except ValueError:
                continue

        self.PARAMS = PARAMS

        for i, c in enumerate(VALUE_CLASSES):
            try:
                val = 0
                #print("c", c, self.p)
                if c in self.p:
                    if c == 'DATE':
                        val = self.getNumber(self.w[self.p.index(c)])
                        setattr(self, c, val)

                    if c == 'YEAR':
                        val = self.getNumber(self.w[self.p.index(c)])
                        setattr(self, c, val)

                    if c == 'DAYWORDREF':
                        val = self.DAY_REFERENCE[self.w[self.p.index(c)]]
                        setattr(self, 'DAYS', val)

                    if c == 'QUARTERNO':
                        val = self.getQuarterNumber(self.w[self.p.index(c)])
                        setattr(self, 'QUARTERNOMONTH', val)

                    if c == 'DIRECT_DATE':
                        val = self.w[self.p.index(c)]
                        DDATE =  parser.parse(val)
                        setattr(self, 'DATE', DDATE.day)
                        setattr(self, 'MONTH', DDATE.month)
                        setattr(self, 'YEAR', DDATE.year)

            except:
                continue


    def parser(self):
        self.actionCounter()
        variables = {}

        for k, v in self.PARAMS.items():
            if k in "QUARTERNO":
                variables["YEARS"] = v['inc']
                continue

            if k in ["C_YEAR"]:
                if "YEARS" in variables:
                    continue
                else:
                    variables["YEARS"] = v['inc']
                    continue

            if k[0:2] in ["C_"]:
                variables[k[2:len(k)] + "S"] = v['inc']
            else:
                variables[k] = v['inc']

        if "MONTH" in self.__dict__:
            variables["MONTH"] = self.__dict__["MONTH"]

        if "DATE" in self.__dict__:
            variables["DATE"] = self.__dict__["DATE"]

        if "YEAR" in self.__dict__:
            variables["YEAR"] = self.__dict__["YEAR"]

        if "QUARTERNOMONTH" in self.__dict__:
            variables["QUARTERNOMONTH"] = self.__dict__["QUARTERNOMONTH"]

        if "DAYINDEX" in self.__dict__:
            variables["DAYINDEX"] = self.__dict__["DAYINDEX"]

        if "DAYS" in self.__dict__:
            variables["DAYS"] = self.__dict__["DAYS"]

        if "DIRECT_DATE" in self.__dict__:
            variables["DIRECT_DATE"] = self.__dict__["DIRECT_DATE"]

        return variables