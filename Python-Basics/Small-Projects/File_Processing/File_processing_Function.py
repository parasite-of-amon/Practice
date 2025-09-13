import time
from time import sleep as slp

def finding_word(string,filepath):
    number = 0
    with open(filepath,'r') as myfile:
        process_list = myfile.read()
        for process_word in process_list:
            if string == process_word:
                number = number + 1 
    return number

while True:
    with open('fruits.txt', 'a+') as Fruits:
        slp(10)
        main_fruit = input('Enter Fruit Name: ')
        Fruits.write(f'{main_fruit} \n')
        process = Fruits.read()

    print(process)


