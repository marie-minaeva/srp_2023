from Bio import SeqIO, Seq
import argparse
import numpy as np
from collections import defaultdict
from itertools import chain, combinations
from os.path import exists

def parse_msa(file):
    """
    Parses MSA hhblist outputs (initial .a3m was converted to .fas (FASTA) format beforehand) to ungap the MSA with
    respect to the query  sequence
    Parameters
    ----------
    wd : str
        Path to the working directory

    Returns
    ----------
    Resulting MSA is stored in a file ./wd/wd.fasta

    Files
    ----------
    ./wd/try-hhlist.fas :
        Input MSA
    ./wd/wd.fasta :
        Output MSA
    """
    seqs = defaultdict(str)
    query = False
    # Reading the MSA file
    for seq_record in SeqIO.parse(file, "fasta"):
        seqs[seq_record.name] = seq_record.seq
        if not query:
            query = seq_record.name
    # Getting gaps positions in the query sequence to be deleted
    pos = [i for i in range(len(seqs[query])) if seqs[query].startswith('-', i)]
    pos = pos[::-1]
    # Deleting positions
    for key, value in seqs.items():
        temp = value
        for p in pos:
            temp = value[:p] + temp[p + 1:]
        #temp = temp.replace("-", ".")
        seqs[key] = temp	
    # Writing resulting MSA to file
    with open(file.removesuffix(".fas") + "ali.fasta", "w") as output_handle:
        for i in seqs.items():
            writer = SeqIO.FastaIO.FastaWriter(output_handle, wrap=50)
            writer.write_record(SeqIO.SeqRecord(Seq.Seq(i[1]), id=i[0], name=i[0], description=""))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', 
                        help='Path to file.')
    args = parser.parse_args()
    parse_msa(args.file)
