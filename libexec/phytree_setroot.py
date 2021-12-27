import ete3
import argparse

def getargs(args):
    parser = argparse.ArgumentParser(prog='phytree_setroot', description='set root of tree.')
    parser.add_argument('nwkfile', help='tree file name in newick format.')
    parser.add_argument("-TF", "--tree_format", default=0, type=int, help="newick tree format. default is 0.")
    parser.add_argument("-OG", "--out_group", default=None, type=str, help="name of outgroup.")
    parser.add_argument("-o", "--out_file", default="tree_rooted.nwk", help="file name of output.")
    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parser_args()
    nwkfile, tree_format, out_group, out_file = args.nwkfile, args.tree_format, args.out_group, args.out_file
    return nwkfile, tree_format, out_group, out_file


def main(name="phytree_setroot", args=None):
    myname = "phytree_setroot"
    if name == myname:
        nwkfile, tree_format, out_group, out_file = getargs(args)
        tree = ete3.Tree(nwkfile, format=tree_format)
        if out_group:
            out_group_node = tree.get_leaves_by_name(out_group)
            if out_group_node:
                tree.set_outgroup(out_group_node[0])
            else:
                print(out_group, "not found, use midpoint as root.")
        else:
            tree.set_outgroup(tree.get_midpoint_outgroup())
        tree.write(outfile=out_file, format=tree_format)
    return 0

