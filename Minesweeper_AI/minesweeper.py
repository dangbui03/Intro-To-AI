import random
import numpy as np

dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]

class Minesweeper():
    """Minesweeper game representation"""

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """Prints a text-based representation of where mines are located."""

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    print("x", end=" ")
                else:
                    print("_", end=" ")
            print()

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """Checks if all mines have been flagged."""

        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """Returns the set of all cells in self.cells known to be mines."""

        if self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        """Returns the set of all cells in self.cells known to be safe."""

        if not self.count:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """Minesweeper game player"""

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add to the cell collection if the cell is not yet explored
                # and is not the mine already none
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        cells.add((i, j))
                    # when excluding a known mine cell, decrease the count by 1
                    elif (i, j) in self.mines:
                        count -= 1
        self.knowledge.append(Sentence(cells, count))

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            safes = sentence.known_safes()
            if safes:
                for cell in safes.copy():
                    self.mark_safe(cell)
            mines = sentence.known_mines()
            if mines:
                for cell in mines.copy():
                    self.mark_mine(cell)

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 is sentence2:
                    continue
                if sentence1 == sentence2:
                    self.knowledge.remove(sentence2)
                elif sentence1.cells.issubset(sentence2.cells):
                    new_knowledge = Sentence(
                        sentence2.cells - sentence1.cells,
                        sentence2.count - sentence1.count)
                    if new_knowledge not in self.knowledge:
                        self.knowledge.append(new_knowledge)
    
    def isValid(self, x, y, N, M):
        return (x >= 0 and y >= 0 and x < N and y < M)
    
    def printGrid(self, grid):
        print("Generated Solution:")
        for row in grid:
            for cell in row:
                if cell:
                    print("x", end=" ")
                else:
                    print("_", end=" ")
            print()
    
    def isSafe(self, arr, x, y, N, M):
        if not self.isValid(x, y, N, M):
            return False
    
        for i in range(9):
            if self.isValid(x + dx[i], y + dy[i], N, M) and (arr[x + dx[i]][y + dy[i]] - 1 < 0):
                return False
    
        for i in range(9):
            if self.isValid(x + dx[i], y + dy[i], N, M):
                arr[x + dx[i]][y + dy[i]] -= 1
    
        return True
    
    def findUnvisited(self, visited):
        for x in range(len(visited)):
            for y in range(len(visited[0])):
                if not visited[x][y]:
                    return x, y
        return -1, -1
    
    def isDone(self, arr, visited):
        done = True
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                done = done and (arr[i][j] == 0) and visited[i][j]
        return done
    
    # Function to solve the minesweeper matrix
    def SolveMinesweeper(self, grid, arr, visited, N, M):
        done = self.isDone(arr, visited)
        if done:
            return True
    
        x, y = self.findUnvisited(visited)
        if x == -1 and y == -1:
            return False
        visited[x][y] = True
    
        if self.isSafe(arr, x, y, N, M):
            grid[x][y] = True
    
            if self.SolveMinesweeper(grid, arr, visited, N, M):
                return True
    
            grid[x][y] = False
            for i in range(9):
                if self.isValid(x + dx[i], y + dy[i], N, M):
                    arr[x + dx[i]][y + dy[i]] += 1
    
        if self.SolveMinesweeper(grid, arr, visited, N, M):
            return True
    
        visited[x][y] = False
    
        return False
    
    def minesweeperOperations(self, arr, N, M):
        grid = np.zeros((N, M), dtype=bool)
    
        visited = np.zeros((N, M), dtype=bool)
    
        if self.SolveMinesweeper(grid, arr, visited, N, M):
            self.printGrid(grid)
            return grid
        else:
            print("No solution exists")
            return None                  

    def backtrack_call(self, arr, M, N):
        self.minesweeperOperations(arr, M, N)
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        available_steps = self.safes - self.moves_made
        if available_steps:
            return random.choice(tuple(available_steps))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # if no move can be made
        if len(self.mines) + len(self.moves_made) == self.height * self.width:
            return None

        # loop until an appropriate move is found
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
