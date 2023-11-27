import pygame
import math
import numpy as np
import os 
import argparse


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
g = 9.8
LENGTH = 1.0
PI = math.pi
COS = math.cos
SIN = math.sin
HEIGHT = 128
WIDTH = 128
np.random.seed(seed = 2023)


class Single_pendulum:

    def __init__(self, theta, omega, Nx, Ny, l, size, color, dt):
        self.theta = theta
        self.omega = omega
        self.Nx = Nx
        self.Ny = Ny
        self.l = l
        self.size = size
        self.color = color
        self.dt = dt
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.Nx + SIN(self.theta)*self.l), int(self.Ny + COS(self.theta)*self.l)), int(self.size))

    def ode(self,theta, omega):
        theta_dot = omega
        omega_dot = - g * SIN(theta) / LENGTH

        return np.array([theta_dot, omega_dot])
    
    def update_position(self):
        y = np.array([self.theta, self.omega])
        k1 = self.ode(*y)
        k2 = self.ode(*(y + self.dt * k1 / 2))
        k3 = self.ode(*(y + self.dt * k2 / 2))
        k4 = self.ode(*(y + self.dt * k3))

        y_dot = 1.0 / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.theta = self.theta + self.dt * y_dot[0]
        self.omega = self.omega + self.dt * y_dot[1]

def plot_trajectory(initial_condition, traj_length, dt, save_path):

    theta = initial_condition[0]
    omega = initial_condition[1]

    window = pygame.display.set_mode((HEIGHT, WIDTH))
    window.fill(BLACK)
    pendulum = Single_pendulum(theta = theta, omega=omega, Nx = HEIGHT/2, Ny = WIDTH/2, l=50, size=5, color=WHITE, dt=dt)
    clock = pygame.time.Clock()
    count = 0
    run = True

    while count < traj_length and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pendulum.draw(window)
        pendulum.update_position()
        
        clock.tick(30)
        pygame.image.save(window, save_path + str(count) + ".jpg")
        pygame.display.flip()
        window.fill(BLACK)

        count +=1

if __name__ == "__main__":
    initial_conditions = np.random.uniform(-PI, PI,1000)
    for i in range(1000):
        initial_condition = [initial_conditions[i], 0]
        traj_length = 120
        dt = 1 / 30
        save_path = "./dataset/simple_pendulum/" + str(i) + "/"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plot_trajectory(initial_condition, traj_length, dt, save_path)
