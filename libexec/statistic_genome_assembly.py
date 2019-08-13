#! /usr/bin/env python3 

import copy
class Fasta_parse:
    """
    this class was writed to parse fasta file. 

    And there are three methods within class. fist is __inint__, to add data and seq_heads attibution to Instance. The second is fasta_print, to print self.data back to fasta file, and the length of fasta file line can be modifed by argrment 'line_len', dauflt length is 80 characters. The third is join_lines, which will modified self.data, and make value into a line

    And Instance contain tow attibution. one is data, it is a dictionary contain the information of fasta file, and the key is head line, and the value is the seq. second attribution is seq_heads this is a list, contain all head line of fasta file and by the fasta file order.
    """

    def __init__(self,file_name):
        def check_file_format(file_name):
            all_first_char=[line[0] for line in open(file_name)]
            all_char=[char for char in all_first_char if char != '>']
            #string=''.join(all_char)

            i=0
            if all_first_char[0]=='>': pass
            else: i=1
            #if string.isalpha: pass
            #else: i=1

            if i:
                return False
            else:
                return True


        check_res=check_file_format(file_name)
        #print(check_res)
        if check_res:
            self.fileformat='fasta'

            data={}
            seq_heads=[]
            for line in open(file_name,'r'):
                line=line.rstrip()
                if line[0]=='>':
                    key=line[1:]
                    seq_heads.append(key)
                    data[key]=[]
                else:
                    data[key].append(line)
            self.data=data
            self.seq_heads=seq_heads
            self.print_len=80

        else:
            print('The file may not be a fasta file.')
            exit()




    def join_lines(self):
        for key in self.data:
            self.data[key]=''.join(self.data[key])




    def summary_data(self):
        data=copy.deepcopy(self.data) 
        for key in data:
            data[key]=''.join(data[key])
        len_list=[len(data[key]) for key in data]
        len_list.sort()

        total_len=sum(len_list)
        num_seq=len(len_list)
        max_len=len_list[-1]
        min_len=len_list[0]
        ava_len=float(format(total_len/num_seq,'0.2f')) if num_seq>0 else 0
        
        N50=0
        half_total_len=total_len/2
        start=0

        for seq_len in len_list:
            start+=seq_len
            if start >= half_total_len:
                N50=seq_len
                break
        res={'total_len':total_len,'num_seq':num_seq,'max_len':max_len,'min_len':min_len,'ava_len':ava_len,'N50':N50}
        return res





    def fasta_print(self,line_len=80):
        for key in self.seq_heads:
            print('>'+key)
            whole_line=''.join(self.data[key])

            i=0
            part=whole_line[i:i+line_len]
            while part:
                print(part)
                i+=line_len
                part=whole_line[i:i+line_len]
   





#    def __str__(self):
#        new_str=''
#        for key in self.data:
#            new_str+='>'+key+'\n'
#            whole_line=''.join(self.data[key])
#
#            i=0
#            part=whole_line[i:i+self.print_len]
#            while part:
#                new_str+=part+'\n'
#                i+=self.print_len
#                part=whole_line[i:i+self.print_len]
#        return new_str[:-1]


#    def set_print_len(self,line_len):
#        self.print_len=line_len





def statistic_assembly(data):
    
    data_sta={}
    len_list=[]
    for head in data:
        seq=''.join(data[head])
        length=len(seq)
        GC_num=len([base for base in seq if base=='G' or base=='C'])
        data_sta[head]=[length,GC_num]
        len_list.append(length)

    totall_len=0
    totall_GC=0

    for head in data_sta:
        totall_len+=data_sta[head][0]
        totall_GC+=data_sta[head][1]

    len_list.sort(reverse=True)
    max_len=0
    min_len=0
    if len(len_list):
        max_len=len_list[0]
        min_len=len_list[-1]
    num_contig=len(len_list)
    ava_len=totall_len/num_contig if num_contig >0 else 0
    GC_content=totall_GC/totall_len if totall_len >0 else 0

    start=0
    half_len=totall_len/2
    L50=0
    N50=0
   # print(half_len)
   # print(len_list)
    for num in len_list:
        start+=num
        L50+=1
        #print(start)
        if start >= half_len:
            N50=num
            break

    #print(totall_len,num_contig,max_len,min_len,ava_len,GC_content,N50,L50)
    return totall_len,num_contig,max_len,min_len,ava_len,GC_content,N50,L50




#=================================main======================================
import os
import argparse


arg_parse=argparse.ArgumentParser(description='This is a program to statistic informations of genome assembly result.', epilog='Please contact benjaminfang.ol@outlook.com for any problems.')
arg_parse.add_argument('AssemblyFiles',nargs='+', type=str, help='Genome assembly fasta file name')
all_files=arg_parse.parse_args().AssemblyFiles

print('file_name,totall_len,num_contig,Max_len,Min_len,ava_len,GC_content,N50,L50')
for ff in all_files:
    file_dt=Fasta_parse(ff)
    totall_len,num_contig,Max_len,Min_len,ava_len,GC_content,N50,L50=statistic_assembly(file_dt.data)
    print(os.path.basename(ff),totall_len,num_contig,Max_len,Min_len,ava_len,GC_content,N50,L50,sep=',')    







