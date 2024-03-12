import pygame
import random
import math
import os
# from visualization import Visualization

class Simulator:
    def __init__(self, width=800, height=600):
        self.visualization = Visualization(width, height)
        self.car_x = 0
        self.car_y = 0
        self.car_speed = 1

    def move_car(self):
        self.car_x += self.car_speed

    def run_simulation(self):
        self.visualization.run()
        
        
        
class Visualization:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AutoDriveSim")

        self.clock = pygame.time.Clock()

        self.is_running = False
        self.collision = False

        self.car_image = pygame.image.load(os.path.join("assets", "car_image.png"))
        self.obstacle_image = pygame.image.load(os.path.join("assets", "obstacle_image.png"))
        self.traffic_light_image = pygame.image.load(os.path.join("assets", "traffic_light_image.png"))

        self.car_image = pygame.transform.scale(self.car_image, (40, 80))
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (80, 20))
        self.traffic_light_image = pygame.transform.scale(self.traffic_light_image, (40, 40))

        self.car_x = self.width // 2
        self.car_y = self.height - 100
        self.car_speed = 5
        self.car_direction = 0

        self.obstacle_width = 80
        self.obstacle_height = 20
        self.obstacle_speed = 3

        self.obstacle_x = random.randint(0, self.width - self.obstacle_width)
        self.obstacle_y = -self.obstacle_height

        self.traffic_light_x = self.width // 2 - self.traffic_light_image.get_width() // 2
        self.traffic_light_y = 50
        self.traffic_light_state = "red"

    def run(self):
        self.is_running = True
        while self.is_running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            self.move_car()
            self.move_obstacle()
            self.check_collision()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.car_image, (self.car_x, self.car_y))
            self.screen.blit(self.obstacle_image, (self.obstacle_x, self.obstacle_y))
            if self.traffic_light_state == "red":
                self.screen.blit(self.traffic_light_image, (self.traffic_light_x, self.traffic_light_y))

            pygame.display.flip()

        pygame.quit()

    def move_car(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.car_direction += 5  # Rotate counterclockwise by 5 degrees
        if keys[pygame.K_RIGHT]:
            self.car_direction -= 5  # Rotate clockwise by 5 degrees

        self.car_direction %= 360  # Ensure direction stays within 0 to 360 degrees

        angle_rad = math.radians(self.car_direction)  # Convert angle to radians

        self.car_x += self.car_speed * math.cos(angle_rad)
        self.car_y -= self.car_speed * math.sin(angle_rad)  # Negative since y-coordinates increase downwards

        if self.car_x < 0:
            self.car_x = self.width
        if self.car_x > self.width:
            self.car_x = 0
        if self.car_y < 0:
            self.car_y = self.height
        if self.car_y > self.height:
            self.car_y = 0

    def move_obstacle(self):
        self.obstacle_y += self.obstacle_speed
        if self.obstacle_y > self.height:
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

    def check_collision(self):
        if self.car_x < self.obstacle_x + self.obstacle_width and self.car_x + self.car_image.get_width() > self.obstacle_x \
                and self.car_y < self.obstacle_y + self.obstacle_height and self.car_y + self.car_image.get_height() > self.obstacle_y:
            self.collision = True
            self.car_x = self.width // 2
            self.car_y = self.height - 100
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

if __name__ == "__main__":
    sim = Simulator()
    sim.run_simulation()