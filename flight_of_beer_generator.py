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

BASE_PATH = "https://raw.githubusercontent.com/vinsjenzo/fobpy/main"
file_names = ['currentdraft.txt', 'template.docx', 'archive.txt']

for file_name in file_names:
    if not os.path.exists(file_name):
        urllib.request.urlretrieve(f"{BASE_PATH}/{file_name}", file_name)

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
        print(f"\n{FAIL}Couldnt save the generated document"
              ", please close the opened word document!{ENDC} \n")
        return False

    print(f"{OKGREEN}Flight of beer document succesfully generated!{ENDC}")
    return True

def write_list_to_file(current_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for beer in current_list:
            csvwriter.writerow([beer.name, beer.style, beer.abv, beer.info])

def remove_beer_from_current_draft_list():
    current_list = parse_csv_file('currentdraft.txt')
    print_beers(current_list)
    response = input("Select beer to remove.\tChoose q to cancel.\n")
    if response == 'q':
        return
    try:
        index_to_delete = int(response)-1
    except ValueError:
        print(f'{FAIL}Sorry, did not understand that!{ENDC}')
        return
    if(index_to_delete < 0 or index_to_delete >= len(current_list)):
        print(f"{FAIL}Index out of range!{ENDC}")
        return
    current_list.pop(index_to_delete)
    current_list.sort()
    write_list_to_file(current_list,'currentdraft.txt')


def add_beer_to_current_draft_list():
    currentList = parse_csv_file('currentdraft.txt')
    archive_list = parse_csv_file('archive.txt')
    print(30 * "-" , "CURRENT DRAFT" , 30 * "-")
    print_beers(currentList)
    print(30 * "-" , "ARCHIVE" , 30 * "-")
    print_beers(archive_list)

    response = input("Select beer to add.\tChoose q to cancel.\n")
    if response == 'q':
        return
    try:
        index_to_add = int(response)-1
    except ValueError:
        print(f'{FAIL}Sorry, did not understand that!{ENDC}')
        return
    if(index_to_add < 0 or index_to_add >= len(archive_list)):
        print(f"{FAIL}Index out of range!{ENDC}")
        return
    beer_to_add = archive_list[index_to_add]
    if any(beer.name == beer_to_add.name for beer in currentList):
        print(f"{FAIL}Beer already in draft list!{ENDC}")
        return
    currentList.append(beer_to_add)
    currentList.sort()
    write_list_to_file(currentList, 'currentdraft.txt')

def save_new_beer_in_archive(newBeer, filename):
    beer_list = parse_csv_file(filename)
    if not any(beer.name == newBeer.name for beer in beer_list):
        beer_list.append(newBeer)
        beer_list.sort()
        write_list_to_file(beer_list, filename)
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

RUNNING=True
while RUNNING:          ## While loop which will keep going until loop = False
    CHOICE = None
    while CHOICE not in (1, 2, 3, 4, 5):
        print_menu()
        try:
            CHOICE = int(input("Enter your choice [1-5]: "))
        except ValueError:
            print(f"{FAIL}That probably wasn't an option..{ENDC}")
            break
        if(CHOICE <= 0 or CHOICE > 5 ):
            print(f"{FAIL}Your options are [1-5]{ENDC}")
    if CHOICE==1:
        beerList = parse_csv_file('currentdraft.txt')
        if beerList is None:
            continue

        print_beers(beerList)
        chosen_beers = input("\nSelect your 4 beers pls! I.E. 1, 4, 5, 11\tChoose q to cancel!\n")
        if chosen_beers == 'q':
            continue
        chosen_beers = chosen_beers.split(',')

        chosen_beers_list =[]
        FAILED = False
        for i in range(len(chosen_beers)):
            try:
                index = int(chosen_beers[i])-1
            except ValueError:
                print(f'{FAIL}Sorry, did not understand that!{ENDC}')
                FAILED = True
                break

            if(index < 0 or index >= len(beerList)):
                print(F"{FAIL}Index out of range!{ENDC}")
                FAILED = True
                break
            chosen_beers_list.append(beerList[index])
        if not FAILED:
            RUNNING = ~create_new_fob_doc(chosen_beers_list)
    elif CHOICE==2:
        remove_beer_from_current_draft_list()
    elif CHOICE==3:
        add_beer_to_current_draft_list()
    elif CHOICE==4:
        new_beer = get_new_beer_from_input()
        if new_beer is not None:
            print(f'\n{OKGREEN}Added {new_beer.name}{ENDC}\n'
                  if save_new_beer_in_archive(new_beer, 'archive.txt')
                  else F'\n{FAIL}Beer already in archive{ENDC}\n')
    elif CHOICE==5:
        print ("OK BYE")
        RUNNING=False
# End-of-file (EOF)