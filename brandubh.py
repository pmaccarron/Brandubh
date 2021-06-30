import numpy as np
import random as rd
###############
#Initialisation

#attacker go first
comp = 'attack'

depth = 4
########
#Create board
size = 7

rows = [' ']*size
board = []
for i in range(size):
    board += [rows]

board = np.array(board)
board[0][0] = board[0][6] = board[6][0] = board[6][6] = 'O'
#print(board)

def showBoard():
    #print(' ________ ')
    print(' y: 0 1 2 3 4 5 6\nx')
    for i,row in enumerate(board):
        print(i,' |' + '|'.join(u for u in row) + '|')
        #if i < 6:
        #print('_______') 
    
########
#Pieces

#initial layout
# using + for attackers
# - for defenders and = for king
for i in [0,1,5,6]:
    board[3][i] = '+'
    board[i][3] = '+'
for i in [2,4]:
    board[3][i] = '-'
    board[i][3] = '-'
board[3][3] = '='

#Get coordinates/positions of atackers in a dictionary assigning arbitrary numbers to each piece
att_x, att_y = np.where(board=='+')
attack = {i+1:(att_x[i],att_y[i]) for i in range(8)}

#Positions for defenders
def_x, def_y = np.where(board=='-')
defend = {i+1:(def_x[i],def_y[i]) for i in range(4)}
defend['k'] = (3,3)

showBoard()
##########
#Move

def move(turn,player):
    '''This function takes either the attackers or defenders dictionaries (called turn)
        and lists the available pieces asking the user to put the number of which
        they want to move in.
        Then it lists the available moves for that piece and moves them to
        the selected destination.
    '''
    if player == 'human':
        print('Choose piece to move:')
        #List pieces
        for u in turn:
            print(u,turn[u])
        piece = input()
        if piece != 'k':
            #Could do with recursive error handling here
            if piece.isdigit() == False:
                piece = input('Try again\n')
            if int(piece) not in turn:
                piece = input('Try again\n')
            piece = int(piece)

        #call function "available moves" (see below)    
        moves = available_moves(piece,turn)
        if len(moves) == 0:
            #Again, should put recursive error handling function here
            piece = input('No moves, try another piece\n')
            piece = int(piece) if piece != 'k' else 'k'
            moves = available_moves(piece,turn)

        #List available moves
        print('\nAvailable moves:')
        for i,m in enumerate(moves):
            print(i, m)
        mov = input('enter space to move to:\n')
        #mov = tuple([int(i) for i in mov if i.isdigit()])
        if mov.isdigit() == False or int(mov) > i:
            mov = input('Try again\n')
        #get new position coordinate
        mov = moves[int(mov)]


    if player == 'computer':
        #random movement
        #piece = rd.choice(list(turn.keys()))
        #moves = available_moves(piece,turn)
        #mov = rd.choice(moves)
        #print("Moving piece",piece,"in position", turn[piece],"to", mov)

        piece, mov = best_move(turn)
        print("Moving piece",piece,"in position", turn[piece],"to", mov)
        
        
        
    #Replace where the piece was with an empty space
    board[turn[piece]] = ' '
    #Assign new position to the piece
    turn[piece] = mov
    #Draw piece on board
    if turn == attack:
        board[mov] = '+'
    if piece == 'k':
        board[mov] = '='
        #If the king moved from the centre position put an "O" there
        if turn[piece] != (3,3):
            board[3,3] = 'O'
    elif turn == defend:
        board[mov] = '-'

    return piece, mov


def available_moves(piece,turn):
    '''Function to check available moves for a piece
        Get piece and which player's turn it is, then check
        left and right and up and down iteratively to get free
        positions. '''
    x,y = turn[piece]
    moves = []#{}
    #moves[piece] = []
    if x < 6 :
        for i in range(x+1,7):
            if piece == 'k' and board[i,y] == 'O':
                moves += [(i,y)]
            if board[i,y] == ' ':                
                moves += [(i,y)]
            else:
                break
    if x > 0:
        for i in range(x-1,-1,-1):            
            if piece == 'k' and board[i,y] == 'O':
                moves += [(i,y)]
            if board[i,y] == ' ':
                moves += [(i,y)]
            else:
                break
    if y > 0:
        for i in range(y-1,-1,-1):            
            if piece == 'k' and board[x,i] == 'O':
                moves += [(x,i)]
            if board[x,i] == ' ':
                moves += [(x,i)]
            else:
                break
    if y < 6:
        for i in range(y+1,7):            
            if piece == 'k' and board[x,i] == 'O':
                moves += [(x,i)]
            if board[x,i] == ' ':
                moves += [(x,i)]
            else:
                break
    return moves
    


###########
#Winner

def check_win(captured):
    '''Function to check winner, takes the captured list, if the king is
        in it the attackers win, if the king is on one of the corner pieces
        the defenders win. 
    '''
    win = False
    if board[0][0] == '=' or board[0][6] == '=' or board[6][0] == '=' or board[6][6]  == '=':
        win = 1
        print('\nDefenders win!')

    if 'k' in captured:
        win = -1
        print('\nAttackers win!')

    if comp == 'attack':
        win = win*-1
    return win


#################
#Capture

