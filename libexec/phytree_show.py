#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ete3
import argparse


def getargs(args_in):
    parser = argparse.ArgumentParser(prog='phytree_show', description='show phylogeneitc\
        tree.')
    parser.add_argument('nwkfile', help='tree file name in newik format.')
    parser.add_argument('-TF', "--tree_format", default=0, type=int, help="tree format, default is 0. 0: flexible with support values,\
        1: flexible with internal node names, 2: all branches + leaf names + internal supports, 3: all branches + all names. and so on.\
        detail please see http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#reading-and-writing-newick-trees")
    parser.add_argument('-TM', '--tree_mode', choices=['c', 'r'], default='c', help='tree style mode.')
    parser.add_argument('-SBL', '--show_branch_length', action='store_true', help='show branch length')
    parser.add_argument('-SLN' ,'--show_leaf_name', action='store_true', help='show leaf name.')
    parser.add_argument('-SBP', '--show_branch_support', action='store_true', help='show branch support.')
    parser.add_argument('-SIN', '--show_inner_name', action='store_true', help='show inner node name.')
    parser.add_argument('-AL', '--align_leaf_name', action='store_true', help='align leaf name')
    parser.add_argument('-HI', '--hide_inner_node', action='store_true', help='hide inner node point.')
    parser.add_argument('-SP', '--save_plot', action='store_true', help='save plot directly.')
    parser.add_argument("-o", "--out_file", default="plot.pdf", help="file name of saved pdf.")
    if args_in == None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args_in)
    nwkfile, tree_format, tree_mode, show_leaf_name, show_branch_length, show_branch_support, align_leaf_name, \
        hide_inner_node, save_plot, show_inner_name, out_file = args.nwkfile, args.tree_format, args.tree_mode, args.show_leaf_name, \
        args.show_branch_length, args.show_branch_support, args.align_leaf_name, \
        args.hide_inner_node, args.save_plot, args.show_inner_name, args.out_file
    return nwkfile, tree_format, tree_mode, show_leaf_name, show_branch_length, show_branch_support, \
        align_leaf_name, hide_inner_node, save_plot, show_inner_name, out_file


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


def _show_inner_name(tree, tree_format):
    if tree_format != 0:
        return 0
    for node in tree.traverse():
        if (not node.is_leaf()) and (not node.is_root()):
            node_name_face = ete3.TextFace(node.name)
            node.add_face(node_name_face, position='branch-bottom', column=0)
    return 0


def main(name='phytree_show', args=None):
    myname = 'phytree_show'
    if name == myname:
        nwkfile, tree_format, tree_mode, show_leaf_name, show_branch_length, show_branch_support, \
            align_leaf_name, hide_inner_node, save_plot, show_inner_name, out_file = getargs(args)
        tree = ete3.TreeNode(nwkfile, format=tree_format)
        tree_style = ete3.TreeStyle()
        tree_style.mode = tree_mode
        tree_style.show_leaf_name = show_leaf_name
        tree_style.show_branch_length = show_branch_length
        if align_leaf_name:
            tree_style.show_leaf_name = False
            _align_leaf_name(tree)
        if hide_inner_node:
            _hide_inner_node(tree)
        if show_inner_name:
            _show_inner_name(tree, tree_format)
        try:
            if save_plot:
                tree.render(out_file, tree_style=tree_style)
            else:
                tree.show(tree_style=tree_style)
        except:
            print('opps...')
    return 0


if __name__ == '__main__':
    main()
