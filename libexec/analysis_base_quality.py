#! /usr/bin/env python3
import numpy as np
import sys

def struc_dt(file):
    dt_out = []
    i = 0
    for line in open(file):
        i += 1
        if i == 4:
            dt_out.append(line[:10])
            i = 0
    return dt_out


def get_position_qulity(dt_in, pos):
    dt_out = []
    for line in dt_in:
        dt_out.append(line[pos])
    return dt_out


def trans_char_to_qulity(dt_in):
    dt_out = []
    for b in dt_in:
        dt_out.append(ord(b) - 33)
    return dt_out


def main():
    res = []
    dt = struc_dt(sys.argv[1])
    for pos in range(10):
        poss = get_position_qulity(dt, pos)
        poss_qulity = trans_char_to_qulity(poss)
        res.append([pos + 1, np.mean(poss_qulity), np.median(poss_qulity), np.percentile(poss_qulity, 25), np.percentile(poss_qulity, 75)])
    for record in res:
        print(record)
    return 0


if __name__  == '__main__':
    main()
