import numpy as np
import random as rd
###############
#Initialisation

#attacker is player 1 and goes first
player2 = 'human'
player1 = 'computer'


glob_depth = 5
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

def showBoard(board):
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
defend = {u:(def_x[i],def_y[i]) for i,u in enumerate(['a','b','c','d'])}
defend['k'] = (3,3)

showBoard(board)
##########
#Move

def move(board,turn,player=None,piece=None,mov=None):
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
            if 'k' not in turn:
                if piece.isdigit() == False:
                    piece = input('Try again\n')
                if int(piece) not in turn:
                    piece = input('Try again\n')
            if 'k' in turn and piece not in turn:
                piece = input('Try again\n')
            piece = int(piece) if 'k' not in turn else piece

        #call function "available moves" (see below)    
        moves = available_moves(board,piece,turn)
        if len(moves) == 0:
            #Again, should put recursive error handling function here
            piece = input('No moves, try another piece\n')
            piece = int(piece) if piece != 'k' else 'k'
            moves = available_moves(board,piece,turn)

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
    if 'k' not in turn:
        board[mov] = '+'
    if piece == 'k':
        board[mov] = '='
        #If the king moved from the centre position put an "O" there
        if turn[piece] != (3,3):
            board[3,3] = 'O'
    elif 'k' in turn:
        board[mov] = '-'


    return piece, mov


def available_moves(board,piece,turn):
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

def check_win(board,captured,turn):
    '''Function to check winner, takes the captured list, if the king is
        in it the attackers win, if the king is on one of the corner pieces
        the defenders win. 
    '''
    win = False
    if board[0][0] == '=' or board[0][6] == '=' or board[6][0] == '=' or board[6][6]  == '=':
        win = 1
        #print('\nDefenders win!')

    if 'k' in captured:
        win = -1
        #print('\nAttackers win!')

    if 'k' not in turn:
        win = win*-1

    return win


#################
#Capture

def capture(board,turn,mov):
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
            #print("Captured",captured, 'in pos',(x-1,y),'\n')
    if x < 5 and board[x+1,y] in enemy:
        if board[x+2,y] in friend:
            board[x+1,y] = ' '
            captured += [u for u in enemies if enemies[u] == (x+1,y)]
            #print("Captured",captured, 'in pos',(x+1,y),'\n')
    if y > 1 and board[x,y-1] in enemy:
        if board[x,y-2] in friend:
            board[x,y-1] = ' '
            captured += [u for u in enemies if enemies[u] == (x,y-1)]
            #print("Captured",captured, 'in pos',( x,y-1),'\n')
    if y < 5 and board[x,y+1] in enemy:
        if board[x,y+2] in friend:
            board[x,y+1] = ' '
            captured += [u for u in enemies if enemies[u] == (x,y+1)]
            #print("Captured:",captured, 'in pos',(x,y+1),'\n')

##    for u in captured:
##        turn.pop(u)
##        captured.remove(u)
            
    #Return list of captured pieces
    return(captured)

###########
#AI move

def best_move(turn):
    best_score = -1e100

    #create new dictionaries
    dfn = {u:defend[u] for u in defend}
    att = {u:attack[u] for u in attack}
    turn = dfn if 'k' in turn else att
    notturn = att if 'k' in turn else dfn
    
    best_pieces = {}
    for piece in turn:
        
        #copy board
        temp_board = np.array([u for u in board])

        #As the board is symmetrical, there are only 2 pieces it should
        # consider moving in the first move
        if count == 1:
            #Ideally ranomise this for a quadrant and them pick one of those two pieces
            if piece > 2:
                break

        for m in available_moves(temp_board, piece, turn):

            #re-initialise everything
            dfn = {u:defend[u] for u in defend}
            att = {u:attack[u] for u in attack}
            turn = dfn if 'k' in turn else att
            notturn = att if 'k' in turn else dfn
            temp_board = np.array([u for u in board])

            #Should this definitely be here?
            capt = []
            
            original = turn[piece]
            piece, m = move(temp_board,turn,None,piece,m)
            capt += capture(temp_board,turn,m)

            #this is a counter for minimax, it aims to make the best move in the quickest time
            c = 1
            #These are just copies for the minimax to keep originals
            turn0 = {u:turn[u] for u in turn}
            notturn0 = {u:notturn[u] for u in notturn}
            Board0 = np.array([u for u in temp_board])
            
            score = minimax(temp_board,notturn, glob_depth,-1e100,1e100, False,capt,turn,c,notturn0,turn0,Board0)
            
            #print(piece,score,m)
            turn[piece] = original
            temp_board[0][0] = temp_board[0][6] = temp_board[6][0] = temp_board[6][6] = 'O'
            if score >= best_score:
                if score > best_score:
                    best_pieces = {}
                best_score = score
                bestmove = m
                bestpiece = piece
                if bestpiece in best_pieces:
                    best_pieces[piece] += [bestmove]
                else:
                    best_pieces[piece] = [bestmove]

        print(piece, score)

    if len(best_pieces) > 1:
        bestpiece = rd.choice(list(best_pieces.keys()))
    if len(best_pieces[bestpiece]) > 1:
        bestmove = rd.choice(best_pieces[bestpiece])
    
    return bestpiece, bestmove


