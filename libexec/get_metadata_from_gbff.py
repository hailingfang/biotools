#! /usr/bin/env python3
'''
input a gbff file name, and output BioProject ID, BioSample ID and Assembly Number information.
'''
import argparse
import re
import sys

def get_args():
    args = argparse.ArgumentParser(description='get biosample id, bioproject id, \
        information for gbff file.')
    args.add_argument('gbff_file', type=str, help='gbff file name.')
    args.add_argument('-f_out', default=sys.stdout, help='output file name. system \
        stand out as default stream.')
    args = args.parse_args()
    gbff_file, f_out = args.gbff_file, args.f_out
    return gbff_file, f_out


def get_metadata_gbff(gbff_file):
    data_out = {}
    block = []
    block_s_re = re.compile(r'DBLINK\s{6}')
    block_e_re = re.compile(r'KEYWORDS\s{4}')
    biop_re = re.compile(r'\s+?BioProject:\s(.+)$')
    bios_re = re.compile(r'\s+?BioSample:\s(.+)$')
    assmbly_re = re.compile(r'\s+?Assembly:\s(.+)$')
    i = 0
    for line in open(gbff_file):
        if block_s_re.match(line):
            i = 1
        if block_e_re.match(line):
            break
        if i == 1:
            block.append(line)
    for line in block:
        if biop_re.search(line):
            data_out['BioProject'] = biop_re.search(line).groups()[0]
        elif bios_re.search(line):
            data_out['BioSample'] = bios_re.search(line).groups()[0]
        elif assmbly_re.search(line):
            data_out['Assembly'] = assmbly_re.search(line).groups()[0]

    return data_out


def print_res(res_dt, f_out=sys.stdout):
    key_ord = ['BioProject', 'BioSample', 'Assembly']
    res_line = []
    for key in key_ord:
        res_line.append(res_dt.get(key, None))
    print(','.join(res_line), file=f_out)


def main():
    gbff_file, f_out = get_args()
    res = get_metadata_gbff(gbff_file)
    if f_out != sys.stdout:
        f_out = open(f_out, 'w')
    print_res(res, f_out)
    if f_out != sys.stdout:
        f_out.close()
    return 0


if __name__ == '__main__':
    main()
