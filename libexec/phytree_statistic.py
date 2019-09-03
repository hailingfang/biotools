#! /usr/bin/env python3
import argparse
import ete3

def get_args():
    args=argparse.ArgumentParser(description='calculate max distance from leaf to root.')
    args.add_argument('tree_file',type=str,help='tree file name.')
    args=args.parse_args()
    tree_file=args.tree_file
    return tree_file

def get_longest_dist(tree):
    el_max=tree.get_farthest_leaf()
    nl_max=tree.get_farthest_leaf(topology_only=True)
    return el_max,nl_max

def get_average_leaf_dist(tree):
    len_all=[]
    for leaf in tree:
        len_all.append([leaf.name,leaf.dist])
    sort_f=lambda x:x[1]
    len_all.sort(key=sort_f)
    shortest_leaf=[]
    min_len=len_all[0][1]
    for ele in len_all:
        if ele[1]==min_len:
            shortest_leaf.append(ele)
    longest_leaf=[]
    max_len=len_all[-1][1]
    for ele in len_all:
        if ele[1]==max_len:
            longest_leaf.append(ele)
    leaf_ave_len=sum([x[1] for x in len_all])/len(len_all)
    return shortest_leaf,longest_leaf,leaf_ave_len


if __name__ == '__main__':
    tree_file=get_args()
    tree=ete3.Tree(tree_file)
    el_max,nl_max=get_longest_dist(tree)
    shortest_leaf,longest_leaf,leaf_ave_len=get_average_leaf_dist(tree)
    print('el_max:',el_max[0].name, el_max[1])
    print('nl_max:',nl_max[0].name, nl_max[1])
    print('shortest_leaf:',shortest_leaf)
    print('longest_leaf:',longest_leaf)
    print('leaf_ave_len:',leaf_ave_len)

