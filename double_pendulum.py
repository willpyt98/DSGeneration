import pygame
import math
import numpy as np
import os 
import argparse
import time


pygame.display.set_caption("Double pendulum Simulation")

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


class double_pendulm:

    def __init__(self, theta1, omega1, theta2, omega2, l1, l2, m1, m2, g, Nx, Ny, l, size, color, dt):
        self.theta1 = theta1
        self.omega1 = omega1
        self.theta2 = theta2
        self.omega2 = omega2
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.g = g
        self.Nx = Nx
        self.Ny = Ny
        self.l = l
        self.size = size
        self.color = color
        self.dt = dt

    def draw(self, window):
        # self.theta1 = np.pi /3
        # self.theta2 = np.pi/2
        x1 = SIN(self.theta1)*self.l
        y1 = COS(self.theta1)*self.l
        x2 = x1 + SIN(self.theta2)*self.l
        y2 = y1 + COS(self.theta2)*self.l
        pygame.draw.circle(window, self.color, (int(self.Nx + x1), int(self.Ny + y1)), int(self.size))
        pygame.draw.circle(window, self.color, (int(self.Nx + x2), int(self.Ny + y2)), int(self.size))


    def ode(self,theta1, omega1, theta2, omega2):

        c = np.cos(theta1-theta2)  # intermediate variables
        s = np.sin(theta1-theta2)  # intermediate variables
        theta1_dot = omega1
        omega1_dot = (self.m2*self.g*np.sin(theta2)*c - self.m2*s*(self.l1*c*omega1**2 + self.l2*omega2**2) - (self.m1+self.m2)*self.g*np.sin(theta1) ) /( self.l1 *(self.m1+self.m2*s**2) )
        theta2_dot = omega2
        omega2_dot = ((self.m1+self.m2)*(self.l1*omega1**2*s - self.g*np.sin(theta2) + self.g*np.sin(theta1)*c) + self.m2*self.l2*omega2**2*s*c) / (self.l2 * (self.m1 + self.m2*s**2))

        return np.array([theta1_dot, omega1_dot,theta2_dot, omega2_dot])
    
    def update_position(self):
        y = np.array([self.theta1, self.omega1, self.theta2, self.omega2])
        k1 = self.ode(*y)
        k2 = self.ode(*(y + self.dt * k1 / 2))
        k3 = self.ode(*(y + self.dt * k2 / 2))
        k4 = self.ode(*(y + self.dt * k3))

        y_dot = 1.0 / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.theta1 = self.theta1 + self.dt * y_dot[0]
        self.omega1 = self.omega1 + self.dt * y_dot[1]
        self.theta2 = self.theta2 + self.dt * y_dot[2]
        self.omega2 = self.omega2 + self.dt * y_dot[3]


def plot_trajectory(initial_condition, traj_length, dt, save_path):

    theta1 = initial_condition[0]
    omega1 = initial_condition[1]
    theta2 = initial_condition[2]
    omega2 = initial_condition[3]

    window = pygame.display.set_mode((HEIGHT, WIDTH))
    window.fill(BLACK)
    pendulum = double_pendulm( theta1 = theta1, omega1 = omega1, theta2 = theta2, omega2 = omega2, l1=1, l2=1, m1=1, m2=1, g = 9.8, Nx = HEIGHT/2, Ny = WIDTH/2, l=25, size=5, color=WHITE, dt=dt)
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
    np.random.seed(2023)
    traj_length = 120
    n_traj = 1000
    n_observables = 2

    theta1 = np.random.uniform(-PI, PI,n_traj)
    theta2 = np.random.uniform(-PI, PI,n_traj)
    zeros = np.zeros(n_traj)
    initial_conditions = np.transpose(np.array([theta1, zeros, theta2, zeros]))
    locations = np.zeros(n_traj,traj_length,4)
    observables = np.zeros(n_traj,traj_length, n_observables)
    
    print(initial_conditions.shape)
    start_time = time.time()
    for i in range(1):
        initial_condition = initial_conditions[i]

        dt = 1 / 30
        # save_path = "../../dataset/double_pendulum_bw/" + str(i) + "/"
        save_path = "../../dataset/double_pendulum_bw/test/"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plot_trajectory(initial_condition, traj_length, dt, save_path)
        print(str(i) + "-th simulation done. Total time used:" + str(time.time() - start_time))
