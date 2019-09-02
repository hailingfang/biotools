#! /usr/bin/env python3

import argparse
import fbio.fparse
import os
import sys


def get_args(args_in):
    args = argparse.ArgumentParser(prog='statistic_assembly', description='stat\
        istic assembly information.')
    args.add_argument('assembly_file', nargs='+', type=str, help='assembly file name.')
    args.add_argument('-f_out', default=sys.stdout, help='file name of output.')
    if args_in == None:
        args = args.parse_args()
    else:
        args = args.parse_args(args_in)
    assembly_file, f_out = args.assembly_file, args.f_out
    return assembly_file, f_out


def stat_assembly(data):
    data_sta = {}
    len_list = []
    for head in data:
        seq = ''.join(data[head])
        length = len(seq)
        GC_num = len([base for base in seq if base=='G' or base=='C'])
        data_sta[head] = [length,GC_num]
        len_list.append(length)
    totall_len = 0
    totall_GC = 0
    for head in data_sta:
        totall_len += data_sta[head][0]
        totall_GC += data_sta[head][1]
    len_list.sort(reverse=True)
    max_len = 0
    min_len = 0
    if len(len_list):
        max_len = len_list[0]
        min_len = len_list[-1]
    num_contig = len(len_list)
    ava_len = totall_len/num_contig if num_contig >0 else 0
    GC_content = totall_GC/totall_len if totall_len >0 else 0
    start = 0
    half_len = totall_len/2
    L50 = 0
    N50 = 0
    for num in len_list:
        start += num
        L50 += 1
        if start >= half_len:
            N50 = num
            break

    return [totall_len,num_contig,max_len,min_len,ava_len,GC_content,N50,L50]


def print_res(infors, f_out):
    if f_out != sys.stdout:
        f_out = open(f_out, 'w')
    print('assembly_file,totall_len,num_contig,max_len,min_len,ava_len,GC_conte\
        nt,N50,L50', file=f_out)
    for record in infors:
        record = [str(s) for s in record]
        record = ','.join(record)
        print(record, file=f_out)
    f_out.close()
    return 0


def main(name='statistic_assembly', args=None):
    myname = 'statistic_assembly'
    infors = []
    if name == myname:
        assembly_file, f_out = get_args(args)
        for ff in assembly_file:
            f_dt = fbio.fparse.Fasta_parse(ff)
            f_dt = f_dt.data
            infors.append([os.path.basename(ff)] + stat_assembly(f_dt))
        print_res(infors, f_out)
    return 0


if __name__ == '__main__':
    main()
