""" 
Creates an adapter for mounting the micro epsilon ILD1402-250.VT 
laser onto the linear motor.   

To create a dxf file (from plate_0.scad or plate_1.scad): 

    1. Create the .scad files by running "python mount_maker.py" from the 
       command line. 
    2. Open .scad file using openscad.
    3. Compile and render w/ Menu Design -> Compile and Render or the F6 hot
       key.
    4. Save as dxf file w/ Menu Design -> Export as DXF. 

Note, plate_assembly.scad is only for viewing the assembly.

Authors: 
Joanne Long,   IO Rodeo Inc. - original version
Will Dickson,  IO Rodeo Inc. - modified so that both assembly and 
                               projection files are written.
"""

import sys
import scipy
from py2scad import *

# Units below are in mm
INCH2MM = 25.4
INCH2CM = 2.54

# Part parameters
clamp_x = 50
clamp_y = 30
clamp_z = 55
rail_height = 6.25*INCH2MM
rail_radius = 11.5
screw_height = 0.25*INCH2MM
screw_radius = 2.1
laser_height = 65
laser_width = 50
laser_thickness = 20
mount_height = 0.25*INCH2MM
mount_radius = 1.65
mount_x_pos = 20.0
mount_z_pos = 28.7
mountholes_num = 4
mountholes_step = 10
adapter_thickness = 0.25*INCH2MM

#Parts list and colors
clamp = Cube(size = [clamp_x, clamp_y, clamp_z])
clamp = Color(clamp, rgba=[0,0,0,1])
screwhole = Cylinder(h = 1.2*screw_height , r1 = screw_radius, r2 = screw_radius)
rail = Cylinder(h = rail_height , r1 = rail_radius, r2 = rail_radius)
adapter = Cube(size =[0.6*rail_height, adapter_thickness, laser_height]) 
laser = Cube(size = [laser_width, laser_thickness, laser_height])
laser = Color(laser, rgba=[1,0,0,1])
mounthole = Cylinder(h = 1.5*mount_height , r1 = mount_radius, r2 = mount_radius)
mounthole = Color(mounthole, rgba=[1,0,0,1])

# Rotate and translate screw holes 
screwhole = Rotate(screwhole, a =90, v=[1,0,0])
screwhole = Color(screwhole, rgba=[0,0,0,1])
v1 = [0,-(0.5*clamp_y+0.5*screw_height), 0.5*clamp_z-7.5]
screwhole1 = Translate(screwhole,v=v1)
v2=[0,-(0.5*clamp_y+0.5*screw_height), -(0.5*clamp_z-7.5)]
screwhole2 = Translate(screwhole,v=v2 )

# Rotate and translate rail
rail = Rotate(rail, a =90, v=[0,1,0])
v = [0.5*rail_height - 0.5*clamp_x - 28.8,0,0.5*clamp_z-rail_radius-18.5]
rail= Translate(rail, v=v)

# Translate mount adapter
v = [0, -(0.5*clamp_y+0.5*adapter_thickness),0.5*(laser_height - clamp_z)]
adapter = Translate(adapter,v=v )

# Translate laser
v_x = 0
v_y = -(0.5*clamp_y+0.5*adapter_thickness + laser_thickness) 
v_z = 0.5*(laser_height - clamp_z)
laser = Translate(laser, v=[v_x, v_y,v_z])

# Mounting hole array
mounthole = Rotate(mounthole, a =90, v=[1,0,0])
v_x = mount_x_pos
v_y = -(0.5*clamp_y + adapter_thickness + 0.5*mount_height)
v_z =  mount_z_pos +  0.5*(laser_height - clamp_z)
mounthole1 = Translate(mounthole, v=[v_x, v_y, v_z])
v_x  = -mount_x_pos 
v_z = -mount_z_pos + 0.5*(laser_height - clamp_z)
mounthole2 = Translate(mounthole, v=[v_x, v_y, v_z])
mountholes = Union([mounthole1, mounthole2])
mountholes = Translate(mountholes, v=[0, adapter_thickness, 0])

mountholes_list = []
for i in range(0, mountholes_num):
    x_step = i*mountholes_step -0.5*mountholes_num*mountholes_step
    mountholes_new = Translate(mountholes, v=[x_step, 0, 0])
    mountholes_list.append(mountholes_new)

# Differencing
adapter = Difference([adapter, screwhole1, screwhole2] + mountholes_list)

# Rotations and Projections
v = [0, 0.5*clamp_y+0.5*adapter_thickness, -0.5*(laser_height - clamp_z)]
adapter_proj = Translate(adapter, v=v)
adapter_proj = Rotate(adapter_proj, a= 90, v= [1,0,0])
adapter_proj = Projection(adapter_proj)

# Reference cube for laser cutting
reference = Cube(size = [INCH2MM, INCH2MM, INCH2MM])
reference = Translate(reference, v= [50, 50, 0])
reference = Projection(reference)


# Write assembly file 
prog = SCAD_Prog()
prog.fn=50
prog.add(clamp)
prog.add(rail)
prog.add(adapter)
prog.add(laser)
prog.write('laser_mount_assembly.scad')     

# Write 2D projection and reference for laser cutting
prog = SCAD_Prog()
prog.fn=50
prog.add(adapter_proj)
prog.add(reference)
prog.write('laser_mount_projection.scad')     

