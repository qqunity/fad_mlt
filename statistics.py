import csv
import datetime

labels_cached = [[[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], [['req1', 'delete', 'update', 'req2'], ['London', 'Obninsk', 'NewYork', 'Moscow'], ['B1', 'E3', 'M2', 'E2', 'M1', 'M4', 'M3', 'D1', 'A1', 'E1']], [0, 3, 4]]
roi = [3, 5, 6, 12, 13, 14, 15]
lat_index = 16
base_path = '/media/dmaksimov/Miscellanea/Transactions dataset/export.csv'

def time_to_yearly_stamp(time):
	time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
	ytime = time
	ytime = ytime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

	time = int(time.timestamp() - ytime.timestamp())
	return time


def uniq_type_in_column(file_obj, column):
	file_obj.seek(0)
	data_base = csv.reader(file_obj)
	req_types = set()
	for row in data_base:
		if row[0] == '':
			continue
		if not (row[column] in req_types):
			req_types.add(row[column])
	return list(req_types)


def lat_value_dep(file_obj, column):
	data_base = csv.reader(file_obj)
	values_in_column = uniq_type_in_column(file_obj, column)
	max_for_values_in_column = [-100000] * len(values_in_column)
	min_for_values_in_column = [100000000] * len(values_in_column)
	cnt_for_values_in_column = [0] * len(values_in_column)
	sum_for_values_in_column = [0] * len(values_in_column)

	file_obj.seek(0)

	for row in data_base:
		if row[0] == '':
			continue
		i = 0
		lat = float(row[16])

		k = values_in_column.index(row[column])
		max_for_values_in_column[k] = max(max_for_values_in_column[i], lat)
		min_for_values_in_column[k] = min(min_for_values_in_column[i], lat)
		cnt_for_values_in_column[k] += 1
		sum_for_values_in_column[k] += abs(lat)


	value_dep = []
	i = 0
	for val in values_in_column:
		value_dep += [val, {'max': max_for_values_in_column[i], 'min': min_for_values_in_column[i],
							'average': (sum_for_values_in_column[i] / cnt_for_values_in_column[i])}]
		i += 1

	return value_dep


def cnt_uniq_type_in_column(file_obj, column):
	file_obj.seek(0)
	data_base = csv.reader(file_obj)
	req_types = set()
	cnt = 0
	for row in data_base:
		if not (row[column] in req_types):
			cnt += 1
			req_types.add(row[column])

	return cnt - 1


def get_labels(train_data, roi, f_obj):
	f_obj.seek(0)
	labels = []
	labels_name = []
	labels_id = []
	i = 0
	for item in train_data[0]:
		if not item.isdigit() and item != '':
			labels.append([])
			labels[-1] = [buff for buff in range(cnt_uniq_type_in_column(f_obj, roi[i]))]
			labels_name.append([])
			labels_name[-1] = [buff for buff in uniq_type_in_column(f_obj, roi[i])]
			labels_id.append(i)
		i += 1

	return (labels, labels_name, labels_id)


def set_labels(train_data, roi, f_obj):
	f_obj.seek(0)
	labels, labels_name, labels_id = labels_cached[0], labels_cached[1], labels_cached[2]
	new_train_data = []
	for row in train_data:
		for i in range(len(labels_id)):
			val = row[labels_id[i]]
			j = 0
			while val != labels_name[i][j]:
				j += 1
			row[labels_id[i]] = labels[i][j]
		# row[0] = time_to_yearly_stamp(row[0])

		for i in range(len(row)):
			if row[i] == '':
				row[i] = 0.0
			else:
				row[i] = float(row[i])

		new_train_data.append(row)

	return new_train_data



