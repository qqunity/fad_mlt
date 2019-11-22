import datetime

import csv

import numpy as np
from numba import jit

from keras import Model, Sequential
from keras.layers import Dense
from keras.utils import to_categorical


roi = [1, 5, 6, 12, 13, 14, 15]
lat_index = 16
base_path = 'export.csv'

def create_model():
	nn = Sequential()
	nn.add(Dense(len(roi), activation="sigmoid", input_shape=(len(roi), )))
	nn.add(Dense(512, activation="sigmoid"))
	nn.add(Dense(1))
	nn.compile("adadelta", "mse", metrics=['accuracy'])

	return nn


def time_to_daytime(time):
	time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
	ytime = time
	ytime = ytime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


	time = int(time.timestamp() - ytime.timestamp())
	return time

def to_vec(train_data):
	return train_data


def read_data(fname, slice = None):
	train_data = []
	train_labels = []

	if slice == None:
		slice = (0, 1)
	else:
		slice = (slice[0] / 100, slice[1] / 100)

	f_obj = open(fname, 'r')
	db = csv.reader(f_obj)
	length = 0

	for row in db:
		length += 1

	slice = (slice[0] * length, slice[1] * length)
	f_obj.seek(0)
	print(slice)

	for row in db:
		if row[0] == '' or int(row[0]) < slice[0]:
			continue

		if int(row[0]) > slice[1]:
			break

		train_data.append([])
		for i in roi:
			train_data[-1].append(row[i])

		train_labels.append(row[lat_index])

	train_data = to_vec(train_data)
	return train_data, train_labels



def main():
	print(time_to_daytime('2019-10-24 10:50:08.171513'))
	# train_data, train_labels = read_data(base_path, (0, 1))
	#
	# train_data = np.asarray(train_data)
	# train_labels = np.asarray(train_labels)
	#
	# print(train_data.shape)

	# nn = create_model()
	# nn.fit(train_data,train_labels, 25, 500, )


if __name__ == '__main__':
	main()
