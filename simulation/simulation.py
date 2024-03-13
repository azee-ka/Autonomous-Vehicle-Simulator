import pygame
import random
import sys

class RoadSimulation:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.LANE_COUNT = 6
        self.LANE_WIDTH = self.WIDTH // self.LANE_COUNT
        self.CAR_WIDTH = 40
        self.CAR_HEIGHT = 60
        self.CAR_SPEED = 2
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Create the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Road Simulation')

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Group to hold all sprites
        self.all_sprites = pygame.sprite.Group()

        # Create the controllable car
        self.controllable_car = self.create_controllable_car(self.WIDTH // 2, self.HEIGHT - self.CAR_HEIGHT)

        # Create other cars
        self.other_cars = pygame.sprite.Group()
        for i in range(self.LANE_COUNT):
            for _ in range(3):
                other_car = self.create_other_car(i)
                self.other_cars.add(other_car)
                self.all_sprites.add(other_car)

    def create_controllable_car(self, x, y):
        controllable_car = Car(x, y, self)
        self.all_sprites.add(controllable_car)
        return controllable_car


    def create_other_car(self, lane):
        other_car = OtherCar(lane, self)
        self.all_sprites.add(other_car)
        return other_car

    def run(self):
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

            # Update controllable car only if a direction key is pressed
            if direction:
                self.controllable_car.update(direction)

            # Check for collisions between controllable car and other cars
            collisions = pygame.sprite.spritecollide(self.controllable_car, self.other_cars, False)
            for collision_car in collisions:
                # Prevent sticky overlapping for all directions
                if self.controllable_car.rect.colliderect(collision_car.rect):
                    if direction == "left":
                        self.controllable_car.rect.left = collision_car.rect.right
                    elif direction == "right":
                        self.controllable_car.rect.right = collision_car.rect.left
                    elif direction == "up":
                        self.controllable_car.rect.top = collision_car.rect.bottom
                    elif direction == "down":
                        self.controllable_car.rect.bottom = collision_car.rect.top

                # If collision is from the front or back and the controllable car is not moving, move it back to its previous position
                if direction == "" and (self.controllable_car.rect.colliderect(collision_car.rect) or
                                        (self.controllable_car.prev_x, self.controllable_car.prev_y) == self.controllable_car.rect.center):
                    if self.controllable_car.prev_x < collision_car.rect.centerx:
                        self.controllable_car.rect.right = collision_car.rect.left
                    elif self.controllable_car.prev_x > collision_car.rect.centerx:
                        self.controllable_car.rect.left = collision_car.rect.right
                    elif self.controllable_car.prev_y < collision_car.rect.centery:
                        self.controllable_car.rect.bottom = collision_car.rect.top
                    elif self.controllable_car.prev_y > collision_car.rect.centery:
                        self.controllable_car.rect.top = collision_car.rect.bottom

            # Update other cars
            self.other_cars.update()

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw lanes
            for i in range(1, self.LANE_COUNT):
                pygame.draw.line(self.screen, self.WHITE, (i * self.LANE_WIDTH, 0), (i * self.LANE_WIDTH, self.HEIGHT), 2)

            # Draw all sprites
            self.all_sprites.draw(self.screen)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

        # Quit pygame
        pygame.quit()
        sys.exit()

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, road_simulation):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.road_simulation = road_simulation
        self.prev_x = x
        self.prev_y = y

    def update(self, direction):
        self.prev_x, self.prev_y = self.rect.center

        if direction == "left":
            self.rect.x -= self.road_simulation.CAR_SPEED
        elif direction == "right":
            self.rect.x += self.road_simulation.CAR_SPEED
        elif direction == "up":
            self.rect.y -= self.road_simulation.CAR_SPEED
        elif direction == "down":
            self.rect.y += self.road_simulation.CAR_SPEED

        # Keep the car within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, self.road_simulation.WIDTH - self.road_simulation.CAR_WIDTH))
        self.rect.y = max(0, min(self.rect.y, self.road_simulation.HEIGHT - self.road_simulation.CAR_HEIGHT))



class OtherCar(pygame.sprite.Sprite):
    lane_positions = {}  # Keep track of last spawned car position in each lane
    lane_speeds = {}  # Keep track of the speed of cars in each lane
    
    def __init__(self, lane, road_simulation):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.road_simulation = road_simulation
        self.speed = self.get_lane_speed(self, lane)  # Set the speed attribute
        self.rect.center = self.get_centered_position_in_lane(lane)

    @staticmethod
    def get_lane_speed(self, lane):
        # Get the speed of cars in the lane
        return OtherCar.lane_speeds.get(lane, random.uniform(0.5, 1.5) * self.road_simulation.CAR_SPEED)

    def get_centered_position_in_lane(self, lane):
        # Get the last position of car in the lane
        last_position = OtherCar.lane_positions.get(lane, -self.road_simulation.CAR_HEIGHT)

        # Calculate the centered position
        new_position = last_position + self.road_simulation.CAR_HEIGHT * 2 + random.randint(0, self.road_simulation.CAR_HEIGHT // 2)
        while new_position > self.road_simulation.HEIGHT:
            new_position -= self.road_simulation.HEIGHT

        # Ensure horizontal centering
        new_x = lane * self.road_simulation.LANE_WIDTH + (self.road_simulation.LANE_WIDTH - self.road_simulation.CAR_WIDTH) // 2

        # Adjust position to avoid overlap
        while True:
            collision = False
            for car in self.road_simulation.other_cars:
                if car.rect.colliderect(pygame.Rect(new_x, new_position, self.road_simulation.CAR_WIDTH, self.road_simulation.CAR_HEIGHT)):
                    collision = True
                    break
            if not collision:
                break
            new_position += self.road_simulation.CAR_HEIGHT
            if new_position > self.road_simulation.HEIGHT:
                new_position = 0
                
        OtherCar.lane_positions[lane] = new_position
        OtherCar.lane_speeds[lane] = self.speed

        return (new_x, new_position)

    def update(self):
        self.rect.y += self.speed

        # Reset car position if it goes off the screen
        if self.rect.y > self.road_simulation.HEIGHT:
            self.rect.y = random.randint(-self.road_simulation.HEIGHT, 0)
            self.rect.x = self.get_centered_position_in_lane(self.rect.center[0] // self.road_simulation.LANE_WIDTH)[0]
            self.speed = OtherCar.get_lane_speed(self, self.rect.center[0] // self.road_simulation.LANE_WIDTH)




def main():
    game = RoadSimulation()
    game.run()

if __name__ == "__main__":
    main()
