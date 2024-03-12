import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
LANE_COUNT = 6
LANE_WIDTH = WIDTH // LANE_COUNT
CAR_WIDTH = 40
CAR_HEIGHT = 60
CAR_SPEED = 2
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Road Simulation')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Define a class for the controllable car
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, direction):
        if direction == "left":
            self.rect.x -= CAR_SPEED
        elif direction == "right":
            self.rect.x += CAR_SPEED
        elif direction == "up":
            self.rect.y -= CAR_SPEED
        elif direction == "down":
            self.rect.y += CAR_SPEED

        # Keep the car within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - CAR_WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - CAR_HEIGHT))

# Define a class for the other cars
class OtherCar(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(lane * LANE_WIDTH, (lane + 1) * LANE_WIDTH - CAR_WIDTH), random.randint(-HEIGHT, 0))
        self.speed = random.uniform(0.5, 1.5) * CAR_SPEED

    def update(self):
        self.rect.y += self.speed

        # Reset car position if it goes off the screen
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, 0)
            self.rect.x = random.randint(self.rect.x, self.rect.x + CAR_WIDTH)
            self.speed = random.uniform(0.5, 1.5) * CAR_SPEED

# Group to hold all sprites
all_sprites = pygame.sprite.Group()

# Create the controllable car
controllable_car = Car(WIDTH // 2, HEIGHT - CAR_HEIGHT)
all_sprites.add(controllable_car)

# Create other cars
other_cars = pygame.sprite.Group()
for i in range(LANE_COUNT):
    for _ in range(3):
        other_car = OtherCar(i)
        other_cars.add(other_car)
        all_sprites.add(other_car)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get user input for controllable car
    keys = pygame.key.get_pressed()
    direction = ""
    if keys[pygame.K_LEFT]:
        direction = "left"
    if keys[pygame.K_RIGHT]:
        direction = "right"
    if keys[pygame.K_UP]:
        direction = "up"
    if keys[pygame.K_DOWN]:
        direction = "down"

    # Update controllable car
    controllable_car.update(direction)

    # Update other cars
    other_cars.update()

    # Check for collisions between controllable car and other cars
    if pygame.sprite.spritecollide(controllable_car, other_cars, False):
        print("Collision detected!")

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw lanes
    for i in range(1, LANE_COUNT):
        pygame.draw.line(screen, WHITE, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 2)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
