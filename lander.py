# Lunar Lander in Pygame
# by Barry Bridgens

import pygame
import os, math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class LanderSprite(pygame.sprite.Sprite):

    TURN_RATE = 1

    def __init__(self, image, position, floor):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        pygame.sprite.Sprite.__init__(self)
        color = self.src_image.get_at((0,0)) #we get the color of the upper-left corner pixel
        self.src_image.set_colorkey(color)
        self.x, self.y = position
        self.vx = 0.5
        self.vy = 0
        self.direction = 0
        self.floor = floor
        self.rect = self.src_image.get_rect()

    def left(self):
        self.direction = self.direction + self.TURN_RATE

    def right(self):
        self.direction = self.direction - self.TURN_RATE

    def fire_engine(self):
        rad = self.direction * math.pi / 180
        self.vx -= 0.1 * math.sin(rad)
        self.vy -= 0.1 * math.cos(rad)

    def ground_flatness(self):
        flat_data = []
        data_points = 0
        total = 0
        for x in range(-25, 25):
            xpos = self.x + x
            flat_data.append(self.floor.get_height(xpos))
            data_points = data_points + 1
        for x in range(1, data_points):
            total = total + (flat_data[x] - flat_data[x - 1])
        return(abs(total))

    def landing_ok(self):
        if ((self.vy < 0.6) and (self.vx < 0.4) and (self.vx > -0.4) and
            (self.direction < 3) and (self.direction > -3) and self.ground_flatness() < 5):
            return(True)
        else:
            return(False)

    def update(self, deltat):

        # Gravity
        self.vy = self.vy + 0.01

        # Move
        self.x = self.x + self.vx
        if self.x < 0:
            self.x = 0
            self.vx = 0
        if self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
            self.vx = 0

        self.y = self.y + self.vy
        # Top limit
        if self.y < 0:
            self.y = 0
            self.vy = 0
        # Floor interaction
        if self.y > (SCREEN_HEIGHT - self.floor.get_height(self.x) - (self.rect.height / 2)):
            self.y = (SCREEN_HEIGHT - self.floor.get_height(self.x) - (self.rect.height / 2))
            if self.landing_ok():
                self.vx = 0
                self.vy = 0
            else:
                # Temporary "crash" action
                self.vx = 0.5
                self.vy = 0
                self.x = 50
                self.y = 100
                self.direction = 0

        self.position = (int(self.x), int(self.y))

        # Display
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        #print (self.vx, self.vy, self.direction, self.ground_flatness())


class GroundSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        # Load height data
        (root, ext) = os.path.splitext(image)
        datafile = root + ".dat"
        self.heights = []
        with open (datafile, 'r') as f:
            for line in f:
                self.heights.append(int(line))

    def get_height(self, x):
        if x < len(self.heights):
            h = self.heights[int(x)]
        else:
            h = self.heights[len(self.heights) - 1]
        return(h)

    def update(self, deltat):
        # Display
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT - (self.rect.height / 2)))


ground = GroundSprite('floor.png', (0, SCREEN_HEIGHT))
ground_group = pygame.sprite.RenderPlain(ground)

lander = LanderSprite('lander.png', (50, 100), ground)
lander_group = pygame.sprite.RenderPlain(lander)


#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

pygame.key.set_repeat(50, 50)
 
while done==False:
 
    # This limits the while loop to a max of 30 times per second.
    # Leave this out and we will use all CPU we can.
    deltat = clock.tick(30)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if not hasattr(event, 'key'): continue
        down = event.type == pygame.KEYDOWN     # key down or up?
        if event.key == pygame.K_RIGHT: lander.right()
        elif event.key == pygame.K_LEFT: lander.left()
        elif event.key == pygame.K_UP: lander.fire_engine()
        elif event.key == pygame.K_ESCAPE: done=True     # quit the game


    # RENDERING
    screen.fill((0,0,0))
    ground_group.update(deltat)
    ground_group.draw(screen)
    lander_group.update(deltat)
    lander_group.draw(screen)
    pygame.display.flip()

