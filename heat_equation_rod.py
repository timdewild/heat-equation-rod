import sys
import os

abs_path = 'vendor/matnimation'
sys.path.append(os.path.abspath(abs_path)) 

import numpy as np

from vendor.matnimation.src.matnimation.animation.animation import Animation
from vendor.matnimation.src.matnimation.canvas.multi_canvas import MultiCanvas
from vendor.matnimation.src.matnimation.artist.static.static_line import StaticLine
from vendor.matnimation.src.matnimation.artist.animated.animated_line import AnimatedLine
from vendor.matnimation.src.matnimation.artist.animated.animated_imshow import AnimatedImshow

length_rod = 1
alpha = 1           # diffusivity constant D = alpha^2
tau = length_rod ** 2 / alpha ** 2

time_array = np.linspace(0, 0.25*tau, 200)

def lambda_n(n: int):
    return alpha * np.pi * n / length_rod

def mu_n(n: int):
    return n * np.pi / length_rod

def b_fourier(n: int):
    if n % 2 == 0:
        return 0
    else:
        return 2 / np.pi / n - 2 * n / (n ** 2 - 4) / np.pi
    
def temperature_normal_mode_dirichlet(x, t, n: int):
    u_n = b_fourier(n) * np.exp(- lambda_n(n)**2 * t) * np.sin(mu_n(n) * x)

    return u_n
    
def temperature_dirichlet(x, t, number_of_terms = 100):
    u = np.zeros_like(x)
    for n in range(1,number_of_terms):
        u += temperature_normal_mode_dirichlet(x, t, n)

    return u

def temperature_neumann(x,t):
    u = 0.5 - 0.5 * np.cos(2*np.pi*x)*np.exp(-4 * np.pi**2 * t)

    return u

def temperature_grid(temp_func : callable, X, Y, t):
    return temp_func(X, t)


x = np.linspace(0,1,100)

temp_profile_dirichlet = [temperature_dirichlet(x, t) for t in time_array]
temp_profile_dirichlet = np.stack(temp_profile_dirichlet, axis = 1)

X, Y = np.meshgrid(np.linspace(0,1,300), np.linspace(0,1,100))

image_data = [temperature_grid(temperature_neumann, X, Y, t) for t in time_array]


temp_profile_neumann = [temperature_neumann(x, t) for t in time_array]
temp_profile_neumann = np.stack(temp_profile_neumann, axis = 1)

canvas = MultiCanvas(
    figsize = (5,6),
    dpi = 400,
    time_array = time_array,
    nrows = 3,
    ncols = 1,
    axes_limits = [[0,1,0,1.2],[0,1,0,1],[0,1,0,1]],
    axes_labels = [['', '$T$'],['', ''],['$x$', '$y$']],
    height_ratios = [6,0.33,2],
    shared_x = True
)

canvas.set_axis_properties(row = 1, col = 0, xticklabels = [], yticklabels = [])

temperature_profile = AnimatedLine(
    name = 'Temperature',
    x_data = x,
    y_data = temp_profile_neumann
)

heat_map = AnimatedImshow(
    name = 'Heatmap',
    image_data = image_data,
    extent = [0,1,0,1],
    aspect = 'auto',
    cmap = 'plasma'
)

canvas.add_artist(temperature_profile, row = 0, col = 0)
canvas.add_artist(heat_map, row = 1, col = 0)

animation = Animation(canvas, interval = 10)
animation.render('heat_evolution_rod.mp4')