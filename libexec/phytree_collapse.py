#! /usr/bin/env python3

import argparse
import sys
from biobrary.CircleNode import CircleNodeTree

def getargs(args_in):
    parser = argparse.ArgumentParser(prog='phytree_collapse', description='utilit to \
        collapse phylogenetic tree.')
    subparser = parser.add_subparsers(help='methods to collapse phytree.')
    parser_cluster = subparser.add_parser('cluster', help='user methods cluster to \
        collapse phytree.')
    parser_cluster.add_argument('treefile', help='phylogenetic tree file name in newike \
        format.')
    parser_cluster.add_argument('edge_len_cutoff', type=float, help='edge length to cluster.')
    parser_cluster.add_argument('--cluster_result', default='cluster.fasta', help='file name of cluster result. default is cluster.fasta')
    parser_cluster.add_argument('--collapse_tree', default='collapse_tree.nwk', help='file name of collapse tree. default is collapse_tree.nwk')
    parser_cluster_exclusive = parser_cluster.add_mutually_exclusive_group()
    parser_cluster_exclusive.add_argument('-LK', '--leaf_name_keep', default=None, help='file list, leaf name that want keep, \
        which can not coexist with "leaf_name_remove".')
    parser_cluster_exclusive.add_argument('-LR', '--leaf_name_remove',default=None, help='file list, leaf name that want remove, \
        which can not coexist with "leaf_name_keep".')
    parser_cluster_exclusive.add_argument("-MC", "--manually_choose", default=None, help="file list, choose which leaf left maully.")
    if args_in==None:
        args = parser.parse_args()
        if len(sys.argv) == 1:
            parser.parse_args(['-h'])
        method = sys.argv[1]
    else:
        args = parser.parse_args(args_in)
        if len(args_in) == 0:
            parser.parse_args(['-h'])
        method = args_in[0]
    return method, args


def collapse_cluster(treefile, edge_len_cutoff, leaf_name_keep, leaf_name_remove, cluster_result, \
    collapse_tree, manuall_choose):

    def do_have_keep_leaf(circle_node, keep_leaf):
        inner_node = circle_node.get_inner_node()
        i = 0
        for node in inner_node:
            if node.name in keep_leaf:
                i += 1
        if i > 0:
            return True
        else:
            return False

    circle_node_tree = CircleNodeTree(treefile, edge_len_cutoff)
    original_tree = circle_node_tree.original_tree
    circle_node_tree = circle_node_tree.circle_node_tree
    circle_node_tree.print_cluster(cluster_result)
    all_leafs = original_tree.get_leaf_names()
    circle_node_tree.change_base_inner_node_name()
    if leaf_name_keep:
        keep_leaf = [name.rstrip() for name in open(leaf_name_keep)]
        for circle_node in circle_node_tree.traverse():
            if not do_have_keep_leaf(circle_node, keep_leaf):
                circle_node.trim_inner_node()
        print(original_tree.write(), file=open(collapse_tree, 'w'))

    elif leaf_name_remove:
        remove_leaf = [name.rstrip() for name in open(leaf_name_remove)]
        keep_leaf = list(set(all_leafs) - set(remove_leaf))
        for circle_node in circle_node_tree.traverse():
            if not do_have_keep_leaf(circle_node, keep_leaf):
                circle_node.trim_inner_node()
        print(original_tree.write(), file=open(collapse_tree, 'w'))
    elif manuall_choose:
        #print(original_tree)
        keep_leaf = [name.rstrip() for name in open(manuall_choose)]
        removed_leaf = list(set(all_leafs) - set(keep_leaf))
        #print(removed_leaf)
        for name in removed_leaf:
            try:
                node = original_tree.get_leaves_by_name(name)[0]
                node.delete()
            except:
                print("remove", node, "faild, ignored.")
        #print(original_tree)
        print(original_tree.write(), file=open(collapse_tree, 'w'))
    else:
        for circle_node in circle_node_tree.traverse():
            circle_node.trim_inner_node()
        print(original_tree.write(), file=open(collapse_tree, 'w'))
    return 0


def main(name='phytree_collapse', args=None):
    myname = 'phytree_collapse'
    if myname == name:
        method, args = getargs(args)
        if method == 'cluster':
            collapse_cluster(args.treefile, args.edge_len_cutoff, args.leaf_name_keep, \
                args.leaf_name_remove, args.cluster_result, args.collapse_tree, args.manually_choose)
        else:
            print("Until now, only cluster collapse method was support in this tool.")
            pass
    return 0


if __name__ == '__main__':
    main()
