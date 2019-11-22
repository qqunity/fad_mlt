import csv
from fad_mlt.statistics import *


def creator():
    csv_path = '/home/philip/PycharmProjects/ExactPro_project/Data_set/export.csv'
    f_obj = open(csv_path, 'r')
    f_obj.seek(0)
    info_from_db = []
    for clmn in (15,):
        info_from_db.append(lat_value_dep(f_obj, clmn))
    return info_from_db


def info_parser(info_from_db):
    new_info = []
    for i in range(len(info_from_db)):
        new_info.append([info_from_db[i][0][0], info_from_db[i][0][1]['max'], info_from_db[i][0][1]['min'],
                         info_from_db[i][0][1]['average']])
    return new_info
