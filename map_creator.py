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
from collections import namedtuple
from lxml import etree
import os
import sys

from plotmap import create_map

MSG_ERROR_NO_OUTPUT_FILE = 'Error: unspecified output file\n'
MSG_ERROR_NONEXISTENT_FILE = 'Error: nonexistent input file\n'
OUTPUT_DIR = 'computed_output'
OUTPUT_DAT = 'dat'

nrml_ns = '{http://openquake.org/xmlns/nrml/0.2}'

lm_node = '%sLMNode' % nrml_ns

pos_node = '{http://www.opengis.net/gml}pos'

loss_node_elem = '%sloss' % nrml_ns

mean_node = '%smean' % nrml_ns

Entry = namedtuple('Entry', 'lon, lat, sum_mean')


def build_cmd_parser():
    parser = argparse.ArgumentParser(prog='MapCreator')

    parser.add_argument('-i', '--input-file',
                        nargs=1,
                        metavar='input file',
                        dest='input_file',
                        help='Specify the input file (i.e. loss_map.xml)')

    parser.add_argument('-r', '--res',
                        nargs=1,
                        default=0.5,
                        type=float,
                        help='resolution of each dot',
                        metavar='value',
                        dest='resolution')

    parser.add_argument('-min', "--min-val",
                        nargs=1,
                        default=100.0,
                        type=float,
                        help='minimum value in a loss map',
                        metavar='value',
                        dest='min-val')

    parser.add_argument('-max', '--max-val',
                        nargs=1,
                        default=1000000000.0,
                        type=float,
                        help='maximum value in a loss map',
                        metavar='value',
                        dest='max-val')

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

    output_file_name = loss_map_file_name[0:-4] + '.txt'
    compute_map_output = os.path.join(OUTPUT_DIR, OUTPUT_DAT, output_file_name)
    write_loss_map_entries(compute_map_output,
            read_loss_map_entries(loss_map_file_name))
    create_map(OUTPUT_DIR, compute_map_output)


def read_loss_map_entries(loss_map_xml):

    entries = []

    elem = 1

    with open('loss-map.xml') as loss_file:
        for node in etree.iterparse(loss_file):
            if node[elem].tag == lm_node:
                lon, lat = node[elem].find('.//%s' % pos_node).text.split()

                loss_nodes = node[elem].findall('.//%s' % loss_node_elem)

                sum_mean = 0
                for loss_node in loss_nodes:
                    sum_mean += float(loss_node.find('.//%s' % mean_node).text)

                entries.append(Entry(lon, lat, sum_mean))

    return entries


def write_loss_map_entries(output_filename, loss_entries):

    with open(output_filename, 'w') as out_file:
        out_file.write('x,y,value\n')
        for entry in loss_entries:
            entry_string = ','.join(
                [entry.lon, entry.lat, str(entry.sum_mean)]) + '\n'
            out_file.write(entry_string)


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

if __name__ == '__main__':
    main()
