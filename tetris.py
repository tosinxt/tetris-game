import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]]
]


class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_shape = self.get_random_shape()
        self.current_shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_shape_y = 0

    def get_random_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_shape(self, screen):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x] != 0:
                    pygame.draw.rect(screen, WHITE, ((self.current_shape_x + x) * BLOCK_SIZE,
                                                     (self.current_shape_y + y) * BLOCK_SIZE,
                                                     BLOCK_SIZE, BLOCK_SIZE))

    def is_valid_position(self, shape, x, y):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] != 0:
                    if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or self.grid[y + row][x + col] != 0:
                        return False
        return True

    def place_shape(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x] != 0:
                    self.grid[self.current_shape_y + y][self.current_shape_x + x] = WHITE

    def check_lines(self):
        lines_to_remove = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_remove.append(y)

        for line in lines_to_remove:
            del self.grid[line]
            self.grid.insert(0, [0] * GRID_WIDTH)

    def update(self):
        if self.is_valid_position(self.current_shape, self.current_shape_x, self.current_shape_y + 1):
            self.current_shape_y += 1
        else:
            self.place_shape()
            self.check_lines()
            self.current_shape = self.get_random_shape()
            self.current_shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
            self.current_shape_y = 0

    def move_shape(self, dx):
        if self.is_valid_position(self.current_shape, self.current_shape_x + dx, self.current_shape_y):
            self.current_shape_x += dx

    def rotate_shape(self):
        rotated_shape = [[self.current_shape[y][x] for y in range(len(self.current_shape))] for x in
                         range(len(self.current_shape[0]) - 1, -1, -1)]
        if self.is_valid_position(rotated_shape, self.current_shape_x, self.current_shape_y):
            self.current_shape = rotated_shape

    def is_game_over(self):
        return not self.is_valid_position(self.current_shape, self.current_shape_x, self.current_shape_y)

    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_grid(screen)
        self.draw_shape(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    game_over = False
    tetris = Tetris()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_shape(-1)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_shape(1)
                elif event.key == pygame.K_DOWN:
                    tetris.update()
                elif event.key == pygame.K_UP:
                    tetris.rotate_shape()

        tetris.update()

        if tetris.is_game_over():
            game_over = True

        tetris.draw(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
