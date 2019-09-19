#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ete3
import argparse


def getargs(args_in):
    parser = argparse.ArgumentParser(prog='phytree_show', description='show phylogeneitc\
        tree.')
    parser.add_argument('nwkfile', help='tree file name in newik format.')
    parser.add_argument('-TM', '--tree_mode', choices=['c', 'r'], default='r', help='tree style mode.')
    parser.add_argument('--show_branch_length', action='store_true', help='show branch length')
    parser.add_argument('--show_leaf_name', action='store_true', help='show leaf name.')
    parser.add_argument('--show_branch_support', action='store_true', help='show branch support.')
    parser.add_argument('--align_leaf_name', action='store_true', help='align leaf name')
    parser.add_argument('--hide_inner_node', action='store_true', help='hide inner node.')
    if args_in == None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args_in)
    nwkfile, tree_mode, show_leaf_name, show_branch_length, show_branch_support, align_leaf_name, \
        hide_inner_node = args.nwkfile, args.tree_mode, args.show_leaf_name, args.show_branch_length, \
        args.show_branch_support, args.align_leaf_name, args.hide_inner_node
    return nwkfile, tree_mode, show_leaf_name, show_branch_length, show_branch_support, \
        align_leaf_name, hide_inner_node


def _align_leaf_name(tree):
    attr_face = ete3.AttrFace('name')
    text_face = ete3.TextFace('  ')
    for leaf in tree:
        leaf.add_face(text_face, column=0, position='aligned')
        leaf.add_face(attr_face, column=1, position='aligned')
    return 0


def _hide_inner_node(tree):
    ns = ete3.NodeStyle()
    ns['size'] = 0
    for node in tree.traverse():
        if (not node.is_leaf()) and (not node.is_root()):
            node.set_style(ns)
    return 0


def main(name='phytree_show', args=None):
    myname = 'phytree_show'
    if name == myname:
        nwkfile, tree_mode, show_leaf_name, show_branch_length, show_branch_support, \
            align_leaf_name, hide_inner_node = getargs(args)
        tree = ete3.TreeNode(nwkfile)
        tree_style = ete3.TreeStyle()
        tree_style.mode = tree_mode
        tree_style.show_leaf_name = show_leaf_name
        tree_style.show_branch_length = show_branch_length
        if align_leaf_name:
            tree_style.show_leaf_name = False
            _align_leaf_name(tree)
        if hide_inner_node:
            _hide_inner_node(tree)
        try:
            tree.show(tree_style=tree_style)
        except:
            print('opps...')
    return 0


if __name__ == '__main__':
    main()
