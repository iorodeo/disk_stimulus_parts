"""
Creates a mount for the Linmot linear motor. There are two M6 through holes
along the center line of the part which are to connect the mount to the motor
flange via the t-slot in the flange. The mount contains a grid of 1/4-20
through holes which can be used to mount the motor.

The mount consist of two parts, designed to be laser cut form acrylic and the
solvent welded together. 

The parts are designed to be laser cut. There are three output files

plate_assembly.scad - shows an assembly of the two parts
plate_0.scad - 2D projection of the first acrylic plate
plate_1.scad - 2D projection of the second acrylic plate


To create a dxf file (from plate_0.scad or plate_1.scad): 

    1. Create the .scad files by running "python mount_maker.py" from the 
       command line. 
    2. Open .scad file using openscad.
    3. Compile and render w/ Menu Design -> Compile and Render or the F6 hot
       key.
    4. Save as dxf file w/ Menu Design -> Export as DXF. 

Note, plate_assembly.scad is only for viewing the assembly.

Author: Will Dickson

"""
from py2scad import *

INCH2MM = 25.4      

# Part parameters
x = INCH2MM*3.0
y = INCH2MM*6.0
z = INCH2MM*1.0/4.0
mount_hole_diam = 0.257*INCH2MM
M6_thru_hole_diam = 6.2
M6_washer_hole_diam =12.5 

# Create 1/4-20 mount hole list
mount_holes = []
hole_x_step = INCH2MM
hole_y_step = INCH2MM
hole_y_offset = 0.5*INCH2MM 
y_range = range(-3,3)
x_range = range(-1,2)
for i in x_range:
    for j in y_range:
        if (j in y_range[2:-1]) and (i == 0):
            continue
        x_pos = i*hole_x_step
        y_pos = j*hole_y_step + hole_y_offset
        hole = (x_pos,y_pos,mount_hole_diam)
        mount_holes.append(hole)

# Create M6 thru and washer hole lists
M6_thru_holes = []
M6_washer_holes = []
hole_y_step = 16.0
hole_y_offset = 0.5*INCH2MM
for i in [-1,1]:
    y_pos = i*hole_y_step + hole_y_offset
    thru_hole = (0.0, y_pos, M6_thru_hole_diam)
    washer_hole = (0.0, y_pos, M6_washer_hole_diam) 
    M6_thru_holes.append(thru_hole)
    M6_washer_holes.append(washer_hole)

# Create plate 0
holes_0 = mount_holes + M6_thru_holes
plate_0 = plate_w_holes(x,y,z,holes_0)

# Create plate 1
holes_1 = mount_holes + M6_washer_holes
plate_1 = plate_w_holes(x,y,z,holes_1)

# Translate plates for assembly
plate_0_assem = Translate(plate_0,v=[0,0,-0.6*z])
plate_1_assem = Translate(plate_1,v=[0,0,0.6*z])

# Create plate projections
plate_0_proj = Projection(plate_0)
plate_1_proj = Projection(plate_1)

# Create reference cube for mounting plate
ref_cube = Cube(size=[INCH2MM,INCH2MM,INCH2MM])
ref_cube = Translate(ref_cube, v=[0.5*INCH2MM+0.5*x + 2*z,0,0])
ref_cube = Projection(ref_cube)

# Write scad file for plate assembly
prog_assem = SCAD_Prog()
prog_assem.fn=100
prog_assem.add(plate_0_assem)
prog_assem.add(plate_1_assem)
prog_assem.write('plate_assem.scad')

# Write scad files for plate projections
prog_0 = SCAD_Prog()
prog_0.fn=100
prog_0.add(plate_0_proj)
prog_0.add(ref_cube)
prog_0.write('plate_0.scad')

prog_1 = SCAD_Prog()
prog_1.fn=100
prog_1.add(plate_1_proj)
prog_1.add(ref_cube)
prog_1.write('plate_1.scad')

