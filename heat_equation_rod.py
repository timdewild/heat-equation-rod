import sys
import os

abs_path = 'vendor/matnimation'
sys.path.append(os.path.abspath(abs_path)) 

from matplotlib import colors
import numpy as np

from vendor.matnimation.src.matnimation.animation.animation import Animation
from vendor.matnimation.src.matnimation.canvas.multi_canvas import MultiCanvas
from vendor.matnimation.src.matnimation.artist.animated.animated_line import AnimatedLine
from vendor.matnimation.src.matnimation.artist.animated.animated_imshow import AnimatedImshow
from vendor.matnimation.src.matnimation.artist.static.static_hlines import StaticHlines
from vendor.matnimation.src.matnimation.artist.static.static_vlines import StaticVlines
from vendor.matnimation.src.matnimation.helper.helper_functions import HelperFunctions
from vendor.matnimation.src.matnimation.artist.animated.animated_scatter import AnimatedScatter
from vendor.matnimation.src.matnimation.artist.static.static_colorbar import StaticColorBar

length_rod = 1
alpha = 1           # diffusivity constant D = alpha^2
tau = length_rod ** 2 / alpha ** 2

time_array = np.linspace(0, 0.5*tau, 900)      #0, 0.15*tau, 300, Nt = 900
x_array = np.linspace(0,1,100)

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
    
def temperature_dirichlet(x, t):
    u = np.zeros_like(x)
    for n in range(1,30):
        u += temperature_normal_mode_dirichlet(x, t, n)

    return u

def temperature_neumann(x,t):
    u = 0.5 - 0.5 * np.cos(2*np.pi*x)*np.exp(-4 * np.pi**2 * t)
    return u

def temperature_grid(temp_func : callable, X, Y, t):
    return temp_func(X, t)

def omega(temp_func : callable, x, t, omega0 = 1):
    return omega0 / 2 + omega0 * (temp_func(x,t)) ** 0.5

#--- Tempereture Evolution ---#
temp_profile_dirichlet = [temperature_dirichlet(x_array, t) for t in time_array]
temp_profile_dirichlet = np.stack(temp_profile_dirichlet, axis = 1)

temp_profile_neumann = [temperature_neumann(x_array, t) for t in time_array]
temp_profile_neumann = np.stack(temp_profile_neumann, axis = 1)

print('Temp evo done')

xmin, xmax = 0, 1
ymin, ymax = 0, 0.1

#--- Heat Map Data ---#
x_grid, y_grid = np.linspace(xmin, xmax, 300), np.linspace(ymin, ymax, 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

image_data = [temperature_grid(temperature_dirichlet, X_grid, Y_grid, t) for t in time_array]

print('Image data done')

#--- Lattice ---#
x_lat = np.linspace(xmin,xmax,50)
y_lat = np.linspace(ymin,ymax,5)

amp = 0.0025
omega0 = 800

x_lattice, y_lattice = HelperFunctions.xy_grid(x_lat, y_lat) 
thetas = np.random.uniform(low = 0., high = 2*np.pi, size = len(x_lattice))

x_atoms = [ [x_lattice[i] + amp * np.sin(omega(temp_func=temperature_dirichlet, x=x_lattice[i], t=t, omega0=omega0) * t) * np.cos(thetas[i]) for i in range(len(x_lattice))] for t in time_array]
y_atoms = [ [y_lattice[i] + amp * np.sin(omega(temp_func=temperature_dirichlet, x=x_lattice[i], t=t, omega0=omega0) * t) * np.sin(thetas[i]) for i in range(len(x_lattice))] for t in time_array]

x_atoms = np.asarray(x_atoms).transpose()
y_atoms = np.asarray(y_atoms).transpose()

print('Lattice evo done')

#--- Canvas ---#
canvas = MultiCanvas(
    figsize = (5,6),
    dpi = 400,
    time_array = time_array,
    nrows = 3,
    ncols = 1,
    axes_limits = [[0,1,0,1.2],[xmin,xmax,ymin,ymax],[xmin,xmax,ymin,ymax]],
    axes_labels = [['$x$', 'Temperature $T(x,t)$'],['', ''],['', '']],
    height_ratios = [5, 1, 1]
)

canvas.set_axis_properties(row = 0, col = 0, yticks = [-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], yticklabels = ['', '$T_\\infty$', '', '', '', '', '$T_\\mathrm{max}$', ''])
canvas.set_axis_properties(row = 1, col = 0, aspect = 'equal', xticklabels = [], yticklabels = [], xticks = [], yticks = [])
canvas.set_axis_properties(row = 2, col = 0, aspect = 'equal', yticks = [], yticklabels = [], xticks = [], xticklabels = [])

temperature_profile = AnimatedLine(
    name = 'Temperature',
    x_data = x_array,
    y_data = temp_profile_dirichlet
)

canvas.add_artist(temperature_profile, row = 0, col = 0)

heat_map = AnimatedImshow(
    name = 'Heatmap',
    image_data = image_data,
    extent = [xmin,xmax,ymin,ymax],
    cmap = 'plasma',
    aspect = 'equal',
    vmin = 0,
    vmax = 1
)

canvas.add_artist(heat_map, row = 1, col = 0)

colorscale = StaticColorBar(
    name = 'Colorbar',
    imshow = heat_map,
    styling_dict = dict(location = 'top', orientation = 'horizontal', ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]),
)


canvas.add_artist(colorscale, row = 1, col = 0)
colorscale.set_tick_labels(['$T_\\infty$', '', '', '', '', '$T_\\mathrm{max}$'], orientation = 'horizontal')


lattice_hlines = StaticHlines('lattice hlines', y_lat, xmin, xmax)
lattice_vlines = StaticVlines('lattice vlines', x_lat, ymin, ymax)

canvas.add_artist(lattice_hlines, row = 2, col = 0)
canvas.add_artist(lattice_vlines, row = 2, col = 0)

lattice_hlines.set_styling_properties(color = 'grey', linewidth = 0.3)
lattice_vlines.set_styling_properties(color = 'grey', linewidth = 0.3)

atoms = AnimatedScatter('atoms', x_atoms, y_atoms)
atoms.set_styling_properties(markersize = 5, markerfacecolor = colors.to_rgba('tab:blue', 0.6), markeredgecolor = 'tab:blue', markeredgewidth=0.5)

canvas.add_artist(atoms, row = 2, col = 0)

canvas.save_canvas('canvas.jpg')

animation = Animation(canvas, interval = 10)
animation.render('heat_evolution_rod.mp4')

