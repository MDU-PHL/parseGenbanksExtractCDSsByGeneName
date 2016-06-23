#!/usr/bin/env python

'''
20160623_2130
github schultzm
dr.mark.schultz@gmail.com

Extract CDS DNA sequences from gbk files using the CDS gene name.

Example usage (in series):
    python parseGenbanksExtractCDSsByGeneName.py -g *.gbk -c accA accB_2 accD

Example usage (in parallel):
    Save your gene list to txt file, one gene name per line in file, then use:
    nice parallel -j 36 python parseGenbanksExtractCDSsByGeneName.py \
    -g *.gbk -c {} :::: core_genes_list.txt

'''

import argparse
import os
from Bio.Alphabet import generic_dna
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#set up the arguments parser to deal with the command line input
PARSER = argparse.ArgumentParser(description='Get CDS DNA seq(s) from genbanks')
PARSER.add_argument('-c', '--CDS_names', help='Names of CDSs, separated by \
                    whitespace. ', nargs='+',
                    required=False)
PARSER.add_argument('-g', '--genbank_files', 
                    help='Input genbanks sequence(s), separated by \
                    whitespace or use a wildcard \'*\'', nargs='+', 
                    required=True)
ARGS = PARSER.parse_args()

def getDNAseq(cds_name, gbk):
    '''
    Reads in the requested CDS name, searches for the CDS in the genbank file, 
    returns the DNA sequence, with isolate name and product name in the 
    sequence description.
    '''
    basename = os.path.splitext(os.path.basename(gbk))[0]
    n_hits = 0
    for gb_record in SeqIO.parse(open(gbk,'r'), 'genbank'):
        for index, feature in enumerate(gb_record.features):
            if feature.type == 'CDS':
                gb_feature = gb_record.features[index]
                if 'gene' in gb_feature.qualifiers:
                    if cds_name == gb_feature.qualifiers['gene'][0]:
                        product = gb_feature.qualifiers['product']
                        DNAseq = gb_feature.extract(gb_record.seq)
                        record_new = SeqRecord(Seq(str(DNAseq), generic_dna), \
                                     id=basename, name=cds_name, \
                                     description=product[0])
                        return record_new
                        n_hits += 1
    #Tell the user if copy number of the CDS is greater than single-copy
    if n_hits > 1:
        print 'Warning, '+n_hits+' found in '+gbk+' for '+cds_name+'.'

def writeFasta(seqs, cds_name):
    '''
    Takes the list of sequences stored in seqs and writes them to file.
    '''
    outname = cds_name+'.fasta'
    with open(outname, 'w') as output_handle:
        for i in seqs:
            SeqIO.write(i, output_handle, 'fasta')
        print 'Written sequences to '+outname+'.'

#For every locus, check each genbank file and return the locus.
#Write the locus to file.
for i in ARGS.CDS_names:
    SEQS = []
    print '\nProcessing '+i+' in:'
    for j in ARGS.genbank_files:
        print j
        seq = getDNAseq(i, j)
        SEQS.append(seq)
    #use filter on SEQS to get rid of 'None' objects in list
    writeFasta(filter(None, SEQS), i)