def minimax(Board, turn, depth, a,b, is_max,capt,notturn,c,turn0=None,notturn0=None,Board0=None):

    #This is where someone has won
    if is_max:
##      #Want to reverse this as it's checking the result of the previous minimax
        # 
        if check_win(Board,capt,turn) == 1:
            return 100
        if check_win(Board,capt,turn) == -1:
            return -100
    if is_max == False:
##        print(turn)
##        print(check_win(Board,capt,turn))
##        xx
        if check_win(Board,capt,notturn) == 1:
            return 100
        if check_win(Board,capt,notturn) == -1:
            return -100
    #Add in possibility for a tie
    if depth == 0:
        return 0
    
    if is_max:
        value = -1e100  
        for piece in sorted(turn,reverse=True):
            
            if piece in capt:
                continue
            for m in available_moves(Board,piece, turn):
                
                original = turn[piece]
                move(Board,turn,None,piece,m)
                capt += capture(Board,turn,m)

##                if 'k' in capt:
##                    if 'k' in turn:
##                        return -1
##                    else:
##                        return 1

                c += 1

                value = max(value,minimax(Board,notturn,depth-1,a,b,False,capt,turn,c,notturn0,turn0,Board0))
                move(Board,turn,None,piece,original)
                Board[0][0] = Board[0][6] = Board[6][0] = Board[6][6] = 'O'
                
                a = max(a, value)
                if value >= b:
                    break
##                if depth-1 == 0:
##                    Board = Board0
##                    turn = {u:turn0[u] for u in turn0}
##                    notturn = {u:notturn0[u] for u in notturn0}                    
##                    depth = glob_depth
##                    break
        return value
             
    if is_max == False:
        value = 1e100
        for piece in sorted(turn,reverse=True):
##            c = 1
##            flag = 0
##            if piece == 'k':
##                flag = 1
##                print(available_moves(Board,piece, turn))
##                showBoard(Board)
##                xx
            if piece in capt:
                continue
            for m in available_moves(Board,piece, turn):
                original = turn[piece]
                move(Board,turn,None,piece,m)
                c += 1
                capt += capture(Board,turn,m)
##                if flag == 1 and c == 1:
##                    if m == (0,6) or m == (0,0):
##                        print('\n',c)
##                        showBoard(Board)
##                        print(turn, capt)
##                        print(check_win(Board,capt,turn))
##                        xx
                        
##                if 'k' in capt:
##                    if 'k' in turn:
##                        return 1
##                    else:
##                        return -1
                value = min(value,minimax(Board,notturn,depth-1,a,b,True,capt,turn,c,notturn0,turn0,Board0))
##                if value == 100:
##                    print(c)
##                    showBoard(Board)
##                    xx
                
                move(Board,turn,None,piece,original)
                Board[0][0] = Board[0][6] = Board[6][0] = Board[6][6] = 'O'
            
                b = min(b, value)
                if value <= a:
                    break
##                if depth-1 == 0:
##                    depth = glob_depth
##                    Board = Board0
##                    turn = {u:turn0[u] for u in turn0}
##                    notturn = {u:notturn0[u] for u in notturn0}
##                    break
        
        return value/depth

        
    
###########
#Game loop


#move counter
count = 0
#win condition
win = False

##move(board,defend,piece='a',mov=(1,6))
move(board,attack,piece=1,mov=(0,2))
move(board,attack,piece=2,mov=(2,5))
move(board,defend,piece='k',mov=(0,3))
showBoard(board)

captured = []
while win == False:
    count += 1

    #This puts the attacker moving first
    player = player1 if count % 2 != 0 else player2    
    turn = attack if count % 2 != 0 else defend
    #Remove captured pieces from the dicionary of whoever's turn it is (why not do that in the function earlier?)
    for u in captured:
        print("Captured:",u, 'in pos',turn[u],'\n')
        turn.pop(u)
        captured.remove(u)

    print("\nAttacker's turn ("+player+")") if count % 2 != 0 else print("\nDefender's turn ("+player+")")
    #Get the piece to move and their new position
    piece, mov = move(board,turn,player)
##    if player == 'computer':
##        print("Moving piece",piece#,"in position", attack[piece]
##              ,"to", mov)
    #Find out if the move captured any pieces
    captured = capture(board,turn,mov)

    #Display the board
    showBoard(board)

    win = check_win(board,captured,turn)
    if win != False:
        print("\nAttacker's win!!") if count % 2 != 0 else print("\nDefender's win!!")
