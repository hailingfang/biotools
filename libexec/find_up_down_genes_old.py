#! /usr/bin/env python3
'''
This utility is aimed to find out up and down stream genes of a location.
The gff file data needed as basic data.
'''
import argparse
import sys
import fbio.fparse


def get_args():
    args = argparse.ArgumentParser(description='This utility is aimed to find \
        find out up and down stream genes of location.')
    args.add_argument('contig', type=str, help='contig index')
    args.add_argument('start_position', type=int, help='start position of a location.')
    args.add_argument('end_position', type=int, help='end position of a location.')
    args.add_argument('-gff_file', type=str, required=True, help='gff file path of genome that \
        you want fine analysis.')
    args.add_argument('-range', type=int, required=True, help='base or gene length \
        range of up and down stream that offer genes of it.')
    args.add_argument('-range_type', type=str, required=True, choices=['base', 'gene'], \
        help='gene number range of up and down stream that offer genes of it')
    args.add_argument('-out_f', type=str, default=sys.stdout, help='result outputing file. \
        stdout as default.')
    args = args.parse_args()
    contig, start_position, end_position, gff_file, range, range_type, out_f = \
        args.contig, args.start_position, args.end_position, args.gff_file, \
        args.range, args.range_type, args.out_f

    return contig, start_position, end_position, gff_file, range, range_type, out_f


def parse_gff_file(gff_file):

    def adept_dt_struc(gff_dt):
        dt_out = {}
        for contig in gff_dt:
            # DEBUG: print(contig)
            if contig not in dt_out:
                dt_out[contig] = {}
            for source in gff_dt[contig]:
                # DEBUG: print(source)
                for seq_type in gff_dt[contig][source]:
                    if seq_type not in dt_out[contig]:
                        dt_out[contig][seq_type] = {}
                        for position in gff_dt[contig][source][seq_type]:
                            if position not in dt_out[contig][seq_type]:
                                dt_out[contig][seq_type][position] = []
                            dt_out[contig][seq_type][position].append(gff_dt[contig][source][seq_type][position])
        for contig in dt_out:
            dt_out[contig].pop('region')
        tmp = {}
        for contig in dt_out:
            if contig not in tmp:
                tmp[contig] = {}
            for seq_type in dt_out[contig]:
                for position in dt_out[contig][seq_type]:
                    if position not in tmp[contig]:
                        tmp[contig][position] = {}
                    tmp[contig][position][seq_type] = dt_out[contig][seq_type][position]
        dt_out = tmp
        return dt_out

    dt = fbio.fparse.Gff_parse(gff_file)
    dt = dt.data['information']
    dt_adepted = adept_dt_struc(dt)
    return dt_adepted


def get_up_down_gene(contig, start_position, end_position, range, range_type, gff_dt):

    def judge_position(block, num):
        if num[1] <= block[0] or num[0] >= block[1]:
            return 0
        elif (num[1] > block[0] and num[1] <= block[1]) or (num[0] < block[1] and num[0] >= block[0] ):
            return 1
        else:
            return 3

    def add_ele_type(gene_up_down, start_position, end_position):
        dt_out = {}
        block = (start_position, end_position)
        for side in gene_up_down:
            if side not in dt_out:
                dt_out[side] = []
            for ele in gene_up_down[side]:
                ele_type = judge_position(block, ele)
                dt_out[side].append([ele, ele_type])
        return dt_out


    def offer_ele_by_gene_range(start_side_ele, start_position, start_gene_range, \
        end_side_ele, end_position, end_gene_range):
        data_out = {'start_side':[], 'end_side':[]}
        data_out['start_side'] = start_side_ele[-start_gene_range : ]
        data_out['end_side'] = end_side_ele[: end_gene_range]
        return data_out

    def offer_ele_by_base_range(start_side_ele, start_position, start_base_range, \
        end_side_ele, end_position, end_base_range):
        data_out = {'start_side':[], 'end_side':[]}
        start_cut = start_position - start_base_range
        end_cut = end_position + end_base_range
        for ele in start_side_ele:
            if ele[0] >= start_cut:
                data_out['start_side'].append(ele)
        for ele in end_side_ele:
            if ele[1] <= end_cut:
                data_out['end_side'].append(ele)
        return data_out

    if start_position < end_position:
        oritation = '+'
    else:
        start_position, end_position = end_position, start_position
        oritation = '-'
    dt = gff_dt[contig]
    liner_position = []
    for position in dt:
        liner_position.append(position)
    liner_position.sort(key=lambda x:x[0])
    #print(liner_position)
    start_side_ele = []
    for ele in liner_position:
        if ele[0] < start_position:
            start_side_ele.append(ele)
    liner_position.sort(key=lambda x:x[1])
    end_side_ele = []
    for ele in liner_position:
        if ele[1] > end_position:
            end_side_ele.append(ele)
    #print(start_side_ele)
    #print(end_side_ele)

    if range_type == 'gene':
        genes = offer_ele_by_gene_range(start_side_ele, start_position, range, \
            end_side_ele, end_position, range)
        genes = add_ele_type(genes, start_position, end_position)
    elif range_type == 'base':
        genes = offer_ele_by_base_range(start_side_ele, start_position, range, \
            end_side_ele, end_position, range)
        genes = add_ele_type(genes, start_position, end_position)
    else:
        raise Exception('Unrecgnised range type.')

    genes['start_side'].sort(key=lambda x:x[0][0], reverse=True)
    if oritation == '-':
        genes['start_side'], genes['end_side'] = genes['end_side'], genes['start_side']

    return genes, oritation


def print_res(contig, start_position, end_position, oritation, up_down_genes, gff_dt, f_out=sys.stdout):

    def make_line(ele, seq_type, record, ele_type):
        dt_out = None
        # DEBUG: print(record)
        position = '(' + str(ele[0]) + ',' + str(ele[1]) + ')'
        ele_type = str(ele_type)
        strand = record['strand']
        phase = record['phase']
        attrs = []
        for attr in record['attributes']:
            attrs.append(attr + '=' + record['attributes'][attr])
        attrs = ';'.join(attrs)
        dt_out = [position, ele_type, seq_type, strand, phase, attrs]
        dt_out = '\t'.join(dt_out)
        return dt_out

    print('>', '('+str(start_position) + ',' + str(end_position) + ')', oritation, contig, file=f_out)
    print('>> start_side', file=f_out)
    for ele in up_down_genes['start_side']:
        ele_type = ele[1]
        ele = ele[0]
        infor = gff_dt[contig][ele]
        for seq_type in infor:
            for record in infor[seq_type]:
                line = make_line(ele, seq_type, record, ele_type)
                print(line, file=f_out)
    print('>> end_side', file=f_out)
    for ele in up_down_genes['end_side']:
        ele_type = ele[1]
        ele = ele[0]
        infor = gff_dt[contig][ele]
        for seq_type in infor:
            for record in infor[seq_type]:
                line = make_line(ele, seq_type, record, ele_type)
                print(line, file=f_out)
    return 0


def main():
    contig, start_position, end_position, gff_file, range, range_type, out_f = get_args()
    gff_dt = parse_gff_file(gff_file)
    up_down_genes, oritation = get_up_down_gene(contig, start_position, end_position, range, range_type, gff_dt)
    #print(up_down_genes)
    if out_f != sys.stdout:
        out_f = open(out_f, 'w')
    print_res(contig, start_position, end_position, oritation, up_down_genes, gff_dt, out_f)
    out_f.close()
    return 0


if __name__ == '__main__':
    main()
