import csv

def test_terrains_integrity():
    with open('./common/terrains.csv', newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        first_row = True
        keys = list()
        for row in reader:

            if first_row:
                assert "key" in row
                assert "name" in row
                assert "description" in row
                assert "foodYield" in row
                assert "productionYield" in row
                assert "goldYield" in row
                assert "travelCost" in row
                assert "defensiveBonus" in row
                assert "terrainType" in row
                first_row = False
                c_key = row.index("key")
            else:
                assert row[c_key] not in keys #check for duplicate keys
                keys.append(row[c_key])

def test_features_integrity():
    with open('./common/features.csv', newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        first_row = True
        keys = list()
        for row in reader:
            if first_row:
                assert "key" in row
                assert "name" in row
                assert "description" in row
                assert "requiresTech" in row
                assert "constraints" in row
                assert "workAmount" in row
                assert "specials" in row
                assert "tags" in row
                first_row = False
                c_key = row.index("key")
            else:
                assert row[c_key] not in keys #check for duplicate keys
                keys.append(row[c_key])
