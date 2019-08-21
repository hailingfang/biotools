#! /usr/bin/env python3
'''
    Calculate similarity between two Nucltide sequence. The query file and subject
    file can have mulitiple items.
    the result is alignment reto of query. mean how long and what proportion the query
    was aligned to subject.
'''
import argparse
import os
import time
import fbio.fparse


def get_args():
    args = argparse.ArgumentParser(description='Calculate similarity between two Nucltide \
        sequence.')
    args.add_argument('-query_file', required=True, type=str, help='query fasta file.')
    args.add_argument('-subject_file', required=True, type=str, help='db fasta file.')
    args = args.parse_args()
    query_file, subject_file = args.query_file, args.subject_file

    return query_file, subject_file


def makeblastdb(subject_file, working_dir):
    cmd_name = 'makeblastdb'
    opt_dbtype = '-dbtype nucl'
    opt_in = '-in ' + subject_file
    out_name_dir = os.path.join(working_dir, os.path.basename(subject_file))
    opt_out = '-out ' + out_name_dir
    cmd = ' '.join([cmd_name, opt_dbtype, opt_in, opt_out])
    print(cmd)
    os.system(cmd)
    return out_name_dir


def run_balstn(query_file, blast_db_name_dir, working_dir):
    cmd_name = 'blastn'
    opt_query = '-query ' + query_file
    opt_db = '-db ' + blast_db_name_dir
    out_res = os.path.join(working_dir, 'blast_res')
    opt_out = '-out ' + out_res
    opt_outfmt = '-outfmt ' + '7'

    cmd = ' '.join([cmd_name, opt_query, opt_db, opt_out, opt_outfmt])
    print(cmd)
    os.system(cmd)
    return out_res


def parse_blastn_res(blast_res):
    '''format is 7 of blastn'''
    dt_out = {}
    a_line = [line.rstrip().split() for line in open(blast_res) if line[0] != '#']
    for line in a_line:
        query_contig, subject_contig, identity, align_len, mismatch, gaps, \
            query_start, query_end, subject_start, subject_end, e_value, score = \
            line
        identity = float(identity)
        align_len = int(align_len)
        mismatch = int(mismatch)
        gaps = int(gaps)
        query_start = int(query_start)
        query_end = int(query_end)
        subject_start = int(subject_start)
        subject_end = int(subject_end)
        e_value = float(e_value)
        score = float(score)

        align_query_len = query_end - query_start + 1
        match_len = align_len - mismatch - gaps
        if query_contig not in dt_out:
            dt_out[query_contig] = {}
        query_pos = (query_start, query_end)
        if query_pos not in dt_out[query_contig]:
            dt_out[query_contig][query_pos] = []
        dt_out[query_contig][query_pos].append([align_len, align_query_len, match_len, \
            subject_start, subject_end, subject_contig])

    return dt_out


def handle_multiple_match_and_overlap(blast_res_dt):

    def get_overlap_range(id_ranges, id_infor):
        dt_out = {}
        tmp = []
        for Range in id_ranges:
            for id in Range:
                tmp.append(id_infor[id])
            # DEBUG: print(tmp)
            tmp.sort(key=lambda x:x[0])
            start = tmp[0][0]
            tmp.sort(key=lambda x:x[1])
            end = tmp[-1][-1]
            dt_out[(start, end)] = tmp
            tmp = []
        print(dt_out)
        return dt_out

    def handle_overlap(pos_liner):
        print(pos_liner)
        pos_marked = []
        i = 0
        id_infor = {}
        for pos in pos_liner:
            i += 1
            id_infor[i] = pos
            pos_marked.append((i, 'L', pos[0]))
            pos_marked.append((i, 'R', pos[1]))
        pos_marked.sort(key=lambda x:x[2])
        container = []
        id_ranges = []
        tmp = []
        for pos in pos_marked:
            if not container:
                container.append(pos[0])
            else:
                if pos[0] in container:
                    container.remove(pos[0])
                    tmp.append(pos[0])
                    if len(container) == 0:
                        id_ranges.append(tmp)
                        tmp = []
                else:
                    container.append(pos[0])
        print(id_ranges)
        overlap_range = get_overlap_range(id_ranges, id_infor)
        return overlap_range

    # -------------
    dt_out = {}
    query_pos_liner = {}
    for query_contig in blast_res_dt:
        # DEBUG: print(query_contig)
        query_pos_liner[query_contig] = []
        for query_pos in blast_res_dt[query_contig]:
            query_pos_liner[query_contig].append(query_pos)
            if len(blast_res_dt[query_contig][query_pos]) > 1:
                # DEBUG: print(blast_res_dt[query_contig][query_pos])
                blast_res_dt[query_contig][query_pos].sort(key=lambda x:x[0])
                blast_res_dt[query_contig][query_pos] = blast_res_dt[query_contig][query_pos][-1]
            else:
                blast_res_dt[query_contig][query_pos] = blast_res_dt[query_contig][query_pos][0]
    for query_contig in blast_res_dt:
        print('>>>>>')
        print(query_contig)
        dt_out[query_contig] = {}
        pos_dt = blast_res_dt[query_contig]
        overlap_range = handle_overlap(pos_dt)
        for range_merged in overlap_range:
            dt_out[query_contig][range_merged] = {}
            for Range in overlap_range[range_merged]:
                dt_out[query_contig][range_merged][Range] = pos_dt[Range]
    return dt_out


def cal_align_rate(align_block_dt, query_file):
    query_dt = fbio.fparse.Fasta_parse(query_file)
    query_dt.join_lines()
    query_dt = query_dt.data
    query_len = 0
    for head in query_dt:
        query_len += len(query_dt[head])
    align_len = 0
    for contig in align_block_dt:
        for align in align_block_dt[contig]:
            block_len = align[1] - align[0] + 1
            if block_len < 0:
                print('ooops')
            align_len += block_len

    align_rate = round(align_len/query_len, 5)

    return query_len, align_len, align_rate


def main():
    time_now = time.strftime('%Y%m%d%H%M%S')
    working_dir = 'working_dir_' + time_now
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    query_file, subject_file = get_args()
    blast_db_name_dir = makeblastdb(subject_file, working_dir)
    blast_res = run_balstn(query_file, blast_db_name_dir, working_dir)
    blast_res_dt = parse_blastn_res(blast_res)
    align_block_dt = handle_multiple_match_and_overlap(blast_res_dt)
    query_len, align_len, align_rate = cal_align_rate(align_block_dt, query_file)
    print(query_len, align_len, align_rate)
    return 0


if __name__ == '__main__':
    main()
