import pygame
import random


#Method_DFS
#github : Arshia-Danandeh
# Constants
Tile = 20
Margin = 1
Width, Height = 1000, 600
Rows, Cols = Height // Tile, Width // Tile

pygame.init()
sc = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Arshiya's Maze Generator")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"Up": True, "down": True, "left": True, "right": True}
        self.visited = False

    def draw(self):
        x = self.x * Tile
        y = self.y * Tile
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#a9237d'), (x, y, Tile, Tile))
        if self.walls["Up"]:
            pygame.draw.line(sc, pygame.Color('#060105'), (x, y), (x + Tile, y), 2)
        if self.walls["right"]:
            pygame.draw.line(sc, pygame.Color('#060105'), (x + Tile, y), (x + Tile, y + Tile), 2)
        if self.walls["down"]:
            pygame.draw.line(sc, pygame.Color('#060105'), (x + Tile, y + Tile), (x, y + Tile), 2)
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color('#060105'), (x, y + Tile), (x, y), 2)

    def check_neighbors(self, grid):
        neighbors = []
        directions = [
            (0, -1, "Up", "down"),
            (0, 1, "down", "Up"),
            (-1, 0, "left", "right"),
            (1, 0, "right", "left"),
        ]
        for dx, dy, wall1, wall2 in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < Cols and 0 <= ny < Rows:
                neighbor = grid[ny * Cols + nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, wall1, wall2))
        return random.choice(neighbors) if neighbors else None

def remove_walls(current, next_cell, wall1, wall2):
    current.walls[wall1] = False
    next_cell.walls[wall2] = False

def reset_game_state():
    global grid_cells, current_cell, stack
    grid_cells = [Cell(col, row) for row in range(Rows) for col in range(Cols)]
    current_cell = grid_cells[0]
    stack = []

reset_game_state()

gameOn = True
while gameOn:
    sc.fill(pygame.Color('#1e272e'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            reset_game_state()

    for cell in grid_cells:
        cell.draw()

    #maze generation
    current_cell.visited = True
    neighbor = current_cell.check_neighbors(grid_cells)
    if neighbor:
        next_cell, wall1, wall2 = neighbor
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell, wall1, wall2)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    if not stack :
        gameOn = False

    pygame.display.flip()
    clock.tick(150)