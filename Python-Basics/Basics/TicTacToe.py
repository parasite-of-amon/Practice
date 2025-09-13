Main_Board = {'7': ' ' , '8': ' ' , '9': ' ' ,
              '4': ' ' , '5': ' ' , '6': ' ' ,
              '1': ' ' , '2': ' ' , '3': ' ' }

board_keys = []

for key in Main_Board:
    board_keys.append(key)

def printBoard(board):
    print('+---+---+---+')
    print('|' , board['1'] , '|' , board['2'] , '|' , board['3'] , '|')
    print('+---+---+---+')
    print('|' , board['4'] , '|' , board['5'] , '|' , board['6'] , '|')
    print('+---+---+---+')
    print('|' , board['7'] , '|' , board['8'] , '|' , board['9'] , '|')
    print('+---+---+---+')

def game():
    turn = 'X'
    count = 0
    for times in range(10):
        printBoard(Main_Board)
        print("It's your turn," + turn + ".Move to which place?")

        move = input()        

        if Main_Board[move] == ' ':
            Main_Board[move] = turn
            count += 1
        else:
            print("That place is already filled.\nMove to which place?")
            continue

        # Checking The Winner
        if count >= 5:
            if Main_Board['7'] == Main_Board['8'] == Main_Board['9'] != ' ': # across the top
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!')                
                break
            elif Main_Board['4'] == Main_Board['5'] == Main_Board['6'] != ' ': # across the middle
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break
            elif Main_Board['1'] == Main_Board['2'] == Main_Board['3'] != ' ': # across the bottom
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break
            elif Main_Board['1'] == Main_Board['4'] == Main_Board['7'] != ' ': # down the left side
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break
            elif Main_Board['2'] == Main_Board['5'] == Main_Board['8'] != ' ': # down the middle
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break
            elif Main_Board['3'] == Main_Board['6'] == Main_Board['9'] != ' ': # down the right side
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break 
            elif Main_Board['7'] == Main_Board['5'] == Main_Board['3'] != ' ': # diagonal
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break
            elif Main_Board['1'] == Main_Board['5'] == Main_Board['9'] != ' ': # diagonal
                printBoard(Main_Board)
                print("\nGame Over.\n")                
                print(f'Winner = {turn}!!') 
                break 

        # Draw Situation
        if count == 9:
            print("\nGame Over.\n")                
            print("It's a Tie!!")

        # Changing Player per Move
        if turn =='X':
            turn = 'O'
        else:
            turn = 'X'        
    
    # Restaring Game 
    restart = input("Do You Wanna Take Revenge?(y/n)")
    if restart == "y" or restart == "Y":  
        for key in board_keys:
            Main_Board[key] = " "

        game()

if __name__ == "__main__":
    game()