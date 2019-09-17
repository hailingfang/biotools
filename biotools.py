#! /usr/bin/env python3

import argparse
import sys


import libexec.format_fasta_head
import libexec.statistic_assembly
import libexec.phytree_statistic
import libexec.statistic_phytree
import libexec.find_up_down_genes
import libexec.phytree_groups
import libexec.phytree_collapse


def get_args():
    args = argparse.ArgumentParser(description='fbiotools.')
    args.add_argument('cmd_name', help='subcommand name.')
    args.add_argument('cmd_args', nargs='*', help="argument of subcommand.\
        [format_fasta_head, statistic_assembly, phytree_statistic, \
        statistic_phytree, find_up_down_genes, phytree_groups, phytree_collapse]")
    args = args.parse_args([sys.argv[1]])
    cmd_name, cmd_args = args.cmd_name, sys.argv[2:]
    return cmd_name, cmd_args


def main():
    cmd_name, cmd_args = get_args()
    libexec.format_fasta_head.main(cmd_name, cmd_args)
    libexec.statistic_assembly.main(cmd_name, cmd_args)
    libexec.phytree_statistic.main(cmd_name, cmd_args)
    libexec.statistic_phytree.main(cmd_name, cmd_args)
    libexec.find_up_down_genes.main(cmd_name, cmd_args)
    libexec.phytree_groups.main(cmd_name, cmd_args)
    libexec.phytree_collapse.main(cmd_name, cmd_args)
    return 0


if __name__ == '__main__':
    main()
