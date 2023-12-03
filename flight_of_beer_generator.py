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

def parse_csv_file(filename):
    beerDict = {}
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        n = 1
        for row in csv_reader:
            beerName = row[0]
            beerStyle = row[1]
            abv = row[2]
            info = row[3]
            #print(f'{n}.\t{beerName} \t\t {beerStyle} \t\t {abv}%.')
            beerDict[n]={"Name": beerName, "Style" : beerStyle, "ABV" : abv, "Info" : info}
            n += 1
        print(f'Parsed {n} beers.\n')
    return beerDict

def print_beers(beerDict):
    for key, value in beerDict.items():
        print(f'{key}. {value["Name"]}')

def create_new_fob_doc():
    print('Parsing current draft list...')
    beerDict ={}
    template = DocxTemplate('template.docx')
    now = datetime.datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%y')

    beerDict = parse_csv_file('currentdraft.txt')

    print_beers(beerDict)

    chosenBeers = input("\nSelect your 4 beers pls! I.E. 1,4,5,11\nPress q to cancel!\n")
    
    if(chosenBeers == 'q'):
        return
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

def edit_current_draft_list():
    archiveDict = parse_csv_file('archive.txt')
    currentDict = parse_csv_file('currentdraft.txt')
    print('ARCHIVE:\n\n')
    print_beers(archiveDict)
    print('\nCURRENT DRAFT:\n\n')
    print_beers(currentDict)


def print_menu():       ## Your menu design here
    print(30 * "-" , "MENU" , 30 * "-")
    print("1. Generate Flight of Beer Document")
    print("2. Modify current draft list")
    print("3. Exit")
    print(67 * "-")
    
loop=True  
while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = int(input("Enter your choice [1-3]: "))
    if choice==1:     
        create_new_fob_doc()
    elif choice==2:
        edit_current_draft_list()
    elif choice==3:
        print ("OK BYE")
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        input("Wrong option selection. Enter any key to try again..")

