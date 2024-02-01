import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()

# Variables
CELL_SIZE = 30 # Change the screen into a imagine Grid
CELL_NUM = 20
FPS = 60

# Colors
SURFACE_COLOR = (167, 201, 87)
FRUIT_COLOR = (40, 54, 24)
SNAKE_COLOR = (231, 111, 81)

# Window screen 500 x 500
screen = pygame.display.set_mode(
    (CELL_SIZE * CELL_NUM, CELL_SIZE * CELL_NUM)) 

clock = pygame.time.Clock() # For the FPS  

# Trigger user input every 100 milisec
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

class FRUIT:
    def __init__(self):
            self.randomFruit()
    
    def randomFruit(self):
        self.x = random.randint(0, CELL_NUM - 1)
        self.y = random.randint(0, CELL_NUM - 1)
        self.pos = Vector2(self.x, self.y)
        # For x and y position
    
    def draw_fruit(self):
        x_pos = self.pos.x * CELL_SIZE
        y_pos = self.pos.y * CELL_SIZE
        fruit_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        # Draw the rectangle for the fruit 
        pygame.draw.rect(screen, FRUIT_COLOR, fruit_rect)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        # Length of snake from begin = 3
        self.direction = Vector2(1,0)
        # Move from the right when begin the game
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, block_rect)
    
    def movement(self):
        # We copy all the first Vector except the last one
        # And insert the new Vector (as the head of the snake)
        # and take the player input to move the snake
        # finally return to the body
        
        if self.new_block == True: 
            body_copy = self.body[:] 
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] 
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class LOGIC:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.movement()
        self.snakeEatfruit()
        self.check_collision()
        

    def drawing(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def snakeEatfruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomFruit()
            self.snake.add_block()

    def check_collision(self):
        self.snakehead = self.snake.body[0]
        # Snake hit Wall
        if self.snakehead.x < 0 or self.snakehead.x > (CELL_NUM - 1) or self.snakehead.y < 0 or self.snakehead.y > (CELL_NUM - 1):
            self.endgame()
        
        # Snake hit itself
        for block in self.snake.body[1:]: #Take from the second
            if block == self.snakehead:
                self.endgame()

    def endgame(self):
        pygame.quit()
        sys.exit()
    
# For Class
logic = LOGIC()

# This loop will run through the game
# Make this as clean as possible
while True:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit the game
            pygame.quit()
            sys.exit() 

        if event.type == SCREEN_UPDATE:
            logic.update()

        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_w):
                if(logic.snake.direction.y != 1): # Avoid press W can press S (you can kys :<)
                    logic.snake.direction = Vector2(0,-1)
            elif(event.key == pygame.K_s):
                if(logic.snake.direction.y != -1):
                    logic.snake.direction = Vector2(0,1)
            elif(event.key == pygame.K_d):
                if(logic.snake.direction.x != -1):
                    logic.snake.direction = Vector2(1,0)
            elif(event.key == pygame.K_a):
                if(logic.snake.direction.x != 1):
                    logic.snake.direction = Vector2(-1,0)
    
    screen.fill(SURFACE_COLOR)
    logic.drawing()
    pygame.display.update()
    clock.tick(FPS)     

