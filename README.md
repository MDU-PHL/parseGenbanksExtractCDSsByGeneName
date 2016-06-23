# parseGenbanksExtractCDSsByGeneName
Takes a list of CDS gene names (whitespace separated) and extracts the genes from a list of genbank files (can do *.gbk files) and outputs a multi-fasta file for each CDS name.  Useful for, for example, extracting the fasta sequences from multiple genbanks for a list of core genes as detected by Roary. Output is one unaligned fasta file per locus.  Use something like [MACSE](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0022594) to perform codon-aware alignment prior to phylogenetic analysis.

## Example usage:
### In series:
    
```bash
python parseGenbanksExtractCDSsByGeneName.py -g *.gbk -c accA accB_2 accD
```

### In parallel:
    Save your gene list to txt file, one gene name per line in file, then use:

```bash
nice parallel -j 72 python parseGenbanksExtractCDSsByGeneName.py \
-g *.gbk -c {} :::: core_genes_list.txt
```

### Output files:
The output files (*.fasta) contain one fasta entry per hit.  To count the number of fasta entries per files, do:
```bash
arr=(*.fasta)
for i in ${arr[@]}; do echo $i; grep \> $i | wc -l; done
```


