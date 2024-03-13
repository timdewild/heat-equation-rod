import sys
import os

abs_path = 'vendor/matnimation'
sys.path.append(os.path.abspath(abs_path)) 

from vendor.matnimation.src.matnimation.canvas.multi_canvas import MultiCanvas

canvas = MultiCanvas(
    figsize = (4,7),
    dpi = 400,
    time_array = None,
    nrows = 3,
    ncols = 1,
    axes_limits = [[0,1,0,1],[0,1,0,1],[0,1,0,1]],
    axes_labels = [['$x$', '$y$'],['$x$', '$y$'],['$x$', '$y$']] 
)

canvas.set_axis_properties(height_ratios = [2,1,1])

canvas.save_canvas('test.jpg')