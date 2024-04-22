import pygame as pg
import time
from os import path
from retrieve_board import get_board
WIDTH = 750
HEIGHT = 650
BACKGROUND = (251, 234, 235) #pink-ish background
LINE_COLOR = (0, 0, 0)       #black lines
NUM_COLOR = (47, 60, 126)    #blue numbers
FILL_COLOR = (119, 237, 160) #when number is filled
EMPTY_COLOR = (240, 108, 123)#when space is cleared

'''
Helper method to declutter main() loop
Draws Sudoku board lines
@param window Pygame display window and surface
'''
def draw_board_lines(window):
    #draw boxes
    for i in range(0, 10):
        #bolded separators
        if i % 3 == 0:
            pg.draw.line(window, LINE_COLOR, (100 + 50 * i, 100), (100 + 50 * i, 550), 3)
            pg.draw.line(window, LINE_COLOR, (100, 100 + 50 * i), (550, 100 + 50 * i), 3)

        pg.draw.line(window, LINE_COLOR, (100 + 50 * i, 100), (100 + 50 * i, 550))
        pg.draw.line(window, LINE_COLOR, (100, 100 + 50 * i), (550, 100 + 50 * i))
    pg.display.update()

'''
Draws in all the numbers in the Sudoku board onto the display. 
Prints all elements in a single row of the board, for every row.
Does not print zeros.
@param window Pygame display window and surface
@param font PyGame font object
@param board 2-d array representation of a Sudoku board
'''
def fill_board(window, font, board, finish = False):
    if not finish:
        for i in range(len(board)):   #A.K.A. for row in board:
            for j in range(len(board[i])): #A.K.A. for number in row:
                if board[i][j] == 0:
                    continue #do not print zeros.
                fill_space(window, board, j, i, BACKGROUND)
                pg.display.update()
                fill_space(window, board, j, i, FILL_COLOR)
                text, rect = font.render(str(board[i][j]), NUM_COLOR)
                window.blit(text, (118 + 50*j, 115+50*i)) 
                pg.display.update()
    else:
        flower(window, font, board)
'''
EXTRA METHOD FOR FINAL ANIMATION: not required, remove for efficiency
Assumes no zeros.
'''
def flower(window, font, board):
    fill_space(window, board, 4, 4, BACKGROUND)
    for i in range(1,5):  

        for j in range(1,5): 
            fill_space(window, board, 4+i, 4+j, BACKGROUND)
            fill_space(window, board, 4+i, 4-j, BACKGROUND)
            fill_space(window, board, 4-i, 4+j, BACKGROUND)
            fill_space(window, board, 4-i, 4-j, BACKGROUND)

            fill_space(window, board, 4+j, 4+i, BACKGROUND)
            fill_space(window, board, 4+j, 4-i, BACKGROUND)
            fill_space(window, board, 4-j, 4+i, BACKGROUND)
            fill_space(window, board, 4-j, 4-i, BACKGROUND)

            fill_space(window, board, 4+i, 4, BACKGROUND)
            fill_space(window, board, 4-i, 4, BACKGROUND)
            fill_space(window, board, 4, 4+i, BACKGROUND)
            fill_space(window, board, 4, 4-i, BACKGROUND)
            time.sleep(0.015)
            pg.display.update()
            # text = font.render(str(board[i][j]), True, NUM_COLOR)
            # window.blit(text, (117 + 50*j, 110+50*i)) 
            # pg.display.update()
    time.sleep(0.5)
    fill_board(window, font, board)
'''
@param clear boolean value of whether we are clearing or filling in a value
'''

def fill_space(window, board, row, col, color):
    rect = pg.Rect(102 + 50 * row, 102 + 50 * col, 47,47)
    pg.draw.rect(window, color, rect)
def create_empty_board(window):
    window.fill(BACKGROUND)
    draw_board_lines(window)
    

'''
Button class. 
'''
class Button():
    def __init__(self, x, y, image, window):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.window = window
        self.clicked = False
    def draw(self, window):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button onto screen
        window.blit(self.image, (self.rect.x, self.rect.y))

#------------------------------- SOLVER SECTION -------------------------
def safe(board, row, column, num):
    row_clear = num not in board[row]
    col_clear = not in_col(board, column, num)
    box_clear = not in_box(board, row, column, num)
    return row_clear and col_clear and box_clear

'''
Helper method for safe()
@return True if the number provided is in the column, False otherwise
@param column to check
@param num number to check for
'''
def in_col(board, column, num):
    for i in range(9):
        if board[i][column] == num:
            return True
    return False
