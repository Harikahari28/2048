import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Initialize the game grid
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Initialize Pygame window
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048 Game")
font = pygame.font.Font(None, FONT_SIZE)

# Game variables
score = 0
undo_grid = []

# Function to reset the game grid
def reset_game():
    global grid, score
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    spawn_tile()
    spawn_tile()

# Function to spawn a random tile (2 or 4)
def spawn_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Function to draw the game grid
def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(window, WHITE, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if grid[i][j] != 0:
                draw_tile(grid[i][j], i, j)

# Function to draw a tile
def draw_tile(value, row, col):
    color = get_tile_color(value)
    pygame.draw.rect(window, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    text = font.render(str(value), True, BLACK)
    text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))
    window.blit(text, text_rect)

# Function to get tile color based on its value
def get_tile_color(value):
    colors = {
        2: (255, 255, 178),
        4: (255, 204, 102),
        8: (255, 153, 51),
        16: (255, 102, 0),
        32: (255, 51, 51),
        64: (255, 0, 0),
        128: (255, 102, 178),
        256: (255, 0, 255),
        512: (204, 0, 204),
        1024: (102, 0, 102),
        2048: (51, 0, 51),
    }
    return colors.get(value, (255, 255, 255))

# Function to handle tile movements
def move(direction):
    global grid, undo_grid, score
    undo_grid = [row[:] for row in grid]
    if direction == "up":
        grid = [[merge(i, j, -1, 0) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    elif direction == "down":
        grid = [[merge(i, j, 1, 0) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    elif direction == "left":
        grid = [[merge(i, j, 0, -1) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    elif direction == "right":
        grid = [[merge(i, j, 0, 1) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    spawn_tile()
    if grid != undo_grid:
        score += 1

# Function to merge tiles in the specified direction
def merge(row, col, row_delta, col_delta):
    current_value = grid[row][col]
    if current_value == 0:
        return 0
    while 0 <= row + row_delta < GRID_SIZE and 0 <= col + col_delta < GRID_SIZE:
        next_value = grid[row + row_delta][col + col_delta]
        if next_value == 0:
            grid[row][col] = 0
            row += row_delta
            col += col_delta
            grid[row][col] = current_value
        elif next_value == current_value:
            grid[row][col] = 0
            grid[row + row_delta][col + col_delta] = current_value * 2
            return current_value * 2
        else:
            return current_value
    return current_value

# Main game loop
reset_game()
running = True
clock = pygame.time.Clock()

while running:
    window.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move("up")
            elif event.key == pygame.K_DOWN:
                move("down")
            elif event.key == pygame.K_LEFT:
                move("left")
            elif event.key == pygame.K_RIGHT:
                move("right")
            elif event.key == pygame.K_u:
                grid = [row[:] for row in undo_grid]

    draw_grid()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
