# -*- coding: utf-8 -*-
"""Module for printing a styled document with info for selected beers."""
import csv
import os
import urllib.request
import datetime
from docxtpl import DocxTemplate
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
    """Function parsing a beerlist txt file, returning a list of beers, name;style;abv;info."""
    _beer_list = []
    with open(filename, encoding="UTF-8") as csvfile:
        try:
            csv_reader = csv.reader(csvfile, delimiter=';')
            for row in csv_reader:
                name = row[0]
                style = row[1]
                abv = float(row[2])
                info = row[3]
                _beer_list.append(Beer(name, style, abv, info))
            # print(f'Parsed {len(beerList)} beers.\n')
            return _beer_list
        except FileNotFoundError:
            print(f"File not found: {filename}\n")
            return None

def print_beers(beer_list):
    """Function printing a list of beers."""
    for index, beer in enumerate(beer_list):
        print(f'{index+1}. {beer.name}')

def create_new_fob_doc(_chosen_beers_list):
    """Function creating a styled word document from a list of beers."""
    template = DocxTemplate('template.docx')
    now = datetime.datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%y')

    context = {
        'day': day,
        'month': month,
        'chosenBeersList': _chosen_beers_list
    }
    print(_chosen_beers_list[0].style)

    template.render(context, autoescape=True)
    try:
        template.save(f'Flight of Beer {day}-{month}-{year}.docx')
    except PermissionError:
        print(f"\n{FAIL}Couldnt save the generated document"
              f", please close the opened word document!{ENDC} \n")
        return False
    
    print(f"{OKGREEN}Flight of beer document succesfully generated!{ENDC}")
    return True

def write_list_to_file(current_list, filename):
    """Fuction writing a beerlist to a .txt file."""
    with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for beer in current_list:
            csvwriter.writerow([beer.name, beer.style, beer.abv, beer.info])

def remove_beer_from_current_draft_list():
    """Function removing a beer from a list."""
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
    """Function adding a beer to curent draft list from archive.""" 
    current_list = parse_csv_file('currentdraft.txt')
    archive_list = parse_csv_file('archive.txt')
    print(30 * "-" , "CURRENT DRAFT" , 30 * "-")
    print_beers(current_list)
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
    if any(beer.name == beer_to_add.name for beer in current_list):
        print(f"{FAIL}Beer already in draft list!{ENDC}")
        return
    current_list.append(beer_to_add)
    current_list.sort()
    write_list_to_file(current_list, 'currentdraft.txt')

def save_new_beer_in_archive(_new_beer, filename):
    """Function saving a new beer in archive file."""
    beer_list = parse_csv_file(filename)
    if not any(beer.name == _new_beer.name for beer in beer_list):
        beer_list.append(_new_beer)
        beer_list.sort()
        write_list_to_file(beer_list, filename)
        return True
    return False

def get_new_beer_from_input():
    """Function creating a new beer from input."""
    name = input("What is the name of the beer? ")
    style = input("What style is the beer? ")
    abv = input("What is the abv%? ")
    abv = abv.replace(',', '.')
    info = input("Please give a brief description of the beer: ")

    try:
        new_beer = Beer(name, style, float(abv), info)
    except ValueError:
        print(f"{FAIL}Couldn't parse the input{ENDC}")
        return None
    return new_beer


def print_menu():
    """Function printing the program menu."""
    current_list = parse_csv_file('currentdraft.txt')
    print(25 * "-" , "CURRENT DRAFTS" , 25 * "-")
    print_beers(current_list)
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
        beer_list = parse_csv_file('currentdraft.txt')
        if beer_list is None:
            continue

        print_beers(beer_list)
        chosen_indices = input("\nSelect your 4 beers pls! I.E. 1, 4, 5, 11\tChoose q to cancel!\n")
        if chosen_indices == 'q':
            continue
        chosen_indices = chosen_indices.split(',')

        chosen_beers_list =[]
        FAILED = False
        for i, chosen_index in enumerate(chosen_indices):
            try:
                index_beer_list = int(chosen_index)-1
            except ValueError:
                print(f'{FAIL}Sorry, did not understand that!{ENDC}')
                FAILED = True
                break

            if(index_beer_list < 0 or index_beer_list >= len(beer_list)):
                print(F"{FAIL}Index out of range!{ENDC}")
                FAILED = True
                break
            chosen_beers_list.append(beer_list[index_beer_list])
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
