import pygame
from collections import deque

#IEEE Micromouse Simulator showing the flood fill algorithm solving a 8x8 grid maze. The mouse starts at the South West(row 7, column 0) and
# The target is postion on north east (row 0, columnn 7)


# Window and grid and color
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
GRID_SIZE = 8
cell_size = 80
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Horizontal walls between the rows
h_walls = [
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
]

# Vertical walls between the columns
v_walls = [
    [1, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1],
]

target_row = 0
target_col = 7

# Flood fill algorithm
def floodfill(target_row, target_col):
    flood = [[float('inf') for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flood[target_row][target_col] = 0
    dq = deque()
    dq.append((target_row, target_col))

    while dq:
        row, col = dq.popleft()
        curr_dist = flood[row][col]

        if h_walls[row][col] == 0 and row > 0 and flood[row-1][col] > curr_dist + 1:
            flood[row-1][col] = curr_dist + 1
            dq.append((row-1, col))
        if h_walls[row+1][col] == 0 and row < GRID_SIZE-1 and flood[row+1][col] > curr_dist + 1:
            flood[row+1][col] = curr_dist + 1
            dq.append((row+1, col))
        if v_walls[row][col] == 0 and col > 0 and flood[row][col-1] > curr_dist + 1:
            flood[row][col-1] = curr_dist + 1
            dq.append((row, col-1))
        if v_walls[row][col+1] == 0 and col < GRID_SIZE-1 and flood[row][col+1] > curr_dist + 1:
            flood[row][col+1] = curr_dist + 1
            dq.append((row, col+1))

    return flood

# Move mouse to lowest flood value
def getNextcell(row, col, flood):
    best = float('inf')
    next_row, next_col = row, col

    if h_walls[row][col] == 0 and row > 0 and flood[row-1][col] < best:
        best = flood[row-1][col]
        next_row, next_col = row-1, col
    if h_walls[row+1][col] == 0 and row < GRID_SIZE-1 and flood[row+1][col] < best:
        best = flood[row+1][col]
        next_row, next_col = row+1, col
    if v_walls[row][col] == 0 and col > 0 and flood[row][col-1] < best:
        best = flood[row][col-1]
        next_row, next_col = row, col-1
    if v_walls[row][col+1] == 0 and col < GRID_SIZE-1 and flood[row][col+1] < best:
        best = flood[row][col+1]
        next_row, next_col = row, col+1

    return next_row, next_col

# Numerical value of the flood fill algorithm 
def drawDistances(flood):
    font = pygame.font.Font(None, 28)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK,
                             (c * cell_size + 2, r * cell_size + 2,
                              cell_size - 4, cell_size - 4))
            dist = flood[r][c]
            display_val = str(int(dist)) if dist != float('inf') else "?"
            text_surf = font.render(display_val, True, WHITE)
            text_rect = text_surf.get_rect(center=(c * cell_size + cell_size // 2,
                                                    r * cell_size + cell_size // 2))
            screen.blit(text_surf, text_rect)


def drawTrail(trail):
    for r, c in trail:
        pygame.draw.rect(screen, (50, 0, 100),
                         (c * cell_size + 2, r * cell_size + 2,
                          cell_size - 4, cell_size - 4))

# Draw the mouse as an orange circle
def drawMouse(r, c):
    cx = c * cell_size + cell_size // 2
    cy = r * cell_size + cell_size // 2
    pygame.draw.circle(screen, (255, 165, 0), (cx, cy), 15)

def drawGrid():
    for x in range(0, WINDOW_WIDTH, cell_size):
        for y in range(0, WINDOW_HEIGHT, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    for row in range(len(h_walls)):
        for col in range(len(h_walls[0])):
            if h_walls[row][col] == 1:
                pygame.draw.line(screen, RED,
                                 (col * cell_size, row * cell_size),
                                 ((col + 1) * cell_size, row * cell_size), 3)

    for row in range(len(v_walls)):
        for col in range(len(v_walls[0])):
            if v_walls[row][col] == 1:
                pygame.draw.line(screen, RED,
                                 (col * cell_size, row * cell_size),
                                 (col * cell_size, (row + 1) * cell_size), 3)


def drawLabels():
    font = pygame.font.Font(None, 36)
    GREEN = (0, 255, 0)
    screen.blit(font.render('S', True, GREEN), (5, WINDOW_HEIGHT - 40))
    screen.blit(font.render('T', True, RED), (WINDOW_WIDTH - 25, 5))

# Run the simulation
def main():
    global screen, CLOCK
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Micromouse Maze Simulator")
    CLOCK = pygame.time.Clock()

    flood = floodfill(target_row, target_col)
    mouse_r, mouse_c = 7, 0
    move_timer = 0
    trail = []

    running = True
    while running:
        screen.fill(BLACK)
        drawDistances(flood)
        drawTrail(trail)
        drawGrid()
        drawMouse(mouse_r, mouse_c)
        drawLabels()

        move_timer += 1
        if move_timer >= 30 and (mouse_r, mouse_c) != (target_row, target_col):
            trail.append((mouse_r, mouse_c))
            mouse_r, mouse_c = get_next_cell(mouse_r, mouse_c, flood)
            move_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
