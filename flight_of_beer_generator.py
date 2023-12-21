# -*- coding: utf-8 -*-
import csv
import os
import urllib.request
from docxtpl import DocxTemplate
import datetime
from beer import Beer

FAIL = '\033[91m'
ENDC = '\033[0m'
OKGREEN = '\033[92m'

print('Welcome!\n')

file_paths = ['currentdraft.txt', 'template.docx', 'archive.txt']

for file_path in file_paths:
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/vinsjenzo/fobpy/main/{file_path}", file_path)

def parse_csv_file(filename):
    beerList = []
    with open(filename) as csvfile:
        try:
            csv_reader = csv.reader(csvfile, delimiter=';')
            for row in csv_reader:
                beerName = row[0]
                beerStyle = row[1]
                abv = float(row[2])
                info = row[3]
                beerList.append(Beer(beerName, beerStyle, abv, info))
            # print(f'Parsed {len(beerList)} beers.\n')
            return beerList
        except:
            return None
        
def print_beers(beerList):
    for i in range(len(beerList)):
        print(f'{i+1}. {beerList[i].name}')

def create_new_fob_doc(chosenBeersList):
    template = DocxTemplate('template.docx')
    now = datetime.datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%y')
    
    context = {
        'day': day,
        'month': month,
        'chosenBeersList': chosenBeersList
    }
    print(chosenBeersList[0].style)

    template.render(context, autoescape=True)
    try:
        template.save(f'Flight of Beer {day}-{month}-{year}.docx')
    except PermissionError:
        print(f"\n{FAIL}Could not save the generated document, please close the opened word document!{ENDC} \n")
        return False

    print(f"{OKGREEN}Flight of beer document succesfully generated!{ENDC}")
    return True

def write_list_to_file(currentList, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for beer in currentList:
            csvwriter.writerow([beer.name, beer.style, beer.abv, beer.info])

def remove_beer_from_current_draft_list():
    currentList = parse_csv_file('currentdraft.txt')
    print_beers(currentList)
    response = input("Select beer to remove.\tChoose q to cancel.\n")
    if(response == 'q'):
        return
    try: 
        index_to_delete = int(response)-1
    except ValueError:
        print(f'{FAIL}Sorry, did not understand that!{ENDC}')
        return
    if(index_to_delete < 0 or index_to_delete >= len(currentList)):
        print(f"{FAIL}Index out of range!{ENDC}")
        return
    currentList.pop(index_to_delete)
    currentList.sort()
    write_list_to_file(currentList,'currentdraft.txt')

    
def add_beer_to_current_draft_list():
    currentList = parse_csv_file('currentdraft.txt')
    archiveList = parse_csv_file('archive.txt')
    print(30 * "-" , "CURRENT DRAFT" , 30 * "-")
    print_beers(currentList)
    print(30 * "-" , "ARCHIVE" , 30 * "-")
    print_beers(archiveList)

    response = input("Select beer to add.\tChoose q to cancel.\n")
    if(response == 'q'):
        return
    try: 
        indexToAdd = int(response)-1
    except ValueError:
        print(f'{FAIL}Sorry, did not understand that!{ENDC}')
        return
    if(indexToAdd < 0 or indexToAdd >= len(archiveList)):
        print(f"{FAIL}Index out of range!{ENDC}")
        return
    beerToAdd = archiveList[indexToAdd]
    if any(beer.name == beerToAdd.name for beer in currentList):
        print(f"{FAIL}Beer already in draft list!{ENDC}")
        return
    currentList.append(beerToAdd)
    currentList.sort()
    write_list_to_file(currentList, 'currentdraft.txt')

def save_new_beer_in_archive(newBeer, filename):
    beerList = parse_csv_file(filename)
    if not any(beer.name == newBeer.name for beer in beerList):
        beerList.append(newBeer)
        beerList.sort()
        write_list_to_file(beerList, filename)
        return True
    return False

def get_new_beer_from_input():
    name = input("What is the name of the beer? ")
    style = input("What style is the beer? ")
    abv = input("What is the abv%? ")
    abv = abv.replace(',', '.')
    info = input("Please give a brief description of the beer: ")
    
    try:
        newBeer = Beer(name, style, float(abv), info)
    except ValueError:
        print(f"{FAIL}Couldn't parse the input{ENDC}")
        return None
    return newBeer


def print_menu():       ## Your menu design here
    currentList = parse_csv_file('currentdraft.txt')
    print(25 * "-" , "CURRENT DRAFTS" , 25 * "-")
    print_beers(currentList)
    print(30 * "-" , "MENU" , 30 * "-")
    print("1. Generate Flight of Beer document.")
    print("2. Remove beer from current draft list.")
    print("3. Add beer to current draft list.")
    print("4. Create new beer in archive.")
    print("5. Exit")
    print(66 * "-")
    
Running=True  
while Running:          ## While loop which will keep going until loop = False
    choice = None
    while choice not in (1, 2, 3, 4, 5):
        print_menu()
        try:
            choice = int(input("Enter your choice [1-5]: "))
        except ValueError:
            print(f"{FAIL}That probably wasn't an option..{ENDC}")
            break
        if(choice <= 0 or choice > 5 ):
            print(f"{FAIL}Your options are [1-5]{ENDC}")
    if choice==1:
        beerList = parse_csv_file('currentdraft.txt')
        
        if beerList == None:
            continue
        
        print_beers(beerList)
        chosenBeers = input("\nSelect your 4 beers pls! I.E. 1, 4, 5, 11\tChoose q to cancel!\n")
        if(chosenBeers == 'q'):
            continue
        chosenBeers = chosenBeers.split(',')

        chosenBeersList =[]
        failed = False
        for i in range(len(chosenBeers)):
            try: 
                index = int(chosenBeers[i])-1
            except ValueError:
                print(f'{FAIL}Sorry, did not understand that!{ENDC}')
                failed = True
                break
        
            if(index < 0 or index >= len(beerList)):
                print(F"{FAIL}Index out of range!{ENDC}")
                failed = True
                break
            chosenBeersList.append(beerList[index])
        if(not failed):
            Running = ~create_new_fob_doc(chosenBeersList)
    elif choice==2:
        remove_beer_from_current_draft_list()
    elif choice==3:
        add_beer_to_current_draft_list()
    elif choice==4:
        newBeer = get_new_beer_from_input()
        if newBeer!= None:
            print(f'\n{OKGREEN}Added {newBeer.name}{ENDC}\n' if save_new_beer_in_archive(newBeer, 'archive.txt') else F'\n{FAIL}Beer already in archive{ENDC}\n') 
    elif choice==5:
        print ("OK BYE")
        Running=False