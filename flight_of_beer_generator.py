import csv
import os
import urllib.request
from docxtpl import DocxTemplate
import datetime

print('Welcome!\n')

file_paths = ['currentdraft.txt', 'template.docx', 'archive.txt']

for file_path in file_paths:
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/vinsjenzo/fobpy/main/{file_path}", file_path)
      
print('Parsing current draft list...')
beerDict ={}
template = DocxTemplate('template.docx')
now = datetime.datetime.now()
day = now.strftime('%d')
month = now.strftime('%m')
year = now.strftime('%y')

with open('currentdraft.txt') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    n = 0

    for row in csv_reader:
        if n == 0:
            #print(f'Column names are {", ".join(row)}')
            n += 1
        else:
            beerName = row[0]
            beerStyle = row[1]
            abv = row[2]
            info = row[3]
            #print(f'{n}.\t{beerName} \t\t {beerStyle} \t\t {abv}%.')
            beerDict[n]={"Name": beerName, "Style" : beerStyle, "ABV" : abv, "Info" : info}
            n += 1
    print(f'Parsed {n} beers.\n')

for key, value in beerDict.items():
    print(f'{key}. {value["Name"]}')

chosenBeers = input("\nSelect your 4 beers pls! I.E. 1,4,5,11\n")    
chosenBeers = chosenBeers.split(',')

chosenBeersDict = {}
for i in range(len(chosenBeers)):
    chosenBeersDict[i] = beerDict[int(chosenBeers[i])]

context = {
    'day': day,
    'month': month,
    'chosenBeersDict': chosenBeersDict
}

template.render(context)
template.save(f'Flight of Beer {day}-{month}-{year}.docx')

print("Flight of beer document succesfully generated!")