'''
Helper method for safe()
@return True if the number provided is in the respective 3x3 box, False otherwise
@param row to check
@param column to check
@param num number to check for
'''
def in_box(board, row, column, num):
    for i in range(row// 3*3, row//3*3+3):
        for j in range(column//3*3, column//3*3+3):
            if board[i][j] == num:
                return True
    return False

''''''
def solveDFS(window, font, board, row = 0, col = 0):
    
    if row == 9:
        return True #found solution
    elif col == 9:
        #move to next row, and start on column 0
        
        return solveDFS(window, font, board, row + 1, 0)
    elif board[row][col] != 0:
        #space taken, move to next position (col + 1)
        return solveDFS(window, font, board, row, col+1)
    else: #empty space, and not out of bounds
        for num in range(1,10): #valid sudoku numbers
            fill_space(window, board, row, col, EMPTY_COLOR)
            pg.display.update()
            if safe(board, row, col, num):
                board[row][col] = num
                fill_board(window, font, board)
                if solveDFS(window, font, board, row, col+1): #if solution found
                    return True #stop recursion
                board[row][col] = 0 #solution not found, reset space
                
        return False #no valid solution, move on
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def solveAStar(window, front,board):
     # create a array of possible board solutions
    solutions = []

    # loop to run in all board
    for i in range(9):
        for j in range(9):
            # create a list with all posibilities
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            # check if cell is empty
            if (board[i][j] == 0):
                # loop to verify and remove incorrect numbers from row, column and quadrant
                for k in range(9):
                    if (board[i][k] != 0 and board[i][k] in x):
                        x.remove(board[i][k])
                    if (board[k][j] != 0 and board[k][j] in x):
                        x.remove(board[k][j])
                quad_x = j // 3 #used integer division to get the integer value from positions
                quad_y = i // 3
                for m in range(quad_y * 3, quad_y * 3 + 3):
                    for n in range(quad_x * 3, quad_x * 3 + 3):
                        if (board[m][n] != 0 and board[m][n] in x and (m, n) != (i,j)):
                            x.remove(board[m][n])
                tmp = []
                tmp.append(i)
                tmp.append(j)
                tmp.append(len(x))
                tmp.append(x)

                # insert ordered, lowest first
                index = 0
                for k in range(len(solutions)):
                    if (solutions[k][2] > tmp[2] and tmp[2] > 0):
                        index = k
                        break
                    else:
                        index+=1
                solutions.insert(index, tmp)

    if (len(solutions) > 0):
        row = solutions[0][0]
        col = solutions[0][1]

        # loop in array of solutions of current recursion
        for i in solutions[0][3]:
            # insert the valid value to board
            fill_space(window, board, row, col, EMPTY_COLOR)
            pg.display.update()
            board[row][col] = i
            fill_board(window, front, board)
            # if not find empty cell print result or call recursive to next cell
            if (not find_empty(board)):
                return True
            elif solveAStar(window,front,board):
                return True
            # if not, change the actual valid value to 0 and continue testing next value
            board[row][col] = 0

        return False

#---------------------------- END OF SOLVER SECTION -------------------------
#main loop
def main():
    pg.init()
    #make sure font package is loaded
    if not pg.font.get_init(): 
        pg.font.init()
     
    #choose fonts
    font = pg.freetype.Font(path.join('fonts', 'Minecraft.ttf'), size = 27.5)   #for numbers
    pix_font = pg.freetype.Font(path.join('fonts', 'Minecraft.ttf'), size = 25) #for timer
    pix_font.underline = True
    pix_font.strong = True

    #initialize window
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Sudoku Solver")

    #load in images for additional sprites
    instructions = pg.image.load(path.join('sprites', 'instructions.png')).convert() #text instructions
    # credit = pg.image.load(path.join('sprites', 'credit.png')).convert() 
    # version = pg.image.load(path.join('sprites', 'version.png')).convert()
    timer = pg.image.load(path.join('sprites', 'timer.png')).convert()
    #scale images
    scale = 3
    instructions = pg.transform.scale(instructions, (191 * scale, 24 * scale))
    # credit = pg.transform.scale(credit, (112 * scale, 11 * scale))
    # version = pg.transform.scale(version, (85 * scale, 10 * scale))
    timer = pg.transform.scale(timer, (49 * scale * 1.2, 22 * scale * 1.2))
    
    #load in images for buttons
    start_img = pg.image.load(path.join('sprites', 'start_button.png')).convert_alpha()
    reset_img = pg.image.load(path.join('sprites', 'reset_button.png')).convert_alpha()
    #create buttons from Button class
    start_button = Button(WIDTH - 175, 100, start_img, window)
    reset_button = Button(WIDTH - 175, 250, reset_img, window)

    #main loop
    while True:
        #fill the window with a new board and fill it
        create_empty_board(window)
        board = get_board('boards.txt')
        fill_board(window, font, board)
        
        while (not start_button.clicked) and (not reset_button.clicked):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return

            #buttons
            start_button.draw(window)
            reset_button.draw(window)

            #additional sprites
            window.blit(instructions, (10, 10))
            # window.blit(credit, (400, 600))
            # window.blit(version, (10, 600))
            
            pg.display.update()
            if start_button.clicked:
                #if 'solve' button pressed, solve the board
                start_time = time.time() #time how long it takes to solve
            
                solveDFS(window, font, board)
                end_time = time.time()   #ending time
                exec_time = end_time - start_time #elapsed time
                #elapsed = pix_font.render(str(exec_time), False, LINE_COLOR)\
                
                elapsed, rect = pix_font.render(("%.2f" % exec_time), LINE_COLOR)
                window.blit(timer, (575, 400))
                window.blit(elapsed, (558, 450))
                time.sleep(1)

                fill_board(window, font, board, finish = True)
                start_button.clicked = False
            elif reset_button.clicked:
                #if 'reset' button pressed, create a new board
                create_empty_board(window)
                board = get_board('boards.txt')
                fill_board(window, font, board, finish = False)
                reset_button.clicked = False
                time.sleep(0.05)

main()