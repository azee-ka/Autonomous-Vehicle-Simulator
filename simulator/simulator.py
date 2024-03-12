import pygame
import random

class Simulator:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Autonomous Vehicle Simulator")

        self.clock = pygame.time.Clock()

        self.is_running = False
        self.collision = False

        self.car_x = self.width // 2
        self.car_y = self.height - 100
        self.car_width = 40
        self.car_height = 80
        self.car_speed = 5

        self.obstacle_width = 80
        self.obstacle_height = 20
        self.obstacle_speed = 3

        self.obstacle_x = random.randint(0, self.width - self.obstacle_width)
        self.obstacle_y = -self.obstacle_height

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
            pygame.draw.rect(self.screen, (0, 0, 255), (self.car_x, self.car_y, self.car_width, self.car_height))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height))
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
        if self.car_x > self.width - self.car_width:
            self.car_x = self.width - self.car_width

    def move_obstacle(self):
        self.obstacle_y += self.obstacle_speed
        if self.obstacle_y > self.height:
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

    def check_collision(self):
        if self.car_x < self.obstacle_x + self.obstacle_width and self.car_x + self.car_width > self.obstacle_x \
                and self.car_y < self.obstacle_y + self.obstacle_height and self.car_y + self.car_height > self.obstacle_y:
            self.collision = True
            self.car_x = self.width // 2
            self.car_y = self.height - 100
            self.obstacle_y = -self.obstacle_height
            self.obstacle_x = random.randint(0, self.width - self.obstacle_width)

if __name__ == "__main__":
    sim = Simulator()
    sim.run()
