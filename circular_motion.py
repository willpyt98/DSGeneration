import pygame
import math

pygame.display.set_caption("Planet Simulation")

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
PI = math.pi
COS = math.cos
SIN = math.sin
HEIGHT = 128
WIDTH = 128

class Circular_motion:
    def __init__(self, angle, radius, size, color, velocity, dt):
        self.angle = angle
        self.radius = radius
        self.size = size
        self.color = color
        self.velocity = velocity
        self.dt = dt
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, (HEIGHT / 2 + int(SIN(self.angle)*self.radius), WIDTH/2 - int(COS(self.angle)*self.radius)), int(self.size))

    def update_position(self):
        self.angle = self.angle + self.velocity * self.dt

def main():
    window = pygame.display.set_mode((HEIGHT, WIDTH))
    window.fill(BLACK)
    ball = Circular_motion(angle=0, radius = 10, size = 3, color=WHITE, velocity = PI/3, dt = 1 / 30)
    clock = pygame.time.Clock()
    count = 0
    run = True

    while count < 180 and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ball.draw(window)
        ball.update_position()
        
        clock.tick(30)
        pygame.image.save(window, "images/test" + str(count) + ".jpg")
        pygame.display.flip()
        window.fill(BLACK)

        count +=1

if __name__ == "__main__":
    main()
