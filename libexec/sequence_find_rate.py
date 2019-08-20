#! /usr/bin/env python3
'''
    Calculate similarity between two Nucltide sequence. The query file and subject
    file can have mulitiple items.
'''
import argparse
import os
import time

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
        score = int(score)

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
    def handle_overlap(pos_liner):
        dt_out = {}
        pos_marked = []
        i = 0
        id_infor = {}
        for pos in pos_liner:
            i += 1
            id_infor[i] = pos
            pos_marked.append((i, 'L', pos[0]))
            pos_marked.append((i, 'R', pos[1]))
        pos_marked.sort(key=lambda x:x[2])

        container = None
        id_ranges = []
        tmp = []
        for pos in pos_marked:
            if not container:
                container.append(pos[0])
            else:
                if pos[0] in container:
                    container.remove(i)
                    tmp.append(pos[0])
                    if len(container) == 0:
                        id_ranges.append(tmp)
                        tmp = []
                else:
                    container.append(pos[0])

        return 0

    dt_out = {}
    query_pos_liner = {}
    for query_contig in blast_res_dt:
        query_pos_liner[query_contig] = []
        for query_pos in blast_res_dt[query_contig]:
            query_pos_liner[query_contig].append(query_pos)
            if len(blast_res_dt[query_contig][query_pos]) > 1:
                blast_res_dt[query_contig][query_pos].sort(key=lambda x:x[0])
                blast_res_dt[query_contig][query_pos] = blast_res_dt[query_contig][query_pos][-1]
            else:
                blast_res_dt[query_contig][query_pos] = blast_res_dt[query_contig][query_pos][0]
    for query_contig in blast_res_dt:
        pos_dt = blast_res_dt[query_contig]
        handle_overlap(pos_dt)

    return 0

def main():
    time_now = time.strftime('%Y%mD%H%M%S')
    working_dir = 'working_dir_' + time_now
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    query_file, subject_file = get_args()
    blast_db_name_dir = makeblastdb(subject_file, working_dir)
    blast_res = run_balstn(query_file, blast_db_name_dir, working_dir)
    blast_res_dt = parse_blastn_res(blast_res)


    return 0


if __name__ == '__main__':
    main()
