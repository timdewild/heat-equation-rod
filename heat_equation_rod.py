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
from vendor.matnimation.src.matnimation.artist.static.static_line import StaticLine
from vendor.matnimation.src.matnimation.artist.animated.animated_quiver import AnimatedQuiver

from fourier_solutions_heat_equation import FourierHeatSolution

#--- Fourier Coefficients ---#
def fourier_coeff(boundary_cond = 'dirichlet'):
    """
    Returns fourier coefficients (a_n or b_n) depending on boundary condition ('dirichlet' or 'neumann') for the function:

    f(x) = 1/2 * (1 - cos(2 pi x))

    on the interval x in [0,1].  
    """

    def b_fourier(n: int):
        if n % 2 == 0:
            return 0
        else:
            return 2 / np.pi / n - 2 * n / (n ** 2 - 4) / np.pi

    if boundary_cond == 'dirichlet':
        return b_fourier
    
    def a_fourier(n: int):
        if n == 0:
            return 1/2
        
        if n == 2:
            return -1/2
        
        else:
            return 0
        
    if boundary_cond == 'neumann':
        return a_fourier

#--- Specification of Rod ---#
length_rod = 1
diffusivity = 1           
tau = length_rod ** 2 / diffusivity

#--- Discretization Space and Time ---#
time_array = np.linspace(0, 0.5*tau, 900)     
x_array = np.linspace(0, 1, 100)

#--- Boundary Condition: 'dirichlet' or 'neumann' ---#
boundary_cond = 'neumann'

#--- Time Evolution from FourierHeatSolution ---#
solution = FourierHeatSolution(
    x_array = x_array, 
    t_array = time_array, 
    fourier_coeff = fourier_coeff(boundary_cond = boundary_cond), 
    boundary_cond = boundary_cond)

temperature_evolution = solution.temperature_evo()
heat_flux_evolution = solution.heat_flux_evo()

# axes limits for lower two panels
xmin, xmax = 0, 1
ymin, ymax = 0, 0.1

#--- Heat Flux Data ---#
x_vectors = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
y_vectors = ymax / 2 * np.ones_like(x_vectors)

heat_flux_x_components = solution.heat_flux_evo(x = x_vectors, t = time_array)
heat_flux_y_components = np.zeros_like(heat_flux_x_components)

