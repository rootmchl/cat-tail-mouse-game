import pygame
import random

# defining colors
BLACK = (0, 0, 0)

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # call the parent class constructor (sprite)
        super().__init__()

        # set the rect attribute of the cat (width/height)
        self.image = pygame.image.load("cat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # stores the current size of the cat
        self.size = (self.rect.width, self.rect.height)

         # initialize the collision detection radius ### (does not work)
        self.radius = 0.1

    def move(self):
        # moves the cat in a random direction
        self.rect.x += random.randint(-3, 3)
        self.rect.y += random.randint(-3, 3)

        # keeps the cat within the screen boundaries (faced an issue where the cat was able to leave the screen)
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

class TailPiece(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # sets the tail piece image
        self.image = pygame.image.load("tail_piece.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # initialize the collision detection radius ### (does not work)
        self.radius = 0.1

class Mouse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # mouse image
        self.image = pygame.image.load("mouse.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        # sets the initial position of the mouse
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

        # initialize the collision detection radius ### (does not work)
        self.radius = 5


    def change_direction(self):
        # changes the direction of the mouse
        self.rect.x += random.randint(-10, 10)
        self.rect.y += random.randint(-25, 25) # the mouse moves way quicker from top to bottom!

        # keeps the mouse within the screen boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

########################################## Initialize Pygame
pygame.init()

# sets the width and height of the screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# sets the game tital and loads background and win/lose images
pygame.display.set_caption("Cat Chase")
background_image = pygame.image.load("background.png").convert()
explosion_image = pygame.image.load("cat_explosion.gif").convert_alpha()
lose_image = pygame.image.load("you_lose.png").convert_alpha()

# list of sprites
all_sprites_list = pygame.sprite.Group()
tail_piece_list = pygame.sprite.Group()
mouse_list = pygame.sprite.Group()

# Set the starting positions of the cat, mouse, and tail pieces
# I ran into an error where sometimes the game would end instantly because of the spawn positions, so this needed to be done
starting_positions = [(100, 100), (200, 200), (300, 300), (400, 400), (500, 500)]
# shuffle the list of starting positions so they are not in the same order ### (unsure if this works)
random.shuffle(starting_positions)

# creates the cat
cat = Cat(20, 20)
all_sprites_list.add(cat)

# gets the current size of the cat
cat_width, cat_height = cat.rect.width, cat.rect.height

# sets the width and height of the rect attribute of the cat to be smaller
new_width, new_height = cat_width * 0.75, cat_height * 0.75
cat.rect.width, cat.rect.height = new_width, new_height

# creates the tail pieces
for i in range(10):
    # generates a random position for the tail piece within the screen boundaries
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)

    tail_piece = TailPiece(x, y)
    tail_piece_list.add(tail_piece)
    all_sprites_list.add(tail_piece)

# creates the mouse
mouse = Mouse(5,5)
mouse_list.add(mouse)
all_sprites_list.add(mouse)

# loop until the user clicks the close button.
done = False

# used to manage how fast the screen updates
clock = pygame.time.Clock()

#main
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    mouse.change_direction()

    #game logic

    # get the list of keys currently being pressed and update the cat's position accordingly, W = Up, A = Left, S = Down, D = Right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cat.rect.y -= 3
    if keys[pygame.K_a]:
        cat.rect.x -= 3
    if keys[pygame.K_s]:
        cat.rect.y += 3
    if keys[pygame.K_d]:
        cat.rect.x += 3

    # updates position of cat
    cat.move()

    # draw the cat's image on the screen
    screen.blit(cat.image, cat.rect)

    # check if the cat has collected any tail pieces
    tail_piece_hit_list = pygame.sprite.spritecollide(cat, tail_piece_list, True)
    for tail_piece in tail_piece_hit_list:
        if pygame.sprite.collide_circle_ratio(0.5)(cat, tail_piece): #this method checks if rectangles of the two objects are intersecting, and returns "true" if they are, and "false" otherwise. this needed to be done because the radius at which collisions were being detected was too large.
            tail_piece_list.remove(tail_piece)    
            all_sprites_list.remove(tail_piece)

    # checks for collisions between the cat and the mouse
    mouse_hit_list = pygame.sprite.spritecollide(cat, mouse_list, False)
    pygame.sprite.collide_circle_ratio(0.5)

    # drawing
    screen.fill(BLACK)
    screen.blit(background_image, [0, 0])

    all_sprites_list.draw(screen)
    cat.image = pygame.transform.scale(cat.image, (cat.rect.width // 4, cat.rect.height // 4))

    # updates the screen
    pygame.display.flip()

    # limits frames per second
    clock.tick(60)

    # checks if the cat has collected all the tail pieces or collided with the mouse
    if len(tail_piece_list) == 0 or len(mouse_hit_list) > 0:
        # checks if the cat has won or lost the game, and displays the appropriate image for 5 seconds before aborting
        if len(tail_piece_list) == 0:
            # the cat has collected all pieces of its tail, display the cat explosion image
            screen.blit(explosion_image, [0, 0])
        else:
            # the cat has collided with the mouse, display the "YOU LOSE" image
            screen.blit(lose_image, [0, 0])

        # updates the screen
        pygame.display.flip()

        # waits for 5 seconds
        pygame.time.delay(5000)

        # closes the game
        done = True

