#! /usr/bin/env python3

import argparse
import sys
from biobrary import bioparse

def get_args():
    args = argparse.ArgumentParser(description='filter assembly result of spades \
        according length and coverage.')
    args.add_argument('fasta_file', type=str, help='fasta file name.')
    args.add_argument('-length_cutoff', type=int, default=200, help='length cutoff, \
        default is 200 bp.')
    args.add_argument('-coverage_cutoff', type=float, default=10, help='coverage cutoff, \
        default is 10.')
    args.add_argument('-file_out', type=open, default=sys.stdout, help='file out file name, \
        default is stdout.')
    args = args.parse_args()
    fasta_file, len_cutoff, coverage_cutoff, file_out = args.fasta_file, args.length_cutoff, \
        args.coverage_cutoff, args.file_out

    return fasta_file, len_cutoff, coverage_cutoff, file_out


def judge_cutoff(head_line, len_cutoff, coverage_cutoff):
    head = head_line.split('_')
    length = int(head[3])
    coverage = float(head[5])
    if length >= len_cutoff and coverage >= coverage_cutoff:
        return True
    else:
        return False


def main():
    fasta_file, len_cutoff, coverage_cutoff, file_out = get_args()
    fasta_dt = bioparse.Fasta_parse(fasta_file)
    for head in fasta_dt.data:
        okornot = judge_cutoff(head, len_cutoff, coverage_cutoff)
        if okornot:
            print('>' + head, file=file_out)
            for line in fasta_dt.data[head]:
                print(line, file=file_out)
    file_out.close()
    return 0


if __name__  == '__main__':
    main()