#--- Heat Map Data ---#
x_grid, y_grid = np.linspace(xmin, xmax, 300), np.linspace(ymin, ymax, 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

image_data = [solution.temperature_grid_evo(X_grid, Y_grid, t) for t in time_array]

#--- Lattice Vibrations Data---#
x_lat = np.linspace(xmin,xmax,50)
y_lat = np.linspace(ymin,ymax,5)

amp = 0.0025
omega0 = 800   

x_lattice, y_lattice = HelperFunctions.xy_grid(x_lat, y_lat) 
thetas = np.random.uniform(low = 0., high = 2*np.pi, size = len(x_lattice))

x_atoms = [ [x_lattice[i] + amp * np.sin(solution.omega(x=x_lattice[i], t=t, omega0=omega0) * t) * np.cos(thetas[i]) for i in range(len(x_lattice))] for t in time_array]
y_atoms = [ [y_lattice[i] + amp * np.sin(solution.omega(x=x_lattice[i], t=t, omega0=omega0) * t) * np.sin(thetas[i]) for i in range(len(x_lattice))] for t in time_array]

x_atoms = np.asarray(x_atoms).transpose()
y_atoms = np.asarray(y_atoms).transpose()

#--- Canvas ---#
canvas = MultiCanvas(
    figsize = (5,6.5),
    dpi = 400,
    time_array = time_array,
    nrows = 3,
    ncols = 1,
    axes_limits = [[0,1,0,1.2],[xmin,xmax,ymin,ymax],[xmin,xmax,ymin,ymax]],
    axes_labels = [['$x$', ''],['', ''],['', '']],
    height_ratios = [5, 1, 1]
)

if boundary_cond == 'dirichlet':
    title_panel_1 = 'Temperature Evolution: Dirichlet BCs'

if boundary_cond == 'neumann':
    title_panel_1 = 'Temperature Evolution: Neumann BCs'

canvas.set_axis_properties(
    row = 0, col = 0, 
    title = title_panel_1, 
    yticks = [-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], 
    yticklabels = ['', '$T_\\infty$', '', '', '', '', '$T_\\mathrm{max}$', '']
    )

canvas.set_axis_properties(
    row = 1, col = 0, 
    title = 'Heatmap Rod',
    aspect = 'equal', 
    xticklabels = [], 
    yticklabels = [], 
    yticks = []
    )

canvas.set_axis_properties(
    row = 2, col = 0, 
    title = 'Atomic Lattice Vibrations', 
    aspect = 'equal', 
    yticks = [], 
    yticklabels = [], 
    xticklabels = []
    )

#--- Temperature Profile Upper Panel ---#
temperature_profile = AnimatedLine(
    name = '$u(x,t)$',
    x_data = x_array,
    y_data = temperature_evolution
)

canvas.add_artist(temperature_profile, row = 0, col = 0, in_legend=True)
canvas.construct_legend(
    row = 0, 
    col = 0, 
    loc = 'upper right', 
    fontsize = 'x-small'
    )

#--- Temperature HeatMap Middle Panel ---#
heat_flux_vectors = AnimatedQuiver(
    name = "$\\vec{q}$",
    x_data = x_vectors,
    y_data = y_vectors,
    Fx_data = heat_flux_x_components,
    Fy_data = heat_flux_y_components, 
    scale = 40, 
    width = 0.005,
    color = 'white'
)

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
canvas.add_artist(heat_flux_vectors, row = 1, col = 0, in_legend=True)

canvas.construct_legend(
    row = 1, 
    col = 0, 
    fontsize = 'x-small', 
    loc = 'lower right', 
    markerscale = 0.8, 
    framealpha = 1, 
    facecolor = 'darkblue',
    labelcolor = 'white',
    borderaxespad = 0,
    bbox_to_anchor = (1, -0.6)
    ) 

colorscale = StaticColorBar(
    name = 'Colorbar',
    imshow = heat_map,
    styling_dict = dict(location = 'bottom', orientation = 'horizontal', ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]),
)

canvas.add_artist(colorscale, row = 1, col = 0)
colorscale.set_tick_labels(['$T_\\infty$', '', '', '', '', '$T_\\mathrm{max}$'], orientation = 'horizontal')

#--- Vibrating Atomic Lattice Lower Panel ---#
lattice_hlines = StaticHlines('lattice hlines', y_lat, xmin, xmax)
lattice_vlines = StaticVlines('lattice vlines', x_lat, ymin, ymax)

canvas.add_artist(lattice_hlines, row = 2, col = 0)
canvas.add_artist(lattice_vlines, row = 2, col = 0)

lattice_hlines.set_styling_properties(color = 'grey', linewidth = 0.3)
lattice_vlines.set_styling_properties(color = 'grey', linewidth = 0.3)

atoms = AnimatedScatter('atoms', x_atoms, y_atoms)
atoms.set_styling_properties(
    markersize = 5, 
    markerfacecolor = colors.to_rgba('tab:blue', 0.6), 
    markeredgecolor = 'tab:blue', 
    markeredgewidth = 0.5
    )

canvas.add_artist(
    atoms, 
    row = 2, 
    col = 0, 
    in_legend = True
    )

canvas.construct_legend(
    row = 2, 
    col = 0, 
    fontsize = 'x-small', 
    loc = 'lower right', 
    markerscale = 1, 
    framealpha = 1, 
    borderaxespad = 0,
    bbox_to_anchor = (1, -0.6)
    )



#--- Save Canvas ---#
canvas.save_canvas('canvas.jpg')

#--- Render Animation ---#
animation = Animation(canvas, interval = 10)

if boundary_cond == 'dirichlet':
    animation.render('heat_evolution_rod_dirichlet.mp4')

if boundary_cond == 'neumann':
    animation.render('heat_evolution_rod_neumann.mp4')


