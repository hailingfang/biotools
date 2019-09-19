#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse

def getargs(args_in):
    parser = argparse.ArgumentParser(prog='format_table_separater', description='\
        change separater of flat text table.')
    parser.add_argument('table_file', help='table file name.')
    parser.add_argument('-A', '--old_separater', default=' ', help='old separater. \
        default is space.')
    parser.add_argument('-B', '--new_separater', default=',', help='new separater. \
        default is ",".')
    if args_in:
        args = parser.parse_args(args_in)
    else:
        args = parser.parse_args()
    table_file, old_separater, new_separater = args.table_file, args.old_separater, \
        args.new_separater
    return table_file, old_separater, new_separater


def main(name='format_table_separater', args=[]):
    myname = 'format_table_separater'
    if name == myname:
        table_file, old_separater, new_separater = getargs(args)
        separater_map = {r'\t':'\t', r'\s':' ', r'\n':'\n'}
        if old_separater in separater_map:
            old_separater = separater_map[old_separater]
        if new_separater in separater_map:
            new_separater = separater_map[new_separater]
        all_line = [line.rstrip().split(old_separater) for line in open(table_file)]
        for line in all_line:
            print(new_separater.join(line))
    return 0


if __name__ == '__main__':
    main()
