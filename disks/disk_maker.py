"""
Ceates a disk with a hole in the center. The SCAD output file, designed for
sending the parts to laser cutting, consists of a 2D projection of the disk
along with 1" reference cube. 

To create a dxf file: 

    1. Create the disk.scad file by running "python disk_maker.py" from the 
       command line. 
    2. Open disk.scad using openscad.
    3. Compile and render w/ Menu Design -> Compile and Render or the F6 hot
       key.
    4. Save as dxf file w/ Menu Design -> Export as DXF. 

Author: Will Dickson

"""
from py2scad import *

INCH2MM = 25.4

# Disk Parameters
diameter = 100.0 
thickness = INCH2MM*1.0/16.0
M5_close_fit = 5.00 # Adjusted for laser cutting
hole = (0.0,0.0,M5_close_fit)

disk = disk_w_holes(thickness, diameter, [hole])
disk = Projection(disk)

# 1 inch reference cube
ref_cube = Cube(size=[INCH2MM,INCH2MM,INCH2MM])
ref_cube = Translate(ref_cube,v=[0.5*INCH2MM+0.5*diameter+10,0,0])
ref_cube = Projection(ref_cube)

prog = SCAD_Prog()
prog.fn = 150
prog.add(disk)
prog.add(ref_cube)
prog.write('disk.scad')
