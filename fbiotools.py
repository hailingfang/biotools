#! /usr/bin/env python3

import argparse
import sys

import libexec.format_fasta_head
import libexec.statistic_assembly
import libexec.phytree_statistic
import libexec.statistic_phytree

def get_args():
    args = argparse.ArgumentParser(description='fbiotools.')
    args.add_argument('cmd_name', help='subcommand name.')
    args.add_argument('cmd_args', nargs='*', help='argument of subcommand.')
    args = args.parse_args([sys.argv[1]])
    cmd_name, cmd_args = args.cmd_name, sys.argv[2:]
    return cmd_name, cmd_args


def main():
    cmd_name, cmd_args = get_args()
    libexec.format_fasta_head.main(cmd_name, cmd_args)
    libexec.statistic_assembly.main(cmd_name, cmd_args)
    libexec.phytree_statistic.main(cmd_name, cmd_args)
    libexec.statistic_phytree.main(cmd_name, cmd_args)
    return 0


if __name__ == '__main__':
    main()
