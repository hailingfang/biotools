#! /usr/bin/env python3

import argparse
import ete3
import sys


def get_args(args_in):
    args = argparse.ArgumentParser(prog='statistic_phytree', description='statistic phylogenetice tree.')
    args.add_argument('tree_file', type=str, help='tree file name.')
    args.add_argument('-f_out', default=sys.stdout, help='out file name.')
    if args_in == None:
        args = args.parse_args()
    else:
        args = args.parse_args(args_in)
    tree_file, f_out = args.tree_file, args.f_out
    return tree_file, f_out


def get_longest_dist(tree):
    el_max=tree.get_farthest_leaf()
    nl_max=tree.get_farthest_leaf(topology_only=True)
    return el_max,nl_max


def get_average_leaf_dist(tree):
    len_all = []
    for leaf in tree:
        len_all.append([leaf.name,leaf.dist])
    sort_f = lambda x:x[1]
    len_all.sort(key = sort_f)
    shortest_leaf = []
    min_len = len_all[0][1]
    for ele in len_all:
        if ele[1] == min_len:
            shortest_leaf.append(ele)
    longest_leaf = []
    max_len = len_all[-1][1]
    for ele in len_all:
        if ele[1] == max_len:
            longest_leaf.append(ele)
    leaf_ave_len = sum([x[1] for x in len_all])/len(len_all)
    return shortest_leaf,longest_leaf,leaf_ave_len


def print_res(dt, f_out):
    if f_out != sys.stdout:
        f_out = open(f_out, 'w')
    print('max_edge_len:', dt[0], file=f_out)
    print('max_topology_len:', dt[1], file=f_out)
    print('shortest_leaf:', dt[2], file=f_out)
    print('longest_leaf:', dt[3], file=f_out)
    print('leaf_ave_len:', dt[4], file=f_out)
    f_out.close()
    return 0


def main(name='phytree_statistic', args=None):
    myname = 'statistic_phytree'
    if myname == name:
        tree_file, f_out = get_args(args)
        tree = ete3.Tree(tree_file)
        max_edge_len, max_topology_len = get_longest_dist(tree)
        shortest_leaf, longest_leaf, leaf_ave_len = get_average_leaf_dist(tree)
        dt = [max_edge_len, max_topology_len, shortest_leaf, longest_leaf, leaf_ave_len]
        print_res(dt, f_out)
    return 0
    

if __name__ == '__main__':
    main()
