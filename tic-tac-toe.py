import numpy as np
import random as rd
###############
#Initialisation

#X goes first
player = 'O'
comp = 'X'


########
#Create board
Board = {'7': ' ' , '8': ' ' , '9': ' ' ,
         '4': ' ' , '5': ' ' , '6': ' ' ,
         '1': ' ' , '2': ' ' , '3': ' ' }

def printBoard(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['1'] + '|' + board['2'] + '|' + board['3'])


###########
#Winner

def check_win():
    win = False
    a = np.array([np.array(list(Board.values())[0+n:3+n]) for n in range(0,7,3)])
    #check horizontals and verticals
    for i in range(3):
        if np.all(a[i] =='X'):
            win = 'X'
        if np.all(a[i] =='O'):
            win = 'O'
        if np.all(a[:,i] =='X'):
            win = 'X'
        if np.all(a[:,i] =='O'):
            win = 'O'
    #check diagonals
    if np.all(np.array([a[0][0],a[1][1],a[2][2]])=='X') or np.all(np.array([a[0][2],a[1][1],a[2][0]])=='X') :
        win = 'X'
    if np.all(np.array([a[0][0],a[1][1],a[2][2]])=='O') or np.all(np.array([a[0][2],a[1][1],a[2][0]])=='O'):
        win = 'O'
    return win


#################
#Check move valid

def check_move(move):
    if move.isdigit() == False or int(move) < 1 or int(move) > 10:
        move = input('\ntry again\n')
        check_move(move)
    if Board[move] != ' ':
        move = input('\ntry again\n')
        check_move(move)
    return move

###########
#AI move

def best_move():
    best_score = -1e100
    if len([u for u in Board if Board[u] == ' ']) == 9:
           bestmove = '5'
    else:
        moves = {}
        for move in [u for u in Board if Board[u] == ' ']:
            Board[move] = comp
            score = minimax(Board, 9,-1e100,1e100, False)
            print(move, score)
            Board[move] = ' '
            if score >= best_score:
                best_score = score
                bestmove = move
                if len(moves) > 0:
                    if max(moves.values()) < score:
                        moves = {}
                moves[move] = score
            if len(moves) > 1:
                bestmove = rd.choice(list(moves.keys()))

    return bestmove


def minimax(board, depth, a,b, is_max):    

    #This is where someone has won
    if check_win() == comp:
        return 1
    if check_win() == player:
        return -1
    #This is a tie
    if len([u for u in board if board[u] == ' ']) == 0:
        return 0

    if is_max:
        value = -1e100
        for move in [u for u in board if board[u] == ' ']:            
            board[move] = comp
            value = max(value,minimax(board,depth-1,a,b,False))
            board[move] = ' '
            a = max(a, value)
            if value >= b:
                break
        return value
            
        
    if is_max == False:
        value = 1e100
        for move in [u for u in board if board[u] == ' ']:
            board[move] = player
            value = min(value,minimax(board,depth-1,a,b,True))
            board[move] = ' '
            b = min(b, value)
            if value <= a:
                break
    
        return value


##    ####This works but the sum is strange and seems unusual
##    val = -1e100 if is_max else 1e100
##    scores = []
##    for move in [u for u in board if board[u] == ' ']:
####        if depth == 4:
####            break
##        if is_max == True:
##            board[move] = comp
##            scores.append(minimax(board,depth+1,a,b,False))
##            if sum(scores)> b:
##                board[move] = ' '
##                break
##            a = max(val,sum(scores))
##            
##        
##        if is_max == False:
##            board[move] = player
##            scores.append(minimax(board,depth+1,a,b,True))
##            if sum(scores) <a:
##                board[move] = ' '
##                break
##            b = max(val,sum(scores))
##    
##        board[move] = ' '
##    
##    return sum(scores)#max(scores) if is_max==True else min(scores)
        

    
###########
#Game loop

#Start turn
turn = 'X'
#move counter
count = 0
#win condition
win = False

while win == False:
    printBoard(Board)

    #Remove this if there are 2 players
    if turn == player:
        #Get move
        move = input("\n"+turn+"'s turn. [Numpad: 1-9]\n")
        #Check for error
        move = check_move(move)

    if turn == comp:
        print("\ncomp's turn\n")
        move = best_move()

    #Add move to board
    Board[move] = turn
    count += 1
    
    #Switch turn
    turn = 'O' if turn == 'X' else 'X'

    #Check for winner
    if count > 4:
        win = check_win()     
        if win != False:
            printBoard(Board)
            print("\n"+win, "WINS!")
            break
    
    if count == 9:
        printBoard(Board)
        print("\nIt's a Tie")
        break

