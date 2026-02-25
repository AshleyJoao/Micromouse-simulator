import pygame
from collections import deque

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
    [1, 1, 1, 1, 1, 1, 1, 1],
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
        r, c = dq.popleft()
        curr_dist = flood[r][c]

        if h_walls[r][c] == 0 and r > 0 and flood[r-1][c] > curr_dist + 1:
            flood[r-1][c] = curr_dist + 1
            dq.append((r-1, c))
        if h_walls[r+1][c] == 0 and r < GRID_SIZE-1 and flood[r+1][c] > curr_dist + 1:
            flood[r+1][c] = curr_dist + 1
            dq.append((r+1, c))
        if v_walls[r][c] == 0 and c > 0 and flood[r][c-1] > curr_dist + 1:
            flood[r][c-1] = curr_dist + 1
            dq.append((r, c-1))
        if v_walls[r][c+1] == 0 and c < GRID_SIZE-1 and flood[r][c+1] > curr_dist + 1:
            flood[r][c+1] = curr_dist + 1
            dq.append((r, c+1))

    return flood

# Move mouse to lowest flood value neighbor
def get_next_cell(r, c, flood):
    best = float('inf')
    next_r, next_c = r, c

    if h_walls[r][c] == 0 and r > 0 and flood[r-1][c] < best:
        best = flood[r-1][c]
        next_r, next_c = r-1, c
    if h_walls[r+1][c] == 0 and r < GRID_SIZE-1 and flood[r+1][c] < best:
        best = flood[r+1][c]
        next_r, next_c = r+1, c
    if v_walls[r][c] == 0 and c > 0 and flood[r][c-1] < best:
        best = flood[r][c-1]
        next_r, next_c = r, c-1
    if v_walls[r][c+1] == 0 and c < GRID_SIZE-1 and flood[r][c+1] < best:
        best = flood[r][c+1]
        next_r, next_c = r, c+1

    return next_r, next_c

# Draw distances as numbers on black cells
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

# Draw trail of visited cells
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

# Draw the grid and walls
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

# Draw S and T labels
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