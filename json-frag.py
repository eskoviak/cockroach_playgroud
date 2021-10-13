import json

fp = open('./json/receipt.json', 'r')
data = json.load(fp)

for receipt in data['receipts']:
    print(receipt)