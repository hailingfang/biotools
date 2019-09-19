#! /usr/bin/env python3
# -*-coding: utf-8-*-

import argparse
import sys


import libexec.format_fasta_head
import libexec.format_table_separater
import libexec.extra_table_raws
import libexec.statistic_phytree
import libexec.statistic_assembly
import libexec.find_updown_elements
import libexec.phytree_statistic
import libexec.phytree_groups
import libexec.phytree_collapse
import libexec.phytree_show


def getargs():
    Description = \
    '''
Tools for bioinformatics.
The flowing tools/subcommand was supported:

    * format_fasta_head
    * format_table_separater
    * extra_table_raws
    * statistic_assembly
    * statistic_phytree
    * find_updown_elements
    * phytree_statistic
    * phytree_groups
    * phytree_collapse
    * phytree_show
    '''
    parser = argparse.ArgumentParser(prog='biotools')
    parser.add_argument('cmd_name', help='subcommand name.')
    parser.add_argument('cmd_args', nargs='*', help="subcommand arguments.")
    if len(sys.argv) == 1:
        args = parser.parse_args()
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print(Description)
        parser.parse_args()
    else:
        args = parser.parse_args([sys.argv[1]])
    cmd_name, cmd_args = args.cmd_name, sys.argv[2:]
    cmd_name_list = [
    'format_fasta_head',
    'format_table_separater',
    'extra_table_raws',
    'statistic_assembly',
    'statistic_phytree',
    'find_updown_elements',
    'phytree_statistic',
    'phytree_groups',
    'phytree_collapse',
    'phytree_show'
    ]
    if cmd_name not in cmd_name_list:
        print('***error, tool not found***')
        print(Description)
        parser.parse_args(['-h'])
    return cmd_name, cmd_args


def main():
    cmd_name, cmd_args = getargs()
    libexec.format_fasta_head.main(cmd_name, cmd_args)
    libexec.format_table_separater.main(cmd_name, cmd_args)
    libexec.extra_table_raws.main(cmd_name, cmd_args)
    libexec.statistic_assembly.main(cmd_name, cmd_args)
    libexec.statistic_phytree.main(cmd_name, cmd_args)
    libexec.find_updown_elements.main(cmd_name, cmd_args)
    libexec.phytree_groups.main(cmd_name, cmd_args)
    libexec.phytree_collapse.main(cmd_name, cmd_args)
    libexec.phytree_statistic.main(cmd_name, cmd_args)
    libexec.phytree_show.main(cmd_name, cmd_args)
    return 0


if __name__ == '__main__':
    main()
