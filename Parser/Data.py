from copy import  deepcopy
class Data:
    def __init__(self, passport):
        self.passport = passport

    @property
    def columns(self):
        return self.passport.key()

    @property
    def row(self):
        return self.passport

class DataList:
    def __init__(self, data_list=[]):
        self.data_list = deepcopy(data_list)

    def add(self, data):
        self.data_list.append(data)