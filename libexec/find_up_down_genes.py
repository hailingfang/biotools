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
    args.add_argument('-f_out', type=str, default=sys.stdout, help='result outputing file. \
        stdout as default.')
    args = args.parse_args()
    contig, start_position, end_position, gff_file, range, range_type, f_out = \
        args.contig, args.start_position, args.end_position, args.gff_file, \
        args.range, args.range_type, args.f_out
    return contig, start_position, end_position, gff_file, range, range_type, f_out


class Position_find:

    def left_elements(self, element_seq, position):
        dt_out = []
        element_seq.sort(key=lambda x:x[1])
        for ele in element_seq:
            if ele[1] < position:
                dt_out.append(ele)
        return dt_out

    def mid_elements(self, element_seq, position):
        dt_out = []
        element_seq.sort(key=lambda x:x[0])
        for ele in element_seq:
            if ele[0] < position:
                if ele[1] >= position:
                    dt_out.append(ele)
            elif ele[0] == position:
                if ele[1] > position:
                    dt_out.append(ele)
        return dt_out

    def right_elements(self, element_seq, position):
        dt_out = []
        element_seq.sort(key=lambda x:x[0])
        for ele in element_seq:
            if ele[0] > position:
                dt_out.append(ele)
        return dt_out

    def left_elements_by_num(self, element_seq, position, num):
        left_ele = self.left_elements(element_seq, position)
        dt_out = left_ele[-num : ]
        return dt_out

    def mid_elements_by_num_left(self, element_seq, position, num):
        dt_out = []
        mid_ele = self.mid_elements(element_seq, position)
        mid_ele.sort(key=lambda x:x[0])
        dt_out = mid_ele[-num : ]
        return dt_out

    def mid_elements_by_num_right(self, element_seq, position, num):
        dt_out = []
        mid_ele = self.mid_elements(element_seq, position)
        mid_ele.sort(key=lambda x:x[1])
        dt_out = mid_ele[ : num]
        return dt_out

    def right_elements_by_num(self, element_seq, position, num):
        right_ele = self.right_elements(element_seq, position)
        dt_out = right_ele[ : num]
        return dt_out

    def left_elements_by_len(self, element_seq, position, length):
        dt_out = []
        left_ele = self.left_elements(element_seq, position)
        left_cut = position - length
        for ele in left_ele:
            if ele[0] >= left_cut:
                dt_out.append(ele)
        return dt_out

    def mid_elements_by_len_left(self, element_seq, position, length):
        dt_out = []
        left_cut = position - length
        mid_ele = self.mid_elements(element_seq, position)
        mid_ele.sort(key=lambda x:x[0])
        for ele in mid_ele:
            if ele[0] >= left_cut:
                dt_out.append(ele)
        return dt_out

    def mid_elements_by_len_right(self, element_seq, position, length):
        dt_out = []
        right_cut = position + length
        mid_ele = self.mid_elements(element_seq, position)
        mid_ele.sort(key=lambda x:x[1])
        for ele in mid_ele:
            if ele[1] <= right_cut:
                dt_out.append(ele)
        return dt_out

    def right_elements_by_len(self, element_seq, position, length):
        dt_out = []
        right_ele = self.right(element_seq, position)
        right_cut = position + length
        for ele in right_ele:
            if ele[1] <= right_cut:
                dt_out.append(ele)
        return dt_out


def parse_gff_file(gff_file):

    def adept_dt_struc(gff_dt):
        dt_out = {}
        for contig in gff_dt:
            dt_out[contig] = {}
            for source in gff_dt[contig]:
                for seq_type in gff_dt[contig][source]:
                    if seq_type == 'region':
                        continue
                    for position in gff_dt[contig][source][seq_type]:
                        if position not in dt_out[contig]:
                            dt_out[contig][position] = {}
                        #dt_out[contig][position][seq_type] = []
                        dt_out[contig][position][seq_type] = gff_dt[contig][source][seq_type][position]
        return dt_out

    dt = fbio.fparse.Gff_parse(gff_file)
    dt = dt.data['information']
    dt_adepted = adept_dt_struc(dt)
    return dt_adepted


