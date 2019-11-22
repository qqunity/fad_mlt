import csv
import datetime


def time_to_yearly_stamp(time):
	time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
	ytime = time
	ytime = ytime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

	time = int(time.timestamp() - ytime.timestamp())
	return time


def uniq_type_in_column(file_obj, column):
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
