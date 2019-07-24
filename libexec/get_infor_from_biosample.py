#! /usr/bin/env python3
import argparse
import re
import sys

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('f_in', type=str, help='biosample file name download form NCBI.')
    args.add_argument('-f_out', default=sys.stdout, help='output file. stdout as default.')
    args.add_argument('-infor_key', nargs='+', default=['BioSample', 'SRA', 'strain', 'isolate', \
        'collection date', 'geographic location', 'latitude and longitude'], help='information key \
        that interested in and want extracted.')
    args = args.parse_args()
    biosample_f, f_out, infor_key = args.f_in, args.f_out, args.infor_key
    # DEBUG: print(infor_key)
    return biosample_f, f_out, infor_key

def get_info(biosample_f, infor_key=['BioSample', 'SRA', 'strain', 'isolate', \
    'collection date', 'geographic location', 'latitude and longitude']):
    def yield_block(biosample_f):
        block = []
        i = 0
        for line in open(biosample_f):
            line = line.rstrip()
            if i == 1 and line != '':
                yield block
                block = []
                i =0
            if line != '':
                block.append(line)
            else:
                i = 1
        if len(block) > 0:
            yield block

    def get_block_infor(block):
        data_out ={}
        biosample_re = re.compile(r'BioSample:\s(.+?)(?:;|$)')
        sra_re = re.compile(r'SRA:\s(.+?)(?:;|$)')
        attribute_re = re.compile(r'^\s+?/(.+?)="(.+?)"$')
        for line in block:
            biosample = biosample_re.search(line)
            sra = sra_re.search(line)
            attribute = attribute_re.search(line)
            if biosample:
                data_out['BioSample'] = biosample.groups()[0]
            if sra:
                data_out['SRA'] = sra.groups()[0]
            if attribute:
                data_out[attribute.groups()[0]] = attribute.groups()[1]
        return data_out

    data_out = []
    for block in yield_block(biosample_f):
        infor = get_block_infor(block)
        # DEBUG: print(infor)
        record = []
        for key in infor_key:
            value = infor.get(key, 'None')
            record.append(value)
        data_out.append(record)
    return data_out


def print_res(infor, f_out=sys.stdout, head_key=['BioSample', 'SRA', 'strain', 'isolate', \
    'collection date', 'geographic location', 'latitude and longitude']):
    print('#' + '\t'.join(head_key), file=f_out)
    for line in infor:
        print('\t'.join(line), file=f_out)


def main():
    biosample_f, f_out, infor_key = get_args()
    infor = get_info(biosample_f, infor_key)
    if f_out != sys.stdout:
        f_out = open('f_out', 'w')
    print_res(infor, f_out, infor_key)
    if f_out != sys.stdout:
        f_out.close()
    return 0


if __name__ == '__main__':
    main()
