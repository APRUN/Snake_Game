import pygame
from pygame.locals import *
import time, random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    
class Apple:
    def __init__(self, parent_screen):
        self.x = 3 * SIZE
        self.y = 3 * SIZE
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 12) * SIZE

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000, 500))
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.play_background_music()
    
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)  # -1 means play continuously and 0 means play from start

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 200))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 250))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.X[0], self.snake.Y[0], self.apple.x, self.apple.y):
            self.snake.increase_length(1)
            self.apple.move()
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.X[0], self.snake.Y[0], self.snake.X[i], self.snake.Y[i]):
                self.snake.play_sound("crash")
                raise "Game Over"
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        self.play_background_music()
                        self.snake = Snake(self.surface, 1)
                        self.apple = Apple(self.surface)
                    if not pause:
                        if event.key == K_DOWN:
                            self.snake.move(Direction.DOWN)
                        elif event.key == K_UP:
                            self.snake.move(Direction.UP)
                        elif event.key == K_LEFT:
                            self.snake.move(Direction.LEFT)
                        elif event.key == K_RIGHT:
                            self.snake.move(Direction.RIGHT)
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
                    pygame.display.flip()
            except Exception as e:
                pause = True
                self.show_game_over()
            time.sleep(0.05)

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.X = [SIZE] * length
        self.Y = [SIZE] * length
        self.direction = Direction.RIGHT
        self.length = length
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.X[i], self.Y[i]))
    
    def increase_length(self, size):
        self.play_sound("ding")
        self.length += size
        self.X.append(-1)
        self.Y.append(-1)

    def move(self, side):
        if side == Direction.UP:
            self.direction = Direction.UP
        elif side == Direction.DOWN:
            self.direction = Direction.DOWN
        elif side == Direction.LEFT:
            self.direction = Direction.LEFT
        elif side == Direction.RIGHT:
            self.direction = Direction.RIGHT
        self.draw()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.X[i] = self.X[i - 1]
            self.Y[i] = self.Y[i - 1]

        if self.direction == Direction.RIGHT:
            self.X[0] += SIZE
        elif self.direction == Direction.LEFT:
            self.X[0] -= SIZE
        elif self.direction == Direction.UP:
            self.Y[0] -= SIZE
        elif self.direction == Direction.DOWN:
            self.Y[0] += SIZE
        self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()