def capture(turn,mov):
    """
    This function takes whose turn it is to identify the enemies.
    It checks the last move and if it surrounds an enemy it removes them and
    adds them to a captured list which it returns.
    """
    if 'k' not in turn:
        enemies = defend
        enemy = ['-','=']
        #The four corners and empty throne are hostile to everyone.
        friend = ['+','O']
    if 'k' in turn:
        enemies = attack
        enemy = ['+']
        friend = ['-','=','O']
        
    captured = []
    #get the x and y from the last move
    x, y = mov
    #Check if position on left is an enemy, if it is, check if the position to the
    # left of that has a friend (including corner pieces)
    if x > 1 and board[x-1,y] in enemy:
        if board[x-2,y] in friend:
            board[x-1,y] = ' '
            captured += [u for u in enemies if enemies[u] == (x-1,y)]
            print("Captured",captured, 'in pos',(x-1,y),'\n')
    if x < 5 and board[x+1,y] in enemy:
        if board[x+2,y] in friend:
            board[x+1,y] = ' '
            captured += [u for u in enemies if enemies[u] == (x+1,y)]
            print("Captured",captured, 'in pos',(x+1,y),'\n')
    if y > 1 and board[x,y-1] in enemy:
        if board[x,y-2] in friend:
            board[x,y-1] = ' '
            captured += [u for u in enemies if enemies[u] == (x,y-1)]
            print("Captured",captured, 'in pos',( x,y-1),'\n')
    if y < 5 and board[x,y+1] in enemy:
        if board[x,y+2] in friend:
            board[x,y+1] = ' '
            captured += [u for u in enemies if enemies[u] == (x,y+1)]
            print("Captured:",captured, 'in pos',(x,y+1),'\n')

    for u in captured:
        turn.pop(u)
        captured.remove(u)
            
    #Return list of captured pieces
    return(captured)

###########
#AI move

def best_move(turn):
    best_score = -1e100
    
    #As the board is symmetrical, there are only 2 pieces it should
    # consider moving in the first move
    if count == 1:
        #Ideally ranomise this for a quadrant and them pick one of those two pieces
        turn = {u:turn[u] for u in turn if u == 1 or u ==2}
        
    best_pieces = {}
    for piece in turn:
        moves = {}
        for m in available_moves(piece, turn):
            #move piece, same 
            original = turn[piece]
            turn[piece] = m
            capt = capture(turn,m)

            score = minimax(capt, depth,-1e100,1e100, False)

            turn[piece] = original
            if score >= best_score:
                best_score = score
                bestmove = m
                bestpiece = piece
                if len(moves) > 0:
                    if max(moves.values()) < score:
                        moves = {}
                moves[m] = score
            best_pieces[piece] = moves
            #print("moves",moves)
            #bestmove = rd.choice(list(moves.keys()))
            
        print(piece, score)

    if len(best_pieces) > 1:
        bestpiece = rd.choice(list(best_pieces.keys()))
##    else:
##        bestpiece = list(best_pieces.keys())[0]

    if len(best_pieces[bestpiece]) > 1:
        bestmove = rd.choice(list(best_pieces[bestpiece].keys()))
        
    return bestpiece, bestmove


def minimax(capt, depth, a,b, is_max):


    #This is where someone has won
    if check_win(capt) == 1:
        return 1
    if check_win(capt) == -1:
        return -1
    #This is a tie
    if depth == 0:
        return 0

    if is_max:
        
        #copy dictionary so can remove from it to check captures
        pieces = {u:attack[u] for u in attack} if turn == attack else {u:defend[u] for u in defend}

        value = -1e100
        
        for piece in pieces:
            for m in available_moves(piece, pieces):
                original = pieces[piece]
                pieces[piece] = m
                capt = capture(pieces,m)          
                value = max(value,minimax(capt,depth-1,a,b,False))
                pieces[piece] = original
                
            a = max(a, value)
            if value >= b:
                break
        return value
             
    if is_max == False:
        
        pieces = {u:attack[u] for u in attack} if turn != attack else {u:defend[u] for u in defend}

        value = 1e100
        for piece in pieces:
            for m in available_moves(piece, pieces):
                original = pieces[piece]
                pieces[piece] = m
                capt = capture(pieces,m)      
                value = min(value,minimax(board,depth-1,a,b,True))
                pieces[piece] = original
            
                b = min(b, value)
                if value <= a:
                    break
        
        return value

        
    
###########
#Game loop


#move counter
count = 0
#win condition
win = False

captured = []
while win == False:
    count += 1

    player = 'computer' if (comp == 'attack' and count %2 != 0) else 'human'
    if comp == 'defend':
        if count %2 == 0:
            player = 'computer'
        elif count %2 != 0:
            player = 'human'

    #This puts the attacker moving first
    turn = attack if count % 2 != 0 else defend
##    #Remove captured pieces from the dicionary of whoever's turn it is (why not do that in the function earlier?)
##    for u in captured:
##        turn.pop(u)
##        captured.remove(u)

    print("\nAttacker's turn ("+player+")") if count % 2 != 0 else print("\nDefender's turn ("+player+")")
    #Get the piece to move and their new position
    piece, mov = move(turn,player)
##    if player == 'computer':
##        print("Moving piece",piece#,"in position", attack[piece]
##              ,"to", mov)
    #Find out if the move captured any pieces
    captured = capture(turn,mov)
    #Display the board
    showBoard()

    win = check_win(captured)


print(int(count/2),'turns') if count %2 == 0 else print(int(count/2 + 0.5), 'turns')
