#! /usr/bin/env python3

import argparse
from biobrary.tree import CircleNodeTree


def getargs(args_in):
    args = argparse.ArgumentParser(description="This is a utility to cluster a tree's \
        node according to length of edge.", prog='phytree_groups')
    args.add_argument('treefile', type=str, help='file name of newike tree.')
    args.add_argument('edge_len_cutoff', type=float, help='cutoff of edge length to \
        make a circlal cluster.')
    args.add_argument('--f_cluster_res', type=str, default='cluster.fasta', help='\
        file name to output cluster result, default is "cluster.fasta".')
    args.add_argument('--f_profile_tree', type=str, default='profile.nwk', help='\
        CircleNode Tree profile tree file. default is "profile.nwk".')
    if args_in == None:
        args =args.parse_args()
    else:
        args = args.parse_args(args_in)
    treefile, edge_len_cutoff, f_cluster_res, f_profile_tree = args.treefile, \
        args.edge_len_cutoff, args.f_cluster_res, args.f_profile_tree
    return treefile, edge_len_cutoff, f_cluster_res, f_profile_tree


def main(name='phytree_cluster', args=None):
    myname = 'phytree_cluster'
    if name == myname:
        treefile, edge_len_cutoff, f_cluster_res, f_profile_tree = getargs(args)
        circle_node_tree = CircleNodeTree(treefile, edge_len_cutoff)
        circle_node_tree = circle_node_tree.circle_node_tree
        profile_tree = circle_node_tree.make_profile_tree()
        print(profile_tree.write(features=['name']), file=open(f_profile_tree, 'w'))
        circle_node_tree.print_cluster(f_cluster_res)
    return 0


if __name__ == '__main__':
    main()
