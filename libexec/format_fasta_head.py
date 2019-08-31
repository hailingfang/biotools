#! /usr/bin/env python3


import argparse
import fbio.fparse
import sys


def getargs():
    args = argparse.ArgumentParser()
    args.add_argument('fasta_file', help='fasta file name.')
    args.add_argument('-sep_split', default='\s', choices=['_', '-', '.', ',', '\t', '\s'], \
        help='seperator to split head string.')
    args.add_argument('-field', nargs='+', type=int, help='field want to keep.')
    args.add_argument('-sep_link', default='\s', choices=['_', '-', '.', ',', '\t', '\s'], \
        help = 'seperator to link fildes.')
    args.add_argument('-f_out', default=sys.stdout, help='out file name.')
    args = args.parse_args()
    fasta_file, sep_split, field, sep_link, f_out = args.fasta_file, args.sep_split, args.field, \
        args.sep_link, args.f_out
    field = [i-1 for i in field]
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
            new_head.append(head_ele[i])
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


def main(fasta_file, sep_split, field, sep_link, f_out):
    # DEBUG: print(fasta_file, sep_split, field, sep_link)
    fasta_dt = struc_fasta(fasta_file)
    fasta_dt = format_head(fasta_dt, sep_split, field, sep_link)
    print_res(fasta_dt,f_out)
    return 0


if __name__ == '__main__':
    fasta_file, sep_split, field, sep_link,f_out = getargs()
    main(fasta_file, sep_split, field, sep_link, f_out)
