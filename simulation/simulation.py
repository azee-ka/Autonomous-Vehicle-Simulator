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
    lane_positions = {}  # Keep track of last spawned car position in each lane
    lane_speeds = {}  # Keep track of the speed of cars in each lane

    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = OtherCar.get_lane_speed(lane)  # Set the speed attribute
        self.rect.center = self.get_centered_position_in_lane(lane)

    @staticmethod
    def get_lane_speed(lane):
        # Get the speed of cars in the lane
        return OtherCar.lane_speeds.get(lane, random.uniform(0.5, 1.5) * CAR_SPEED)

    def get_centered_position_in_lane(self, lane):
        # Get the last position of car in the lane
        last_position = OtherCar.lane_positions.get(lane, -CAR_HEIGHT)

        # Calculate the centered position
        new_position = last_position + CAR_HEIGHT * 2 + random.randint(0, CAR_HEIGHT // 2)
        while new_position > HEIGHT:
            new_position -= HEIGHT

        # Ensure horizontal centering
        new_x = lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2

        # Adjust position to avoid overlap
        while True:
            collision = False
            for car in other_cars:
                if car.rect.colliderect(pygame.Rect(new_x, new_position, CAR_WIDTH, CAR_HEIGHT)):
                    collision = True
                    break
            if not collision:
                break
            new_position += CAR_HEIGHT
            if new_position > HEIGHT:
                new_position = 0
                
        OtherCar.lane_positions[lane] = new_position
        OtherCar.lane_speeds[lane] = self.speed

        return (new_x, new_position)

    def update(self):
        self.rect.y += self.speed

        # Reset car position if it goes off the screen
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, 0)
            self.rect.x = self.get_centered_position_in_lane(self.rect.center[0] // LANE_WIDTH)[0]
            self.speed = OtherCar.get_lane_speed(self.rect.center[0] // LANE_WIDTH)


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

    # Store the current position of the controllable car
    prev_x, prev_y = controllable_car.rect.center

    # Update controllable car only if a direction key is pressed
    if direction:
        controllable_car.update(direction)

    # Check for collisions between controllable car and other cars
    collisions = pygame.sprite.spritecollide(controllable_car, other_cars, False)
    for collision_car in collisions:
        # Prevent sticky overlapping for all directions
        if controllable_car.rect.colliderect(collision_car.rect):
            if direction == "left":
                controllable_car.rect.left = collision_car.rect.right
            elif direction == "right":
                controllable_car.rect.right = collision_car.rect.left
            elif direction == "up":
                controllable_car.rect.top = collision_car.rect.bottom
            elif direction == "down":
                controllable_car.rect.bottom = collision_car.rect.top

        # If collision is from the front or back and the controllable car is not moving, move it back to its previous position
        if direction == "" and (controllable_car.rect.colliderect(collision_car.rect) or
                                (prev_x, prev_y) == controllable_car.rect.center):
            if prev_x < collision_car.rect.centerx:
                controllable_car.rect.right = collision_car.rect.left
            elif prev_x > collision_car.rect.centerx:
                controllable_car.rect.left = collision_car.rect.right
            elif prev_y < collision_car.rect.centery:
                controllable_car.rect.bottom = collision_car.rect.top
            elif prev_y > collision_car.rect.centery:
                controllable_car.rect.top = collision_car.rect.bottom


    # Update other cars
    other_cars.update()

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
