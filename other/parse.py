import urllib.request
import pdfplumber
import json
from decimal import *

url = 'http://gamma.infor.pl/zalaczniki/dzu/2022/266/dzu.2022.266.1988.0001.pdf'
file = "input.pdf"

print("\ndownloading " + str(url) + "\n")

urllib.request.urlretrieve(url, file)

pdf = pdfplumber.open(file)

print("opening " + str(file) + "\n")

tables = []

for page in pdf.pages:
    tables.extend(page.extract_tables())
    print("  processed " + str(page.page_number) + " of " + str(len(pdf.pages)) + " pages", end="\r")

rows = [
    tables[0][0],
]

for table in tables:
    freq = table[0][1]
    multiplyer = 0 if "kHz" in freq else 3

    for row in table[1:]:
        if "Poniżej 8,3 kHz" in row[1]:
            low = 0
            high = 8.3
        else:
            low = float(Decimal(row[1].replace(',', '.')).shift(multiplyer))
            high = float(Decimal(row[2].replace(',', '.')).shift(multiplyer))

        rows.append([
            row[0],
            low,
            high,
            row[3],
            row[4],
        ])

rows[1:] = sorted(rows[1:], key=lambda x: x[1])

print("\n\nwriting " + str(len(rows)) + " rows to output.json")

with open('pages/data.json', 'w') as outfile:
    json.dump(rows, outfile, indent=2)

print("\ndone\n")

 