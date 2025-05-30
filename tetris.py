import pygame as pg
from utils.tetromino import Tetromino

# Constants
FPS = 60
WIDTH, HEIGHT = 900, 900
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 300, 600
GAME_START_X, GAME_START_Y = (WIDTH - GRID_WIDTH) // 2, HEIGHT - GRID_HEIGHT
BLOCKS_PER_ROW, BLOCKS_PER_COL = 10, 20

class Tetris:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Tetris")

        self.clock = pg.time.Clock()
        self.time = 0
        self.falling_speed = 1
        self.running = False

        self.level = 1
        self.score = 0
        self.lines = 0
        self.combo = 0 
        self.last_clear_tetris = False 

        self.current_tetromino = Tetromino()
        self.next_tetromino = Tetromino()
        self.hold_tetromino = None
        self.last_hold = False

        self.filled_space = {}
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
    
    def hold(self):
        if self.last_hold:
            return
        if self.hold_tetromino:
            self.current_tetromino, self.hold_tetromino = self.hold_tetromino, self.current_tetromino
            self.current_tetromino.reset()
            self.hold_tetromino.reset()
        else:
            self.hold_tetromino = self.current_tetromino
            self.current_tetromino = self.next_tetromino
            self.next_tetromino = Tetromino()
        self.last_hold = True

    def fill_grid(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        for coord, icon in self.filled_space.items():
            x, y = coord
            self.grid[y][x] = icon
    
    def check_collision(self, ghost=False):
        coords = self.current_tetromino.coords if not ghost else self.current_tetromino.ghost_coords
        for x, y in coords:
            if y < 0:
                continue
            if y < 0 or x < 0 or x >= BLOCKS_PER_ROW or y >= BLOCKS_PER_COL or self.grid[y][x]:
                return True
        return False

    def check_lines_cleared(self):
        y_cleared = []
        for y, row in enumerate(self.grid):
            if all(row):
                y_cleared.append(y)
        return y_cleared

    def clear_lines(self, y_cleared):                
        lines = len(y_cleared)
        start_y = y_cleared[0]
        temp_filled_space = {}
        for (x, y), value in self.filled_space.items():
            if y in y_cleared:
                continue
            if y < start_y:
                temp_filled_space[(x, y + lines)] = value
            else:
                temp_filled_space[(x, y)] = value
        self.filled_space = temp_filled_space

    def lose(self) -> bool:
        return any([y < 0 for x, y in self.filled_space.keys()])
    
    def draw_grid(self):
        for row in range(BLOCKS_PER_COL + 1):
            pg.draw.line(self.screen, 
                         (255, 255, 255), 
                         (GAME_START_X, GAME_START_Y + row * BLOCK_SIZE), 
                         (GAME_START_X + GRID_WIDTH, GAME_START_Y + row * BLOCK_SIZE))
        for col in range(BLOCKS_PER_ROW + 1):
            pg.draw.line(self.screen, 
                         (255, 255, 255), 
                         (GAME_START_X + col * BLOCK_SIZE, GAME_START_Y), 
                         (GAME_START_X + col * BLOCK_SIZE, GAME_START_Y + GRID_HEIGHT))
    
    def draw_icons(self):
        for (x, y), icon in self.filled_space.items():
            self.screen.blit(icon, (GAME_START_X + x * BLOCK_SIZE, GAME_START_Y + y * BLOCK_SIZE), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
        for x, y in self.calculate_ghost_coords():
            if y < 0:
                continue
            surface = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
            surface.set_alpha(20)
            surface.fill((255, 255, 255))
            self.screen.blit(surface, (GAME_START_X + x * BLOCK_SIZE, GAME_START_Y + y * BLOCK_SIZE), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
        for x, y in self.current_tetromino.coords:
            if y < 0:
                continue
            self.screen.blit(self.current_tetromino.icon, (GAME_START_X + x * BLOCK_SIZE, GAME_START_Y + y * BLOCK_SIZE), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
    
    def draw_text(self):
        font = pg.font.Font(None, 50)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 200, 100))
        text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 200, 200))
        text = font.render(f"Lines: {self.lines}", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 200, 300))
        text = font.render(f"Next", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 200, 400))
        text = font.render(f"Hold", True, (255, 255, 255))
        self.screen.blit(text, (GAME_START_X - 200, 400))
        if self.next_tetromino:
            for x, y in self.next_tetromino.coords:
                self.screen.blit(self.next_tetromino.icon, (WIDTH - 300 + x * BLOCK_SIZE, 500 + y * BLOCK_SIZE), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
        if self.hold_tetromino:
            for x, y in self.hold_tetromino.coords:
                self.screen.blit(self.hold_tetromino.icon, (GAME_START_X - 300 + x * BLOCK_SIZE, 500 + y * BLOCK_SIZE), (0, 0, BLOCK_SIZE, BLOCK_SIZE))

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_icons()
        self.draw_text()
        pg.display.flip()
    
    def handle_events(self) -> tuple[tuple[int, int], int, int]: #dmove, rmove, move_value
        move_value = 0
        dmove = None
        rmove = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    dmove = (-1, 0)
                elif event.key == pg.K_RIGHT:
                    dmove = (1, 0)
                elif event.key == pg.K_DOWN:
                    dmove = (0, 1)
                    self.time = 0
                elif event.key == pg.K_UP:
                    rmove = 1
                elif event.key == pg.K_z:
                    rmove = -1
                elif event.key == pg.K_SPACE:
                    while not self.check_collision():
                        self.current_tetromino.move(0, 1)
                        move_value += 2
                    self.time = 0
                    self.current_tetromino.move(0, -1)
                    dmove = (0, 1)
                    move_value -= 2
                elif event.key == pg.K_c:
                    if not self.last_hold:
                        self.hold()
                        self.last_hold = True
                        self.time = 0
        return (dmove, rmove, move_value)

    def calculate_ghost_coords(self):
        self.current_tetromino.ghost_coords = self.current_tetromino.coords[:]
        while not self.check_collision(ghost=True):
            self.current_tetromino.move(0, 1, ghost=True)
        self.current_tetromino.move(0, -1, ghost=True)
        return self.current_tetromino.ghost_coords
    
    def game_loop(self):
        self.running = True
        while self.running:
            self.time += self.clock.get_time()
            
            dmove, rmove, move_value = self.handle_events()

            if self.time * self.falling_speed >= 1000:
                dmove = (0, 1)
                self.time = 0
            self.fill_grid()
            if dmove:
                self.current_tetromino.move(*dmove)
            if rmove:
                self.current_tetromino.rotate(rmove)
                if self.check_collision():
                    self.current_tetromino.rotate(-rmove)

            if self.check_collision():
                if dmove == (0, 1) or not dmove:
                    self.current_tetromino.move(0, -1)
                    for x, y in self.current_tetromino.coords:
                        self.filled_space[(x, y)] = self.current_tetromino.icon
                    self.current_tetromino = self.next_tetromino
                    self.next_tetromino = Tetromino()
                    self.fill_grid()
                    while self.check_collision(): 
                        self.current_tetromino.move(0, -1)
                    self.last_hold = False
                else:
                    self.current_tetromino.move(*list(map(lambda x: -x, dmove)))

            if y_cleared := self.check_lines_cleared():
                lines = len(y_cleared)
                if lines == 4:
                    move_value += 1200 * self.level if self.last_clear_tetris else 800 * self.level
                    self.last_clear_tetris = True
                else: 
                    if lines == 3:
                        move_value += 500 * self.level
                    elif lines == 2:
                        move_value += 300 * self.level
                    else:
                        move_value += 100 * self.level
                    self.last_clear_tetris = False
                self.score += (move_value + 50 * self.combo) * self.level

                
                self.lines += lines
                self.combo = True
                self.clear_lines(y_cleared)
                self.level = self.lines // 10
                self.falling_speed = 1 + self.level * 0.1
            else:
                self.combo = False
            
            if self.lose():
                self.running = False
                break
                return
            
            self.draw_game()
            self.clock.tick(FPS)

    def main_menu(self):
        self.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 75)
        title = font.render("Tetris", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2))
        font = pg.font.Font(None, 50)
        start_text = font.render("Press any key to start", True, (255, 255, 255))
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + title.get_height() // 2 + 20))
        pg.display.flip()
        self.menu = True
        while self.menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    self.menu = False
                    quit()
                if event.type == pg.KEYDOWN:
                    self.menu = False
                    tetris.game_loop()
    
    def main(self):
        while True:
            self.main_menu()
            


if __name__ == "__main__":
    tetris = Tetris()

    tetris.main()
