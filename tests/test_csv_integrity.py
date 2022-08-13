import csv

def test_terrains_integrity():
    with open('./common/terrains.csv', newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        first_row = True
        keys = list()
        for row in reader:

            if first_row:
                assert 'key' in row
                first_row = False
                c_key = row.index('key')
            else:
                assert row[c_key] not in keys
                keys.append(row[c_key])

