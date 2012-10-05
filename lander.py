# My Lunar Lander in Pygame

import pygame


screen = pygame.display.set_mode((800, 600))


class LanderSprite(pygame.sprite.Sprite):

    TURN_RATE = 2

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.vx = 0.5
        self.vy = 0
        self.direction = 0

    def left(self):
        self.direction = self.direction + self.TURN_RATE

    def right(self):
        self.direction = self.direction - self.TURN_RATE

    def fire_engine(self):
        pass

    def update(self, deltat):

        # Gravity
        self.vy = self.vy + 0.01

        # Move
        self.x = self.x + self.vx
        if self.y > 0:
            self.y = self.y + self.vy

        self.position = (int(self.x), int(self.y))

        # Display
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



lander = LanderSprite('lander.png', (50, 100))
lander_group = pygame.sprite.RenderPlain(lander)


#Loop until the user clicks the close button.
done=False
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
    lander_group.update(deltat)
    lander_group.draw(screen)
    pygame.display.flip()

