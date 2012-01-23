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
map_creator creates map in eps format
taking loss_map input file. The generated
output is in ./computed_output
"""

import argparse
import os
import sys

from plotmap import create_map

MSG_ERROR_NO_OUTPUT_FILE = 'Error: unspecified output file\n'
MSG_ERROR_NONEXISTENT_FILE = 'Error: nonexistent input file\n'
OUTPUT_DIR = 'computed_output'
OUTPUT_DAT = 'dat'

def build_cmd_parser():
        parser = argparse.ArgumentParser(prog='MapCreator')
        parser.add_argument('-i', '--input-file',
                            dest='input_file',
                            nargs=1,
                            metavar='input file',
                            help='Specify the input file (i.e. loss_map.xml)')
        parser.add_argument('-v', '--version',
                            action='version',
                            version="%(prog)s 0.0.1")
        return parser

def create_output_folders():
    output_dir = os.path.join(OUTPUT_DIR, OUTPUT_DAT)
    no_folder = not os.path.exists(output_dir)
    if no_folder:
        os.makedirs(output_dir)

def compute_map(loss_map_file_name):

    with open(loss_map_file_name) as file_to_read:
        lines = file_to_read.readlines()

    no = len(lines)
    latitude = []
    longitude =[]
    values = []
    no_assets = 0
    output_file_name = loss_map_file_name[0:-4] + '.txt'
    compute_map_output = os.path.join(OUTPUT_DIR, OUTPUT_DAT, output_file_name)
    with open(compute_map_output,"w") as out_file:
        for i in range(no):
            if lines[i].strip()[:7] == '<LMNode':
                j=1
                sub_value = 0.0
                while lines[i+j].strip()[:8] != '</LMNode':
                    if lines[i+j].strip()[:9] == '<gml:pos>':
                        coordinates = lines[i+j].strip()\
                                    .replace('<gml:pos>','')\
                                    .replace('</gml:pos>','').split()
                    if lines[i+j].strip()[:6] == '<mean>':
                        sub_value = sub_value + float(lines[i+j].strip()\
                                   .replace('<mean>','')\
                                   .replace('</mean>',''))
                        no_assets = no_assets+1
                    j=j+1

                latitude.append(coordinates[1])
                longitude.append(coordinates[0])
                values.append(sub_value)

        out_file.write('x,y,value\n')
        for i in range(len(values)):
            out_file.write(longitude[i]+','+latitude[i]+','
                           + str(values[i])+'\n')
    create_map(OUTPUT_DIR, compute_map_output)

def main():

    parser = build_cmd_parser()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.input_file != None:
            if os.path.exists(args.input_file[0]):
                    create_output_folders()
                    compute_map(args.input_file[0])
            else:
                print MSG_ERROR_NONEXISTENT_FILE
                parser.print_help()

if __name__== '__main__':
    main()
