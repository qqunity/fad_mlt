import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from fad_mlt.info_creator.creator import *


def get_diagrams():
    data_values = creator()
    f_names = ['partition', 'segment', 'market', 'req_type', 'cores']
    k = 4
    for info in data_values:
        data = info_parser(info)
        title = ['Максимальное значение', 'Минимальное значение', 'Среднее значение']
        data_names = []
        for i in range(len(data)):
            data_names.append(data[i][0])
            data[i].pop(0)
        new_data = []
        for i in range(3):
            buff_data = []
            for j in range(len(data)):
                buff_data.append(data[j][i])
            new_data.append(buff_data)
        print(new_data)
        c = 1
        dpi = 80
        mpl.rcParams.update({'font.size': 9})
        fig = plt.figure(figsize=(12, 4))
        for i in range(3):
            plt.subplot(1, 3, c)
            mpl.rcParams.update({'font.size': 9})
            plt.title(title[c - 1])
            plt.pie(
                new_data[c - 1], autopct='%.1f', radius=1.1, )
            plt.legend(
                bbox_to_anchor=(-0.25, 0.45, 0.25, 0.25),
                loc='lower left', labels=data_names)
            c = c + 1
            plt.axis('off')
        plt.savefig(f_names[k] + '_column_giagrams')
        k += 1


if __name__ == '__main__':
    get_diagrams()
