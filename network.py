import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import datetime

import csv

import numpy as np
from numba import jit

from keras import Model, Sequential
from keras.layers import Dense
from keras.utils import to_categorical

from fad_mlt.statistics import *




def create_model():
	nn = Sequential()
	nn.add(Dense(len(roi), activation="sigmoid", input_shape=(len(roi),)))
	nn.add(Dense(512, activation="sigmoid"))
	nn.add(Dense(1))
	nn.compile("adadelta", "mse", metrics=['accuracy'])

	return nn



def read_data(fname, slice=None):
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

	train_data = set_labels(train_data, roi, f_obj)
	print(train_data)
	return train_data, train_labels


def main():
	train_data, train_labels = read_data(base_path, (0, 0.005))
	#test_data, test_labels = read_data(base_path, (30, 40))
	#
	# train_data = np.asarray(train_data)
	# train_labels = np.asarray(train_labels)
	#
	# test_data = np.asarray(test_data)
	# test_labels = np.asarray(test_labels)
	#
	#
	# print(train_data.shape)
	#
	# nn = create_model()
	# nn.fit(train_data,train_labels, 25, 500)
	# nn.evaluate(test_data, test_labels)


if __name__ == '__main__':
	main()
