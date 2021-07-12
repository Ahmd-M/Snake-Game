
import pygame, sys, random

pygame.init()
pygame.font.init()


FPS = 40
DIRECTIONS = (LEFT ,UP ,RIGHT, DOWN) = ((-1,0),(0,-1),(1,0),(0,1)) # --> (dx/dy,dy/dx)
SIZE = (WIDTH ,HEIGHT) = 500, 500
SCREEN = pygame.display.set_mode(SIZE)
SURFACE = pygame.Surface(SCREEN.get_size()).convert()
ICON = None
SQ_NUM = 25 #Numbers of squares in height or width (Better be a multiple of 5)
SQ_SIZE = (WIDTH//SQ_NUM,HEIGHT//SQ_NUM)
SCORE_FONT = pygame.font.SysFont('comicsans',40)
ICON = pygame.image.load('Images/snake_icon.png').convert_alpha()
pygame.display.set_icon(ICON)
pygame.display.set_caption('Snake Game') 

#Colors
BLACK = (0,0,0)
DIM_GREY = (105,105,105)
RED = (255,0,0)
LIGHT_CYAN = (93,216,228)
CYAN = (84,194,205)


class Game(object):
    def __init__(self,screen,surface,screen_size,sq_num) -> None:
        self.screen = screen
        self.surface = surface
        self.sq_num = sq_num
        self.sq_size = (screen_size[0]//self.sq_num, screen_size[1]//self.sq_num)

    def draw(self):
        self.screen.blit(self.surface,(0,0))
        for row in range(self.sq_num):
            for column in range(self.sq_num):
                if (row + column) % 2 == 0:
                    self.create_square(LIGHT_CYAN ,(row,column))
                else:
                    self.create_square(CYAN ,(row,column))

    def create_square(self,color,coordinates):
        x,y = coordinates
        square = pygame.Rect((x * self.sq_size[0], y * self.sq_size[1]), self.sq_size)
        pygame.draw.rect(self.surface,color, square)

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

class Snake():
    def __init__(self,position,color,head_color) -> None:
        self.head_position_0 = position
        self.head_color = head_color
        self.color = color
        self.length = 1
        self.direction = random.choice(DIRECTIONS)
        self.body_positions = [position]
        
    def move(self,count):
        if count % 4 != 0:
            return
        x,y = self.direction
        current_head_position = self.get_head_position()
        new_head_position = (current_head_position[0] + x*SQ_SIZE[0] ,current_head_position[1] + y*SQ_SIZE[1]) #Square after head (In same direction)

        if len(self.body_positions) > 3 and new_head_position in self.body_positions[2:]: #Snake collides its body
            self.reset() 
        elif not (0 <= new_head_position[0] < WIDTH) or not (0 <= new_head_position[1] < HEIGHT): #Out of screen
            self.reset()
        else:
            self.body_positions.insert(0,new_head_position)
            if len(self.body_positions) > self.length:
                self.body_positions.pop()
        
    def turn(self,direction):
        x,y = direction
        if not (self.length > 1 and (x*-1,y*-1) ==  self.direction): #Prevents player from moving in opposite direction of the head
            self.direction = direction #Changes direction
        

    def draw(self,count):
        for position in self.body_positions:
            self.create_draw_rect(position,self.color)
            if self.body_positions.index(position) > 0:
                continue #Colors the head with different color
            self.create_draw_rect(position,self.head_color)
        self.move(count)

    def reset(self):
        self.length = 1
        self.direction = random.choice(DIRECTIONS)
        self.body_positions = [self.head_position_0]

    def create_draw_rect(self,coordinates,color):
        rect = pygame.Rect(coordinates, SQ_SIZE)
        pygame.draw.rect(SURFACE, color, rect)
        pygame.draw.rect(SURFACE, (93,216, 228), rect, 1)

    def draw_score(self):
        score_surface = SCORE_FONT.render(f'Score: {self.length-1}',True,BLACK)
        score_rect = score_surface.get_rect(center = (WIDTH//2,1.5*SQ_SIZE[0]))
        SCREEN.blit(score_surface,score_rect)
        

    def get_head_position(self):
        return self.body_positions[0]

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self) -> None:
        self.update_position()
        self.color = (255,0,0)

    def draw(self):
        pygame.draw.rect(SURFACE, self.color, self.create(self.position))

    def create(self,coordinates):
        rect = pygame.Rect(coordinates, SQ_SIZE)
        return rect
        
    def update_position(self):
        self.sq_position = (random.randint(0,SQ_NUM-1),random.randint(0,SQ_NUM-1))
        self.position = (self.sq_position[0]*SQ_SIZE[0],self.sq_position[1]*SQ_SIZE[1])
        
game = Game(SCREEN,SURFACE,SIZE,SQ_NUM)
snake = Snake(((SQ_NUM//2)*SQ_SIZE[0],(SQ_NUM//2)*SQ_SIZE[1]),DIM_GREY,BLACK)
food = Food()

def main():
    clock = pygame.time.Clock()
    count = 0

    while True:
        count += 1
        game.draw()
        snake.draw(count)
        snake.draw_score()
        food.draw()
        snake.handle_keys()
        if food.position == snake.get_head_position():
            snake.length += 1
            food.update_position()


        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
