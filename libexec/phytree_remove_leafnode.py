#! /usr/bin/env python3
import ete3
import argparse
import sys

def get_args():
    args=argparse.ArgumentParser()
    args.add_argument('-tree_file',type=str,required=True,help='name of tree tree file.')
    args.add_argument('-leaf_name_rm',type=str,required=True,help='leaf node name file name.')
    args.add_argument('-mode',default='a',choices=['a','b'],help='leaf remove mode. "a" mean remove leaf and parent and connect sister. "b" just remove leaf node.')
    #args.add_agument('-f_out',default=sys.stdout,type=str,help='file name of result. default is stdout.')
    args=args.parse_args()
    tree_file,leaf_list,mode=args.tree_file,args.leaf_name_rm,args.mode

    return tree_file,leaf_list,mode

def remove_node_mode_a(tree,node):
    #remove node parent node and connect dist.
    parent=node.get_ancestors()[0]
    if parent.is_root():
        node.delete()
    else:
        grand_parent=parent.get_ancestors()[0]
        parent_dist=parent.dist
        parent.detach()
        for sister in node.get_sisters():
            sister.dist=sister.dist + parent_dist
            grand_parent.add_child(sister)

def remove_node_mode_b(tree,node):
    #just detach the node.
    node.detach()

def main():
    tree_file,leaf_list,mode=get_args()
    tree=ete3.Tree(tree_file)
    leaf_names=[line.rstrip() for line in open(leaf_list)]
    for leaf in tree:
        if leaf.name in leaf_names:
            if mode == 'a':
                remove_node_mode_a(tree,leaf)
            elif mode == 'b':
                remove_node_mode_b(tree,leaf)

    print(tree.write())

if __name__ == '__main__':
    main()
