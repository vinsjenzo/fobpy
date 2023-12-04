import csv
import os
import urllib.request
from docxtpl import DocxTemplate
import datetime
from beer import beer

print('Welcome!\n')

file_paths = ['currentdraft.txt', 'template.docx', 'archive.txt']

for file_path in file_paths:
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/vinsjenzo/fobpy/main/{file_path}", file_path)

def parse_csv_file(filename):
    beerList = []
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            beerName = row[0]
            beerStyle = row[1]
            abv = float(row[2])
            info = row[3]
            beerList.append(beer(beerName, beerStyle, abv, info))
        # print(f'Parsed {len(beerList)} beers.\n')
    return beerList

def print_beers(beerList):
    for i in range(len(beerList)):
        print(f'{i+1}. {beerList[i].name}')

def create_new_fob_doc():
    print('Parsing current draft list...')
    template = DocxTemplate('template.docx')
    now = datetime.datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%y')

    beerList = parse_csv_file('currentdraft.txt')

    print_beers(beerList)

    chosenBeers = input("\nSelect your 4 beers pls! I.E. 1,4,5,11\tChoose q to cancel!\n")
    
    if(chosenBeers == 'q'):
        return True
    chosenBeers = chosenBeers.split(',')

    chosenBeersList =[]
    for i in range(len(chosenBeers)):
        try: 
            index = int(chosenBeers[i])-1
        except ValueError:
            print('Sorry, did not understand that!')
            return True
        if(index < 0 or index >= len(beerList)):
            print("Index out of range!")
            return True
        
        chosenBeersList.append(beerList[index])
    
    context = {
        'day': day,
        'month': month,
        'chosenBeersList': chosenBeersList
    }

    template.render(context)
    template.save(f'Flight of Beer {day}-{month}-{year}.docx')

    print("Flight of beer document succesfully generated!")
    return False

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
        print('Sorry, did not understand that!')
        return
    if(index_to_delete < 0 | index_to_delete > len(currentList)):
        print("Index out of range!")
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
        print('Sorry, did not understand that!')
        return
    if(indexToAdd < 0 | indexToAdd > len(archiveList)):
        print("Index out of range!")
        return
    beerToAdd = archiveList[indexToAdd]
    if any(beer.name == beerToAdd.name for beer in currentList):
        print("Beer already in draft list!")
        return
    currentList.append(beerToAdd)
    currentList.sort()
    write_list_to_file(currentList, 'currentdraft.txt')

def print_menu():       ## Your menu design here
    currentList = parse_csv_file('currentdraft.txt')
    print(25 * "-" , "CURRENT DRAFTS" , 25 * "-")
    print_beers(currentList)
    print(30 * "-" , "MENU" , 30 * "-")
    print("1. Generate Flight of Beer Document")
    print("2. Remove beer from current draft list")
    print("3. Add beer to current draft list")
    print("4. Exit")
    print(66 * "-")
    
loop=True  
while loop:          ## While loop which will keep going until loop = False
    choice = None
    while choice not in (1, 2, 3, 4):
        print_menu()
        try:
            choice = int(input("Enter your choice [1-4]: "))
        except ValueError:
            print("That probably wasn't an option..")
            pass  # Could happen in face of bad user input
    if choice==1:     
        loop = create_new_fob_doc()
    elif choice==2:
        remove_beer_from_current_draft_list()
    elif choice==3:
        add_beer_to_current_draft_list()
    elif choice==4:
        print ("OK BYE")
        loop=False # This will make the while loop to end as not value of loop is set to False