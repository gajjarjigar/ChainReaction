import pygame
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

pygame.init()
display_width = 600
display_height = 600
rows = 4
columns = 4
y_cell_size = int(display_height / rows)
x_cell_size = int(display_width / columns)
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chain Reaction - Jigar Gajjar')

# columns ==> x
# rows ==> y

turn = 1


class Color:
    # Custom
    shade = [(244, 67, 54), (0, 163, 232)]

    # Standard
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Cell:
    def __init__(self):
        self.color = None
        self.atoms = 0
        self.neighbors = []

    def addNeighbors(self, x_index, y_index):
        if y_index > 0:
            self.neighbors.append(Grid.grid[x_index][y_index - 1])
        if y_index < rows - 1:
            self.neighbors.append(Grid.grid[x_index][y_index + 1])

        if x_index > 0:
            self.neighbors.append(Grid.grid[x_index - 1][y_index])
        if x_index < columns - 1:
            self.neighbors.append(Grid.grid[x_index + 1][y_index])


class Grid:
    grid = []

    def __init__(self):
        for x in range(columns):
            grid_row = []
            for y in range(rows):
                grid_row.append(Cell())
            Grid.grid.append(grid_row)

    @staticmethod
    def make(line_color):
        screen.fill(Color.BLACK)
        for i in range(columns):
            pygame.draw.line(screen, line_color, (i * x_cell_size, 0), (i * x_cell_size, y_cell_size * columns), 1)
        for i in range(rows):
            pygame.draw.line(screen, line_color, (0, i * y_cell_size), (x_cell_size * rows, i * y_cell_size), 1)

    @staticmethod
    def draw_atoms():
        for y in range(rows):
            for x in range(columns):
                if Grid.grid[y][x].color:
                    x_center = x * x_cell_size + int(x_cell_size / 2)
                    y_center = y * y_cell_size + int(y_cell_size / 2)
                    if Grid.grid[y][x].atoms == 1:
                        pygame.draw.circle(screen, Grid.grid[y][x].color, (x_center, y_center),
                                           int(x_cell_size * 0.1))
                    elif Grid.grid[y][x].atoms == 2:
                        pygame.draw.circle(screen, Grid.grid[y][x].color, (x_center - int(x_cell_size * 0.1), y_center),
                                           int(x_cell_size * 0.1))
                        pygame.draw.circle(screen, Grid.grid[y][x].color, (x_center + int(x_cell_size * 0.1), y_center),
                                           int(x_cell_size * 0.1))
                    elif Grid.grid[y][x].atoms == 3:
                        pygame.draw.circle(screen, Grid.grid[y][x].color,
                                           (x_center - int(x_cell_size * 0.1), y_center - int(x_cell_size/1.2 * 0.1)),
                                           int(x_cell_size * 0.1))
                        pygame.draw.circle(screen, Grid.grid[y][x].color,
                                           (x_center + int(x_cell_size * 0.1), y_center - int(x_cell_size/1.2 * 0.1)),
                                           int(x_cell_size * 0.1))
                        pygame.draw.circle(screen, Grid.grid[y][x].color, (x_center, y_center + int(x_cell_size/1.2 * 0.1)),
                                           int(x_cell_size * 0.1))


def toggle_turn():
    global turn
    turn = 0 if turn == 1 else 1


def next_turn():
    return 0 if turn == 1 else 1


def burst(cell):
    cell.atoms = 0
    cell.color = None
    for neighbor in cell.neighbors:
        neighbor.atoms = neighbor.atoms + 1
        neighbor.color = Color.shade[turn]
    for neighbor in cell.neighbors:
        if neighbor.atoms > 3:
            burst(neighbor)


def check_winner():
    player1_score = 0
    player2_score = 0
    for y in range(rows):
        for x in range(columns):
            if Grid.grid[y][x].color:
                if Grid.grid[y][x].color == Color.shade[turn]:
                    player1_score = player1_score + 1
                else:
                    player2_score = player2_score + 1

    if player1_score >= 2 and player2_score == 0:
        return turn
    elif player2_score >= 2 and player1_score == 0:
        return next_turn()
    else:
        return -1


def add_atom(position):
    x = position[0]
    y = position[1]
    x_index = int((x - (x - x_cell_size * int(x / x_cell_size))) / x_cell_size)
    y_index = int((y - (y - y_cell_size * int(y / y_cell_size))) / y_cell_size)

    # Return if clicked on other players cell
    if Grid.grid[y_index][x_index].color == Color.shade[next_turn()]:
        return

    Grid.grid[y_index][x_index].atoms = Grid.grid[y_index][x_index].atoms + 1
    Grid.grid[y_index][x_index].color = Color.shade[turn]
    if not Grid.grid[y_index][x_index].neighbors:
        Grid.grid[y_index][x_index].addNeighbors(y_index, x_index)

    if Grid.grid[y_index][x_index].atoms > 3:
        burst(Grid.grid[y_index][x_index])

    toggle_turn()
    Grid.make(Color.shade[turn])
    Grid.draw_atoms()


def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONUP:
            pygame.display.set_caption('Chain Reaction - Jigar Gajjar {}'.format(pygame.mouse.get_pos()))
            add_atom(pygame.mouse.get_pos())


if __name__ == '__main__':
    grid_object = Grid()
    grid_object.make(Color.shade[turn])
    while True:
        event_handler()
        pygame.display.update()

        result = check_winner()
        if result == -1:
            continue
        else:
            Tk().wm_withdraw()  # to hide the main window
            player = 'BLUE' if turn == 0 else 'RED'
            messagebox.showinfo('Game Over', 'Player {} Wins'.format(player))
            break
