# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2010-2011, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with OpenQuake. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.

"""
TODO: Add description
"""

import os
import re


def create_map(output_dir, compute_map_output):

    #gmtset commands
    os.system("gmtset GRID_CROSS_SIZE_PRIMARY = 0.2i") 
    os.system("gmtset BASEMAP_TYPE            = PLAIN") 
    os.system("gmtset HEADER_FONT_SIZE        = 12p")
    os.system("gmtset PAPER_MEDIA             = a4+")
    os.system("gmtset HEADER_FONT             = 22")
    os.system("gmtset LABEL_FONT_SIZE         = 14p")
    os.system("gmtset LABEL_FONT              = 22")
    os.system("gmtset ANOT_FONT_SIZE  	      = 10p")
    os.system("gmtset ANOT_FONT               = 21")
    os.system("gmtset PS_IMAGE_FORMAT         = hex")

    tmp = os.path.join(output_dir, ".tmp")
    cmd = "minmax -m -C " + compute_map_output + " > " + tmp   
    os.system(cmd)
    with open(tmp, 'rb') as tmp_file:
        line = tmp_file.readline() 
        aa = re.split("\s+",line)
    # Define the extension
    ext = "%.2f/%.2f/%.2f/%.2f" % \
	    (float(aa[0]),float(aa[1]),float(aa[2]),float(aa[3]))

    # Plotting
    plot_map_file_name = os.path.join(output_dir, 'map.eps')
    cmd = "pscoast -P -R"+ext+" -X7.0c -JM9 -Df -Na -G230 -V -K > %s" % plot_map_file_name 
    #cmd = "pscoast -R"+ext+" -X4.0c -JM15 -Df -Na -G230 -V -K > tmp.eps" 
    #cmd = "pscoast -R"+ext+" -X4.0c -JM15 -W -Df -Na -G230 -V -K -B0.25/0.25/25 -O -Slightblue> tmp.eps" 
    os.system(cmd)
	
    # Create grid 
    awkcmd = "gawk '{print $1, $2, $3}' " + compute_map_output
    os.system(awkcmd)
	
    # Create cpt 
    #cptfile = "./cpt/ad-a.cpt";
    cptfile = "./cpt/YlOrRd_09.cpt" 
    cptf = "./cpt/Blues_08.cpt"
    #cmd = "makecpt -C"+cptfile+" -T0/11/1 -Q -D255/255/255 > "+cptf
    cmd = "makecpt -C"+cptfile+" -T6/9/1 -Q -D255/255/255 > "+cptf
    os.system(cmd)

    # Plot map
    #cmd = "gawk '{print $1, $2, $3}' "+compute_map_output+" | psxy -JM -O -K -R"+ext+" -C"+cptf+" -Ss0.5  >> %s" % plot_map_file_name
    cmd = "gawk '{print $1, $2, $3/1000}' "+compute_map_output+" | psxy -JM -O -K -R"+ ext +" -C"+cptf+" -Ss1.0  >> %s" % plot_map_file_name
    os.system(cmd)

    cmd = "psscale -D4/-1/13c/0.3ch -N1 -O -K -Q -C"+cptf+" -B::/::>> %s" % plot_map_file_name
    os.system(cmd)

    cmd = "pscoast -R"+ext+" "+" -JM -W -Df -Na -V -B0.25/0.25/25 -O -Slightblue >> %s" % plot_map_file_name
    os.system(cmd)
