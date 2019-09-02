#! /usr/bin/env python3

import argparse
import fbio.fparse
import re
import sys


def deal_field(field):
    re_a = re.compile(r'^\d+$')
    re_b = re.compile(r'^\d+:\d+$')
    dt_out = []
    for ele in field:
        if re_a.match(ele):
            dt_out.append(int(ele))
        elif re_b.match(ele):
            ele1, ele2 = ele.split(':')
            ele1, ele2 = int(ele1), int(ele2)
            if ele1 <= ele2:
                ele_range = list(range(ele1, ele2+1))
            else:
                ele_range = list(range(ele2, ele1+1))
                ele_range = ele_range[::-1]
            dt_out += ele_range
        else:
            raise Exception('field wrong.')
    return dt_out


def getargs(args_in):
    args = argparse.ArgumentParser(prog='format_fasta_head', description='Format fasta file head line.', add_help=False)
    args.add_argument('-fasta_file', required=True, help='fasta file name.')
    args.add_argument('-sep_split', default='\s', choices=['_', '-', '.', ',', 't', 's'], \
        help='seperator to split head string.')
    args.add_argument('-sep_link', default='\s', choices=['_', '-', '.', ',', 't', 's'], \
        help = 'seperator to link fildes.')
    args.add_argument('-field', nargs='+', required=True, help='field want to keep.')
    args.add_argument('-f_out', default=sys.stdout, help='out file name.')
    if args_in == None:
        args = args.parse_args()
    else:
        args = args.parse_args(args_in)
    fasta_file, sep_split, field, sep_link, f_out = args.fasta_file, args.sep_split, args.field, \
        args.sep_link, args.f_out
    if sep_split == 's':
        sep_split = ' '
    elif sep_split == 't':
        sep_split = '\t'
    if sep_link == 's':
        sep_link = ' '
    elif sep_link == 't':
        sep_link = '\t'
    field = deal_field(field)
    return fasta_file, sep_split, field, sep_link, f_out


def struc_fasta(fasta_file):
    fasta_dt = fbio.fparse.Fasta_parse(fasta_file)
    fasta_dt = fasta_dt.data
    return fasta_dt


def format_head(fasta_dt, sep_split, field, sep_link):
    dt_out = {}
    for head in fasta_dt:
        new_head = []
        head_ele = head.split(sep_split)
        for i in field:
            new_head.append(head_ele[i - 1])
        new_head = sep_link.join(new_head)
        dt_out[new_head] = fasta_dt[head]
    return dt_out


def print_res(fasta_dt, f_out):
    if f_out != sys.stdout:
        f_out = open(f_out, 'w')
    for head in fasta_dt:
        print('>' + head, file=f_out)
        for line in fasta_dt[head]:
            print(line, file=f_out)
    f_out.close()
    return 0


def main(name='format_fasta_head', args=None):
    myname = 'format_fasta_head'
    if name == myname:
        fasta_file, sep_split, field, sep_link, f_out = getargs(args)
        fasta_dt = struc_fasta(fasta_file)
        fasta_dt = format_head(fasta_dt, sep_split, field, sep_link)
        print_res(fasta_dt,f_out)
    return 0


if __name__ == '__main__':
    main()
