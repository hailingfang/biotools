#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse

def getargs(args_in):
    parser = argparse.ArgumentParser(prog='extra_table_raws', description='extract \
        specific raws of a flat text table.')
    parser.add_argument('table_file', nargs='+', help='table file name.')
    parser.add_argument('-S', '--separater', default=None, help='separater to split line.')
    parser.add_argument('--no_head', action='store_true', help='there are head line within \
        table file the head must put at first line of file.')
    parser.add_argument('-UK', '--unite_key', type=int, nargs='+', default=[1],\
        help='column to unite multiple table. the world whin this column must be unique and \
        same between tables.')
    parser.add_argument('-SFL', '--show_first_line', action='store_true', help='print first \
        line and exit.')
    parser.add_argument('-UT', '--unite_table', action='store_true', help='unite tables and exit.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-FH', '--field_head', type=str, help='field identified by head keyword.')
    group.add_argument('-FC', '--field_column', type=int, help='field identified by column number.')
    parser.add_argument('-FV', '--filter_value', default=None, help='value to filter raw.')
    if args_in == None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args_in)
    table_file, separater, no_head, field_head, field_column, filter_value, show_first_line, \
        unite_key, unint_table = args.table_file, args.separater, args.no_head, args.field_head, \
        args.field_column, args.filter_value, args.show_first_line, args.unite_key, args.unint_table
    return table_file, separater, no_head, field_head, field_column, filter_value, \
        show_first_line, unite_key, unint_table


def unint_table(table_file, separater, no_head, unite_key):

    def unint_table_sub(all_table, unite_key):
        unint_table = []
        all_table_dic = []
        key_order = [line[unite_key[0] - 1] for line in all_table[0]]
        i = 0
        for table in all_table:
            all_table_dic.append({line[unite_key[i] - 1]:line for line in table})
            i += 1
        for key in key_order:
            line = []
            for table in all_table_dic:
                line += table[key]
            unint_table.append(line)
        return unint_table

    table_line = []
    all_table = []
    head_line = []
    if len(table_file) > 1:
        if len(table_file) != len(unite_key):
            raise Exception('There not equal key number to unite different tables.')
        for table_name in table_file:
            all_table.append([line.rstrip().split(separater) for line in open(table_name)])
        if not no_head:
            tmp = []
            for table in all_table:
                head_line += table[0]
                table_line.append(head_line)
                tmp.append(table[1:])
            all_table = tmp
        talbe_united = unint_table_sub(all_table, unite_key)
        table_line += talbe_united
    else:
        table_line = [line.rstrip().split(separater) for line in open(table_file[0])]
    return table_line


def pick_column(table_line, no_head, field_head, field_column, filter_value):
    picked_table = []
    if no_head:
        if field_head:
            raise Exception('no head appared in table according inputed arguments.')
    else:
        head_line = table_line[0]
        picked_table.append(head_line)
        table_line = table_line[1:]
    if field_head:
        column = head_line.index(field_head)
    elif field_column:
        column = field_column - 1
    for line in table_line:
        key = line[column]
        if key == filter_value:
            picked_table.append(line)
    return picked_table


def main(name='extra_table_raws', args=None):
    myname = 'extra_table_raws'
    if name == myname:
        separater_map = {r'\t':'\t', r'\s':' ', r'\n':'\n'}
        table_file, separater, no_head, field_head, field_column, filter_value, \
            show_first_line, unite_key, unint_table = getargs(args)
        separater = separater_map.get(separater, separater)
        table_line = unint_table(table_file, separater, no_head, unite_key)
        if show_first_line:
            if separater == None:
                print('\t'.join(table_line[0]))
            else:
                print(separater.join(table_line))
        else:
            if unint_table:
                picked_table=table_line
            else:
                picked_table = pick_column(table_line, no_head, field_head, field_column, \
                    filter_value)
            if separater == None:
                for line in picked_table:
                    print('\t'.join(line))
            else:
                print(separater.join(line))
    return 0


if __name__ == '__main__':
    main()
