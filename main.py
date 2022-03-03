import pygame
import random
import time

WIDTH = 800
HEIGHT = 900
OFFSET = 100

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLOR_LIGHT = (170,170,170)

# Maze variables
w = 20  # Width of cell
N = 30  # Size of the NxN grid
CELLS = []  # Contains all Cell objects

# Button variables
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40
BUTTON_POS_X = WIDTH / 2 - BUTTON_WIDTH / 2
BUTTON_DFS = screen.get_height() -200
BUTTON_KRUSKAL = screen.get_height() -150
BUTTON_PRIM = screen.get_height() -100


class Cell:
    def __init__(self, row, column, x, y, visited):
        self.row = row  # row position in the 2D array CELLS
        self.column = column  # column position in the 2D array CELLS
        self.x = x  # x coordinate of the cell
        self.y = y  # y coordinate of the cell
        self.visited = visited  # check if we have already visited the cell

        # This is for disjoint set data structure for Kruskal
        self.parent = self
        self.size = 1


class Wall:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2


def build_grid():
    x = OFFSET  # x-axis
    y = 50  # y-axis
    for i in range(0, N):
        CELLS.append([])
        for j in range(0, N):
            pygame.draw.line(screen, WHITE, (x, y), (x + w, y), 1)  # Top line of square
            x = x + w
            pygame.draw.line(screen, WHITE, (x, y), (x, y + w), 1)  # Right line of square
            y = y + w
            pygame.draw.line(screen, WHITE, (x, y), (x - w, y), 1)  # Bottom line of square
            x = x - w
            pygame.draw.line(screen, WHITE, (x, y), (x, y - w), 1)  # Left line of square
            y = y - w

            # Add cell to list of all cells
            CELLS[i].append(Cell((y - 50) // w, (x - OFFSET) // w, x, y, False))

            # Add wall to list of all walls

            x = x + w

        x = OFFSET
        y = y + w

    # Create entrance and exit
    pygame.draw.line(screen, (0, 0, 0), (CELLS[0][0].x, CELLS[0][0].y), (CELLS[0][0].x, CELLS[0][0].y + w), 1)
    pygame.draw.line(screen, (0, 0, 0), (CELLS[N - 1][N - 1].x + w, CELLS[N - 1][N - 1].y),
                     (CELLS[N - 1][N - 1].x + w, CELLS[N - 1][N - 1].y + w), 1)


def text_DFS(button):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_DFS = small_font.render('DFS', True, WHITE)
    text_rect = text_DFS.get_rect()
    text_rect.center = button.center
    screen.blit(text_DFS, text_rect)

def text_Kruskal(button):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_Kruskal = small_font.render('Kruskal', True, WHITE)
    text_rect = text_Kruskal.get_rect()
    text_rect.center = button.center
    screen.blit(text_Kruskal, text_rect)


def text_Prim(button):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_Prim = small_font.render('Prim', True, WHITE)
    text_rect = text_Prim.get_rect()
    text_rect.center = button.center
    screen.blit(text_Prim, text_rect)


def create_buttons():
    color_dark = (100, 100, 100)
    b1 = pygame.draw.rect(screen, color_dark, [BUTTON_POS_X, BUTTON_DFS, BUTTON_WIDTH, BUTTON_HEIGHT])
    b2 = pygame.draw.rect(screen, color_dark, [BUTTON_POS_X, BUTTON_KRUSKAL, BUTTON_WIDTH, BUTTON_HEIGHT])
    b3 = pygame.draw.rect(screen, color_dark, [BUTTON_POS_X, BUTTON_PRIM, BUTTON_WIDTH, BUTTON_HEIGHT])

    text_DFS(b1)
    text_Kruskal(b2)
    text_Prim(b3)


def get_unvisited_neighbors(cell):
    neighbors = []

    # Check if left neighbor exists and is unvisited
    if (cell.column >= 1) and (not CELLS[cell.row][cell.column - 1].visited):
        neighbors.append(CELLS[cell.row][cell.column - 1])

    # Check if right neighbor exists and is unvisited
    if (cell.column < N - 1) and (not CELLS[cell.row][cell.column + 1].visited):
        neighbors.append(CELLS[cell.row][cell.column + 1])

    # Check if top neighbor exists and is unvisited
    if (cell.row >= 1) and (not CELLS[cell.row - 1][cell.column].visited):
        neighbors.append(CELLS[cell.row - 1][cell.column])

    # Check if top neighbor exists and is unvisited
    if (cell.row < N - 1) and (not CELLS[cell.row + 1][cell.column].visited):
        neighbors.append(CELLS[cell.row + 1][cell.column])

    return neighbors


def create_path(current_cell, next_cell):
    black = (0, 0, 0)  # color code for black

    # Next cell is to the right of current cell
    if next_cell.x > current_cell.x:
        pygame.draw.line(screen, black, (next_cell.x, next_cell.y), (next_cell.x, next_cell.y + w), 1)

    # Next cell is to the left of current cell
    elif next_cell.x < current_cell.x:
        pygame.draw.line(screen, black, (current_cell.x, current_cell.y), (current_cell.x, current_cell.y + w), 1)

    # Next cell is under the current cell
    elif next_cell.y > current_cell.y:
        pygame.draw.line(screen, black, (next_cell.x, next_cell.y), (next_cell.x + w, next_cell.y), 1)

    # Next cell is above the current cell
    elif next_cell.y < current_cell.y:
        pygame.draw.line(screen, black, (current_cell.x, current_cell.y), (current_cell.x + w, current_cell.y), 1)

    pygame.display.flip()
    time.sleep(0.005)


def dfs(cell):
    cell.visited = True

    neighbors = get_unvisited_neighbors(cell)  # returns a list of neighbors of the current cell

    while len(neighbors) != 0:
        choice = random.randint(0, len(neighbors) - 1)  # Use this to choose random neighbor (by index)
        next_cell = neighbors.pop(choice)  # Choose a random neighbor

        # Need this cuz might have visited the neighbor through other routes...
        if next_cell.visited:
            continue

        create_path(cell, next_cell)
        dfs(next_cell)


def get_all_walls():
    walls = []
    for i in range(0, N):
        for j in range(0, N):
            CELLS[i][j].visited = True
            neighbors = get_unvisited_neighbors(CELLS[i][j])
            for neighbor in neighbors:
                walls.append(Wall(CELLS[i][j], neighbor))

    return walls


# Find the parent of the current cell with path compression
def find(cell):
    if cell.parent != cell:
        cell.parent = find(cell.parent)
        return cell.parent

    else:
        return cell


# Check if cell1 and cell2 are in the same set. If not, combine them
def union(cell1, cell2):
    x = find(cell1)
    y = find(cell2)

    if x == y:
        return True

    if x.size > y.size:
        y.parent = x
        x.size = x.size + y.size

    else:
        x.parent = y
        y.size = y.size + x.size

    return False


def kruskal():
    walls = get_all_walls()  # Contains all Wall objects

    while len(walls) != 0:
        num = random.randint(0, len(walls) - 1)  # Choosing a random wall
        choice = walls.pop(num)
        if not union(choice.cell1, choice.cell2):
            create_path(choice.cell1, choice.cell2)


# Getting the walls
def get_walls(cell):
    cell.visited = True
    neighbors = get_unvisited_neighbors(cell)
    walls = []

    for neighbor in neighbors:
        walls.append(Wall(cell, neighbor))

    return walls


def prim():
    num = random.randint(0, len(CELLS) - 1)
    choice = random.choice(CELLS[num])  # pick a random starting cell

    walls = get_walls(choice)  # Will contain a list of walls from the cells we pick

    while len(walls) != 0:
        num = random.randint(0, len(walls) - 1)
        choice = walls.pop(num)  # Choose random wall

        if not (choice.cell1.visited and choice.cell2.visited):
            if not choice.cell1.visited:
                walls = walls + get_walls(choice.cell1)
            else:
                walls = walls + get_walls(choice.cell2)

            create_path(choice.cell1, choice.cell2)


def reset():
    screen.fill((0, 0, 0))
    global CELLS
    CELLS = []
    build_grid()
    create_buttons()
    pygame.display.flip()

reset()
pygame.display.flip()

# Need this for the window to stay open
running = True
while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and BUTTON_DFS <= mouse[1] <= BUTTON_DFS + BUTTON_HEIGHT:
                reset()
                dfs(CELLS[0][0])

            if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and BUTTON_KRUSKAL <= mouse[1] <= BUTTON_KRUSKAL + BUTTON_HEIGHT:
                reset()
                kruskal()

            if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and BUTTON_PRIM <= mouse[1] <= BUTTON_PRIM + BUTTON_HEIGHT:
                reset()
                prim()

        if not running:
            pygame.quit()