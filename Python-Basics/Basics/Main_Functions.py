import random
from random import randint as ri

main_list = ['A','B','C','D','E','F','G','H','I']

# Defining Functions
def building_board(a = 'A',b = 'B',c = 'C',d = 'D',e = 'E',f = 'F',g = 'G',h = 'H',i = 'I'):
    board = f"""
    +---+---+---+
    | {a} | {b} | {c} |
    +---+---+---+
    | {d} | {e} | {f} |
    +---+---+---+
    | {g} | {h} | {i} |
    +---+---+---+
    """
    return board

def checking_validity(info):
    if info in main_list:
        return True
    else:
        return False

def printing_processed_board(getting_input):
        

def prompting_value():
    print(building_board())
    board_list = []
    n = 0
    while True:
        if 0 <= n < 9 and if n % 2 == 1:
            input_x = input("Enter The Value Of Box To Be Replaced With X: ")
            if checking_validity(input_x):
                print(printing_processed_board(input_x))