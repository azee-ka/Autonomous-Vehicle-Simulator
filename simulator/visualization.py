import pygame
import random

class Visualization:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AutoDriveSim")

        self.clock = pygame.time.Clock()

        self.is_running = False
        self.collision = False

        self.car_image = pygame.image.load("car_image.png")  # Load car image
        self.car_rect = self.car_image.get_rect()
        self.car_x = self.width // 2
        self.car_y = self.height - 100
        self.car_speed = 5

        self.obstacle_image = pygame.image.load("obstacle_image.png")  # Load obstacle image
        self.obstacle_rect = self.obstacle_image.get_rect()
        self.obstacle_width = self.obstacle_rect.width
        self.obstacle_height = self.obstacle_rect.height
        self.obstacle_speed = 3

        self.obstacle_x = random.randint(0, self.width - self.obstacle_width)
        self.obstacle_y = -self.obstacle_height

        self.traffic_light_image = pygame.image.load("traffic_light_image.png")  # Load traffic light image
        self.traffic_light_rect = self.traffic_light_image.get_rect()
        self.traffic_light_x = self.width // 2 - self.traffic_light_rect.width // 2
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
            self.car_x -= self.car_speed
        if keys[pygame.K_RIGHT]:
            self.car_x += self.car_speed

        if self.car_x < 0:
            self.car_x = 0
        if self.car_x > self.width - self.car_rect.width:
            self.car_x = self.width - self.car_rect.width

    def move_obstacle(self):
        self.obstacle_y += self.obstacle_speed
        if self.obstacle_y > self.height:
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

    def check_collision(self):
        if self.car_x < self.obstacle_x + self.obstacle_width and self.car_x + self.car_rect.width > self.obstacle_x \
                and self.car_y < self.obstacle_y + self.obstacle_height and self.car_y + self.car_rect.height > self.obstacle_y:
            self.collision = True
            self.car_x = self.width // 2
            self.car_y = self.height - 100
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

if __name__ == "__main__":
    vis = Visualization()
    vis.run()
