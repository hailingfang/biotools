import argparse
import biobrary.bioparse as biop
import sys


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta_file", required=True, help="FASTA file")
    parser.add_argument("--gtf_file", required=True, help="GTF file")
    parser.add_argument("gene_id", help="gene ID")

    args = parser.parse_args()
    return args.fasta_file, args.gtf_file, args.gene_id


def extra_gene_info(gtf, gene_id):
    pass


def main():
    fasta_file, gtf_file, gene_id = getargs()
    gtf =  biop.parse_gtf(gtf_file)
    fasta = biop.parse_fasta(fasta_file)
    gene = gtf.get_gene(gene_id)
    if not gene:
        print(f"{gene_id} not found in GTF file.")
        exit()
    gene_name = gene.get_gene_name()
    print(gtf.get_gene_id_by_name(gene_name), file=sys.stderr)

    print(">" + gene_name)
    seq_name = gene.get_seq_name()
    gene_range = gene.get_range()
    gene_range_s = ';'.join([str(ele[0]) + ',' + str(ele[1]) for ele in gene_range])
    ori = gene.get_ori()
    print('\t'.join(["&" + gene_id, seq_name, gene_range_s, ori]))

    transcripts = gene.get_transcript_s()
    for trans in transcripts:
        trans_id = trans.get_transcript_id()
        exon = trans.get_exon()
        exon_range = exon.get_range()
        exon_range = ';'.join([str(ele[0]) + ',' + str(ele[1]) for ele in exon_range])
        gbkey = exon.get_attr('gbkey')
        biotype = exon.get_biotype()
        start = trans.get_start_codon()
        stop = trans.get_stop_codon()
        start_range = start.get_range()
        start_range = ';'.join([str(ele[0]) + ',' + str(ele[1]) for ele in start_range])
        stop_range = stop.get_range()
        stop_range = ';'.join([str(ele[0]) + ',' + str(ele[1]) for ele in stop_range])
        biotype = gbkey if gbkey else biotype
        if not biotype:
            if trans.get_CDS():
                biotype = 'mRNA'
            else:
                biotype = 'None'

        print('\t'.join(['$' + trans_id, biotype, exon_range, start_range, stop_range]))

    entry = fasta.get_seq_entry(seq_name)
    seq = entry.get_seq()
    seq = seq[gene_range[0][0] - 1: gene_range[0][1]]

    seq_slic = list(range(0, len(seq), 80))
    seq_slic.append(len(seq))
    for idx in range(len(seq_slic) - 1):
        print(seq[seq_slic[idx]: seq_slic[idx + 1]])


if __name__ == "__main__":
    main()