import csv
import json


def csv_into_json(csv_file_path, json_file_path):
    data = {}
    data_temp = []
    with open(csv_file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            data_temp.append(row[0].split(';'))
        data_temp.remove(data_temp[0])

    for row in data_temp:
        if row[0] not in data:
            data[row[0]] = {'people': [row[1]]}
        else:
            data[row[0]]['people'].append(row[1])

    for country in data:
        data[country]['count'] = len(data[country]['people'])

    with open(json_file_path, 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    csv_into_json('data.csv', 'data.json')