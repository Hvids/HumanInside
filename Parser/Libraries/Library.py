import sys
sys.path.extend(['../','../../'])
from Data import Data, DataList

class Library(Data):
    name = 'Library'

class Libraries(DataList):
    name = 'Libraries'
    name_save = 'libraries'
