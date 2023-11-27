import pygame
import math
import numpy as np
import os

"""
Plot a spiral 
x_dot = A*x, where A = [-1 2
                        -2 -1]
                <=> (x_dot, y_dot) = (-x+2y, -2x -y)
"""

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
np.random.seed(seed = 2023)


class Spiral_motion:
    def __init__(self, x, y, size, color, dt):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dt = dt
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(HEIGHT/2 + self.x*HEIGHT/2), int(WIDTH/2 - self.y*WIDTH/2)), int(self.size))

    def ode(self,x, y):
        x_dot =  -x + 2*y
        y_dot = -2*x - y
        return np.array([x_dot,y_dot])

    def update_position(self):
        y = np.array([self.x, self.y])
        k1 = self.ode(*y)
        k2 = self.ode(*(y + self.dt * k1 / 2))
        k3 = self.ode(*(y + self.dt * k2 / 2))
        k4 = self.ode(*(y + self.dt * k3))

        y_dot = 1.0 / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.x = self.x + self.dt * y_dot[0]
        self.y = self.y + self.dt * y_dot[1]
        

def  plot_trajectory(initial_condition, traj_length, dt, save_path):
    window = pygame.display.set_mode((HEIGHT, WIDTH))
    window.fill(BLACK)
    ball = Spiral_motion(x=initial_condition[0],y=initial_condition[1], size = 5, color=WHITE, dt = 1 / 30)
    clock = pygame.time.Clock()
    count = 0
    run = True

    while count < traj_length and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ball.draw(window)
        ball.update_position()
        
        clock.tick(30)
        pygame.image.save(window, save_path + str(count) + ".jpg")
        pygame.display.flip()
        window.fill(BLACK)

        count +=1

if __name__ == "__main__":
    initial_conditions = np.random.uniform(0.5,0.9, [1000,2]) * (np.random.randint(2, size=[1000,2])*2-1)
    for i in range(1000):
        initial_condition =initial_conditions[i]
        traj_length = 60
        dt = 1 / 30
        save_path = "./dataset/spiral_2/" + str(i) + "/"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plot_trajectory(initial_condition, traj_length, dt, save_path)
