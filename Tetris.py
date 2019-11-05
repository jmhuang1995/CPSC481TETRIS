import pygame, sys,time,random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_a, K_d,K_UP
BLUE=(0 ,0 ,155)
BOX_SIZE=20
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
BOARD_WIDTH=10
score=0

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..cc.',
                     '.cc..',
                     '.....'],
                    ['.....',
                     '..c..',
                     '..cc.',
                     '...c.',
                     '.....']]

I_SHAPE_TEMPLATE = [['..c..',
                     '..c..',
                     '..c..',
                     '..c..',
                     '.....'],
                   ['.....',
                    '.....',
                    'cccc.',
                    '.....',
                    '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.cc..',
                     '.cc..',
                     '.....']]

def available_pieces():
        return{
            'Z':Z_SHAPE_TEMPLATE,
            'I':I_SHAPE_TEMPLATE,
            'O':O_SHAPE_TEMPLATE
        }

def Tetris():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('TETRIS')
    game_matrix=create_game_matrix()
    last_movement_t=time.time()
    piece=create_piece()
    score=0
    while True:
        screen.fill((0, 0, 0))
        ###move piece
        if(time.time()-last_movement_t>0.3):
            piece['row']= piece['row']+1
            last_movement_t=time.time()
        #-------------#
        draw_moving_piece(screen,piece)
        pygame.draw.rect(
        screen,
        BLUE,
        [100,50,10*20+10,20*20+10],5)
        ##BOARD
        draw_board(screen,game_matrix)
        draw_score(screen,score)

        user_input(game_matrix,piece)
        ## if piece reaches the bottom -> new
        if (not check_valid_position(game_matrix,piece,adjRow=1)):
            game_matrix = update_game_matrix(game_matrix,piece)
            lines_removed=remove_line(game_matrix)
            score += lines_removed
            piece=create_piece()
        ##-----------#
        pygame.display.update()
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

    #

def draw_score(screen,score):
    font=pygame.font.Font('freesansbold.ttf',18)
    scoreSurf=font.render('Score: %s' % score,True,(255,255,255))
    screen.blit(scoreSurf,(640 - 150,20))


def remove_line(game_matrix):
    num_lines_removed=0
    for row in range(20):
        if(check_line_full(game_matrix,row)):
            for row_to_move_down in range(row,0,-1): # from full row to top
                for column in range(10):
                    game_matrix[row_to_move_down][column] = game_matrix[row_to_move_down-1][column]
            #set top to blank
            for x in range(10):
                game_matrix[0][x] = '.'
            num_lines_removed+=1
    return num_lines_removed


def check_line_full(game_matrix,row):
    for column in range(10):
        if game_matrix[row][column] == '.':
            return False
    return True

def user_input(game_matrix,piece):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if (event.key == K_LEFT ) and check_valid_position(game_matrix,piece,adjColumn=-1):
                piece['column'] -= 1
            elif (event.key == K_RIGHT ) and check_valid_position(game_matrix,piece,adjColumn=1):
                piece['column'] += 1
            elif(event.key == K_UP):
                piece['rotate']=(piece['rotate']+1) % len(available_pieces()[piece['shape']])
                if not check_valid_position(game_matrix,piece):
                    piece['rotate']=(piece['rotate']-1) % len(available_pieces()[piece['shape']])
    ############
	
def create_piece():
    piece = {}
    random_shape = random.choice(list(available_pieces().keys()))
    piece['shape'] = random_shape
    piece['rotate'] = 0
    piece['column'] = 2  # update from 4
    piece['row'] = 0
    return piece


def draw_moving_piece(screen,piece):

    shape_to_draw = available_pieces()[piece['shape']][piece['rotate']]
    for row in range(5):
        for col in range(5):
            if shape_to_draw[row][col]!='.':
                draw_single_box(screen,piece['row']+row,piece['column']+col,(255,255,255),(217,222,226))



def update_game_matrix(matrix, piece):
    for row in range(5):
        for col in range(5):
            if(available_pieces()[piece['shape']][piece['rotate']][row][col] != '.'):
                matrix[piece['row']+row][piece['column']+col] = 'c'
    return matrix

def check_valid_position(game_matrix,piece,adjColumn=0,adjRow=0):
    piece_matrix = available_pieces()[piece['shape']][piece['rotate']]
    for row in range(5):
        for col in range(5):
            if piece_matrix[row][col] == '.':
                continue
            if not isOnBoard(piece['row']+ row + adjRow, piece['column']+ col + adjColumn):
                return False
            if game_matrix[piece['row']+ row + adjRow][piece['column'] +col + adjColumn] != '.':
                return False

    return True
	
	 ############
	
def draw_board(screen,matrix):
    game_matrix_columns=10
    game_matrix_rows=20
    for row in range(game_matrix_rows):
        for column in range(game_matrix_columns):
            if(matrix[row][column]!='.'):
                draw_single_box(screen,row,column,(255,255,255),(217,222,226))

def draw_single_box(screen,matrix_cell_row, matrix_cell_column,color,shadow_color):
    origin_x= 100 +5 + (matrix_cell_column*20+1)
    origin_y=50 + 5 + (matrix_cell_row *20+1)
    pygame.draw.rect(screen,(217,222,226),[origin_x,origin_y,20,20])
    pygame.draw.rect(screen,(255,255,255),[origin_x,origin_y,18,18])

    ############
	
def isOnBoard(row, column):
    return column >= 0 and column < 10 and row < 20
	
    ############

def create_game_matrix():
    game_matrix_columns=10
    game_matrix_rows=20
    board=[]
    for row in range(game_matrix_rows):
        new_row=[]
        for column in range(game_matrix_columns):
            new_row.append('.')
        board.append(new_row)
    return board

Tetris()