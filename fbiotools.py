#! /usr/bin/env python3

import argparse
import sys

import libexec.format_fasta_head


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('cmd_name', help='subcommand name.\
        \n    format_fasta_head\n')
    args.add_argument('cmd_args', nargs='*', help='argument of subcommand.')
    args = args.parse_args([sys.argv[1]])
    cmd_name, cmd_args = args.cmd_name, sys.argv[2:]
    return cmd_name, cmd_args


def main():
    cmd_name, cmd_args = get_args()
    libexec.format_fasta_head.main(cmd_name, cmd_args)
    return 0




main()