def get_left_right_ele(contig, start_position, end_position, range, range_type, gff_dt):

    dt_out = {'Left_boundary_left_ele':None, 'Right_boundary_right_ele':None, \
        'Left_boundary_mid_ele':None, 'Right_boundary_mid_ele':None}
    oritation = '+' if start_position < end_position else '-'
    if oritation == '+':
        left_boundary = start_position
        right_boundary = end_position
    else:
        left_boundary = end_position
        right_boundary = start_position
    element_seq = list(gff_dt[contig].keys())
    # DEBUG: print(element_seq)
    fuc_instance = Position_find()

    dt_out['Left_boundary_mid_ele'] = fuc_instance.mid_elements_by_num_left(element_seq, left_boundary, 1)
    dt_out['Right_boundary_mid_ele'] = fuc_instance.mid_elements_by_num_right(element_seq, right_boundary, 1)
    if range_type == 'gene':
        dt_out['Left_boundary_left_ele'] = fuc_instance.left_elements_by_num(element_seq, left_boundary, range)
        dt_out['Right_boundary_right_ele'] = fuc_instance.right_elements_by_num(element_seq, right_boundary, range)
    elif range_type == 'base':
        dt_out['Left_boundary_left_ele'] = fuc_instance.left_elements_by_len(element_seq, left_boundary, range)
        dt_out['Right_boundary_right_ele'] = fuc_instance.right_elements_by_len(element_seq, right_boundary, range)

    return dt_out, oritation


def print_res(contig, start_position, end_position, oritation, left_right_ele, gff_dt, f_out=sys.stdout):

    def get_position_infor_line(contig, position, gff_dt):
        line = []
        infor = gff_dt[contig][position]
        start = position[0]
        end = position[1]
        line = [str(start), str(end)]
        for seq_type in infor:
            line.append(seq_type)
            strand = infor[seq_type]['strand']
            phase = infor[seq_type]['phase']
            attrs = infor[seq_type]['attributes']
            tmp = []
            for key in attrs:
                tmp.append(key + '=' + attrs[key])
            attrs = ';'.join(tmp)
            line.append(strand)
            line.append(phase)
            line.append(attrs)
        line = '\t'.join(line)
        return line

    head_line = '\t'.join(['>', str(start_position), str(end_position), oritation, contig])
    print(head_line, file=f_out)
    if oritation == '+':
        upmid = left_right_ele['Left_boundary_mid_ele']
        upele = left_right_ele['Left_boundary_left_ele']
        downmid = left_right_ele['Right_boundary_mid_ele']
        downele = left_right_ele['Right_boundary_right_ele']
    else:
        upmid = left_right_ele['Right_boundary_mid_ele']
        upele = left_right_ele['Right_boundary_right_ele']
        downmid = left_right_ele['Left_boundary_mid_ele']
        downele = left_right_ele['Left_boundary_left_ele']
    print('UPMID   ', end='', file=f_out)
    i = 0
    for ele in upmid:
        if i != 0: print(' ' * 8, end='', file=f_out)
        i += 1
        line= get_position_infor_line(contig, ele, gff_dt)
        print(line, file=f_out)
    print('DOWNMID ', end='', file=f_out)
    i = 0
    for ele in downmid:
        if i != 0: print(' ' * 8, end='', file=f_out)
        i += 1
        line = get_position_infor_line(contig, ele, gff_dt)
        print(line, file=f_out)
    print('UPELE   ', end='', file=f_out)
    i = 0
    for ele in upele:
        if i != 0: print(' ' * 8, end='', file=f_out)
        i += 1
        line = get_position_infor_line(contig, ele, gff_dt)
        print(line, file=f_out)
    print('DOWNELE ', end='', file=f_out)
    i = 0
    for ele in downele:
        if i != 0: print(' ' * 8, end='', file=f_out)
        i += 1
        line = get_position_infor_line(contig, ele, gff_dt)
        print(line, file=f_out)
    return 0


def main():
    contig, start_position, end_position, gff_file, range, range_type, f_out = get_args()
    gff_dt = parse_gff_file(gff_file)
    left_right_ele, oritation = get_left_right_ele(contig, start_position, end_position, range, range_type, gff_dt)
    # DEBUG: print(left_right_ele)
    # DEBUG: print(oritation)
    if f_out != sys.stdout: f_out = open(f_out, 'w')
    print_res(contig, start_position, end_position, oritation, left_right_ele, gff_dt, f_out)
    if f_out != sys.stdout: f_out.close()
    return 0


if __name__ == '__main__':
    main()
