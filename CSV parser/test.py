import csv


def csv_reader(file_obj, cnt_lines):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    i = 1
    for row in reader:
        print(" ".join(row))
        if i == cnt_lines:
            return
        i += 1


if __name__ == '__main__':
    csv_path = '/media/dmaksimov/Miscellanea/Transactions dataset/export.csv'
    with open(csv_path, 'r') as f_obj:
        csv_reader(f_obj, 10)
