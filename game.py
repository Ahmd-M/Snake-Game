import pygame, sys, random ,json

pygame.init()
pygame.font.init()


#Game constants (UI)
SIZE = (WIDTH, HEIGHT) = 500, 500
SCREEN = pygame.display.set_mode(SIZE)
SURFACE = pygame.Surface(SCREEN.get_size()).convert()
SCORE_FONT = pygame.font.SysFont('comicsans' ,40)
ICON = pygame.image.load('Images/snake_icon.png').convert_alpha()

pygame.display.set_icon(ICON)
pygame.display.set_caption('Snake Game') 

FPS = 40
SQ_NUM = 25 #Numbers of squares in height or width (Better be a multiple of 5)
SQ_SIZE = (WIDTH//SQ_NUM, HEIGHT//SQ_NUM)
DIRECTIONS = (LEFT ,UP ,RIGHT, DOWN) = ((-1, 0), (0, -1), (1, 0), (0, 1)) # --> (dx/dy, dy/dx) 

#Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (84, 194, 205)
DIM_GREY = (105, 105, 105)
LIGHT_CYAN = (93, 216, 228)

try:
    with open('storage.txt', 'r') as storage_file:
        data =  json.load(storage_file)
        high_score = data['High score']
except:
        high_score = 0


class Game(object):
    def __init__(self, screen, surface, screen_size, sq_num) -> None:
        self.screen = screen
        self.sq_num = sq_num
        self.surface = surface
        self.sq_size = (screen_size[0]//self.sq_num, screen_size[1]//self.sq_num)

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
        for row in range(self.sq_num):
            for column in range(self.sq_num):
                if (row + column) % 2 == 0:
                    self.create_square(LIGHT_CYAN, (row, column))
                else:
                    self.create_square(CYAN, (row, column))

    def create_square(self, color, coordinates):
        x,y = coordinates
        square = pygame.Rect((x * self.sq_size[0], y * self.sq_size[1]), self.sq_size)
        pygame.draw.rect(self.surface, color, square)

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

class Snake():
    def __init__(self, position, color, head_color, high_score) -> None:
        self.length = 1 
        self.color = color
        self.head_color = head_color
        self.high_score = high_score 
        self.head_position_0 = position
        self.body_positions = [position] 
        self.direction = random.choice(DIRECTIONS)
        
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
            self.body_positions.insert(0, new_head_position)
            if len(self.body_positions) > self.length:
                self.body_positions.pop()
        
    def turn(self,direction):
        x,y = direction
        if not (self.length > 1 and (x*-1, y*-1) ==  self.direction): #Prevents player from moving in opposite direction of the head
            self.direction = direction #Changes direction
        
    def draw(self, count):
        for position in self.body_positions:
            self.create_draw_rect(position, self.color)
            if self.body_positions.index(position) > 0:
                continue #Colors the head with different color
            self.create_draw_rect(position, self.head_color)
        self.move(count)

    def reset(self):
        self.length = 1
        self.direction = random.choice(DIRECTIONS)
        self.body_positions = [self.head_position_0]

    def create_draw_rect(self, coordinates,color):
        rect = pygame.Rect(coordinates, SQ_SIZE)
        pygame.draw.rect(SURFACE, color, rect)
        pygame.draw.rect(SURFACE, (93,216, 228), rect, 1)

    def draw_score(self):
        self.update_scores()
        score_surface = SCORE_FONT.render(f'Score: {self.length-1}', True,BLACK)
        high_score_surface = SCORE_FONT.render(f'High score: {self.high_score}', True,BLACK)
        score_rect = score_surface.get_rect(center = (WIDTH//2, 3*SQ_SIZE[0]))
        high_score_rect = high_score_surface.get_rect(center = (WIDTH//2, 1.5*SQ_SIZE[0]))
        
        SCREEN.blit(score_surface, score_rect)
        SCREEN.blit(high_score_surface, high_score_rect)

    def update_scores(self):
        if self.length-1 > self.high_score:
            self.high_score = self.length-1
        data = {
            'High score' : self.high_score
        }
        with open('storage.txt', 'w') as storage_file:
            json.dump(data, storage_file)

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
        self.color = RED

    def draw(self):
        pygame.draw.rect(SURFACE, self.color, self.create(self.position))

    def create(self,coordinates):
        rect = pygame.Rect(coordinates, SQ_SIZE)
        return rect
        
    def update_position(self):
        self.sq_position = (random.randint(0, SQ_NUM-1), random.randint(0,SQ_NUM-1))
        self.position = (self.sq_position[0]*SQ_SIZE[0], self.sq_position[1]*SQ_SIZE[1])
        

game = Game(SCREEN, SURFACE, SIZE,SQ_NUM)
snake = Snake(((SQ_NUM//2)*SQ_SIZE[0], (SQ_NUM//2)*SQ_SIZE[1]), DIM_GREY, BLACK, high_score)
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
