import random 
from os import path

def get_board(file_name):
    with open(path.join(file_name)) as file:
        boards = file.readlines()
        while '\n' in boards:
            boards.remove('\n')
        #pick which grid to use, at random
        grid = random.randint(0, len(boards)//9 - 1)
        board = []
        for i in range(grid * 9, grid*9 + 9):
            row = boards[i].replace('\n', '')
            row = row.split(' ')
            row = list(map(int, row))
            board.append(row)

    return board

def input_board_auto(output, source):
    done = False
    puzzles = split_data(source)
    with open(output, 'a') as file:
        for puzzle in puzzles:
            count = 0
            for i in range(81):
                if count == 8:
                    file.write(puzzle[i])
                    count = 0
                    file.write('\n')
                    continue
                file.write(puzzle[i] + " ")
                count += 1
            file.write('\n')

def split_data(source):
    with open(source, 'r') as src:
        all_puzzles = src.readlines()
        return all_puzzles
# def main():
#     input_board_auto('boards.txt', 'easier_puzzles.txt')
# main()
# def main():
#     board = get_board('boards.txt')
#     print(board)
# main()