import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import datetime

import csv

import numpy as np
from numba import jit

from keras import Model, Sequential, optimizers, regularizers
from keras.layers import Dense
from keras.utils import to_categorical

from Hackathon.fad_mlt.statistics import *




def create_model(input_shape):
	nn = Sequential()
	nn.add(Dense(len(roi), input_shape=input_shape))
	nn.add(Dense(1000, activation="sigmoid"))
	nn.add(Dense(1))
	nn.compile("adadelta", "mse", metrics=['mae'])

	return nn


def filter_data(data, without):
	new_data = []
	while len(data) > 0:
		row = data[-1]
		data.pop(-1)

		for td in without:
			row.pop(td)

		new_data.append(row)

	new_data.reverse()
	return new_data

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

		train_labels.append(float(row[lat_index]))

	train_data = set_labels(train_data, roi, f_obj)
	return train_data, train_labels

def check(nn : Model, test_data, test_labels):
	s = 0
	cnt = 0
	for i in range(len(test_data)):
		y = nn.predict([[test_data[i]]])[0][0]
		s += abs(test_labels[i] - y)
		cnt += 1

	print(s / cnt)

def main():
	train_data, train_labels = read_data(base_path, (0, 80))
	test_data, test_labels = read_data(base_path, (80, 90))

	without = (0, )
	train_data = filter_data(train_data, without)
	test_data = filter_data(test_data, without)

	train_data = np.asarray(train_data)
	train_labels = np.asarray(train_labels)

	test_data = np.asarray(test_data)
	test_labels = np.asarray(test_labels)

	# print(train_data)
	# print(train_labels)

	nn = create_model((len(roi) - len(without), ))
	nn.fit(train_data, train_labels, 1000, 50)
	nn.save_weights("weights_without_time.h5")
	#print(nn.evaluate(test_data, test_labels))
	check(nn, test_data, test_labels)


def big_check():
	test_data, test_labels = read_data(base_path, (50, 80))

	without = (0, )

	test_data = filter_data(test_data, without)

	test_data = np.asarray(test_data)
	test_labels = np.asarray(test_labels)

	nn = create_model((len(roi) - len(without), ))
	nn.load_weights('weights_without_time.h5')
	check(nn, test_data, test_labels)

if __name__ == '__main__':
	main()
