import sys

sys.path.extend(['../'])
from Data import DataList, Data
import pandas as pd


class Book(Data):
    name = 'Book'


class Books(DataList):
    name = 'Books'
