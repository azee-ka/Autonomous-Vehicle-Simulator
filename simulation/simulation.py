# simulation/simulation.py

import pygame
import random
import sys
import numpy as np

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



         # Vision parameters
        self.vision_radius = 50  # Radius of the vision circle
        self.vision_color = (0, 255, 0, 50)  # Green with transparency
        
        
        
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


    def get_vision_data(self):
        # Get the position of the car
        car_center_x, car_center_y = self.controllable_car.rect.center

        # Create a vision circle around the car
        vision_circle = pygame.Surface((self.vision_radius * 2, self.vision_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(vision_circle, self.vision_color, (self.vision_radius, self.vision_radius), self.vision_radius)

        # Get the alpha values of the vision circle
        vision_data = pygame.PixelArray(vision_circle)
        alpha_values = [vision_data[x, y] & 0xff for x in range(self.vision_radius * 2) for y in range(self.vision_radius * 2)]

        # Convert alpha values to coordinates relative to the car's center
        vision_coordinates = np.argwhere(np.array(alpha_values) > 0) - [self.vision_radius, self.vision_radius]
        vision_coordinates += [car_center_x, car_center_y]

        # Normalize vision coordinates
        vision_coordinates_norm = vision_coordinates / self.HEIGHT

        # Ensure vision data has the correct shape
        vision_data_shape = vision_coordinates_norm.shape
        if len(vision_data_shape) == 1:
            vision_coordinates_norm = vision_coordinates_norm.reshape(1, -1)

        return vision_coordinates_norm



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
            direction_x = 0
            direction_y = 0
            if keys[pygame.K_LEFT]:
                direction_x = -1
            if keys[pygame.K_RIGHT]:
                direction_x = 1
            if keys[pygame.K_UP]:
                direction_y = -1
            if keys[pygame.K_DOWN]:
                direction_y = 1

            # Update controllable car
            self.controllable_car.update(direction_x, direction_y)

            # Check for collisions between controllable car and other cars
            for other_car in self.other_cars:
                if self.controllable_car.rect.colliderect(other_car.rect):
                    self.controllable_car.handle_collision(other_car)

            # Update other cars
            for other_car in self.other_cars:
                other_car.update()

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

    def update(self, direction_x, direction_y):
        self.prev_x, self.prev_y = self.rect.center

        self.rect.x += direction_x * self.road_simulation.CAR_SPEED
        self.rect.y += direction_y * self.road_simulation.CAR_SPEED

        # Keep the car within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, self.road_simulation.WIDTH - self.road_simulation.CAR_WIDTH))
        self.rect.y = max(0, min(self.rect.y, self.road_simulation.HEIGHT - self.road_simulation.CAR_HEIGHT))


    def check_collision(self, other_car):
        return self.rect.colliderect(other_car.rect)

    def handle_collision(self, other_car):
        # Check the direction of the collision
        dx = other_car.rect.centerx - self.rect.centerx
        dy = other_car.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            # Horizontal collision
            if dx > 0:
                self.rect.right = other_car.rect.left
            else:
                self.rect.left = other_car.rect.right
        else:
            # Vertical collision
            if dy > 0:
                self.rect.bottom = other_car.rect.top
            else:
                self.rect.top = other_car.rect.bottom

        # Additional logic for specific collisions
        if self.rect.right >= other_car.rect.left and self.prev_x < other_car.rect.left:
            # Side collision from the left
            self.rect.right = other_car.rect.left
        elif self.rect.left <= other_car.rect.right and self.prev_x > other_car.rect.right:
            # Side collision from the right
            self.rect.left = other_car.rect.right
        elif self.rect.bottom >= other_car.rect.top and self.prev_y < other_car.rect.top:
            # Back collision
            self.rect.bottom = other_car.rect.top
        elif self.rect.top <= other_car.rect.bottom and self.prev_y > other_car.rect.bottom:
            # Front collision with other car's back
            self.rect.top = other_car.rect.bottom

    def drag_backwards(self, other_car):
        # Calculate the new position based on the other car's position
        self.rect.top = other_car.rect.bottom

        # Keep moving the car back while there is a collision
        while any(self.rect.colliderect(car.rect) for car in self.road_simulation.all_sprites if car != self):
            self.rect.y -= other_car.rect.y  # Move the car up

            # Reposition if the car reaches the end of the canvas
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > self.road_simulation.HEIGHT:
                self.rect.bottom = self.road_simulation.HEIGHT

            # If the car reaches the top without finding a clear spot, stop moving
            if self.rect.top == 0:
                break

        # Reposition if the car reaches the end of the canvas
        if self.rect.right > self.road_simulation.WIDTH:
            self.rect.right = self.road_simulation.WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0




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
