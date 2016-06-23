# parseGenbanksExtractCDSsByGeneName
Takes a list of CDS gene names (whitespace separated) and extracts the DNA sequences from a list of genbank files (can do *.gbk files) and outputs a DNA multi-fasta file for each CDS name.  Useful for, for example, extracting the fasta DNA sequences from multiple prokka-annotated genbanks for a list of core genes as detected by Roary. Output is one unaligned fasta file per locus – use something like [MACSE](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0022594) to perform codon-aware alignment.

## Example usage:

```bash
python parseGenbanksExtractCDSsByGeneName.py -h
usage: parseGenbanksExtractCDSsByGeneName.py [-h]
                                             [-c CDS_NAMES [CDS_NAMES ...]] -g
                                             GENBANK_FILES [GENBANK_FILES ...]

Get CDS DNA seq(s) from genbanks

optional arguments:
  -h, --help            show this help message and exit
  -c CDS_NAMES [CDS_NAMES ...], --CDS_names CDS_NAMES [CDS_NAMES ...]
                        Names of CDSs, separated by whitespace.
  -g GENBANK_FILES [GENBANK_FILES ...], --genbank_files GENBANK_FILES [GENBANK_FILES ...]
                        Input genbanks sequence(s), separated by whitespace or
                        use a wildcard '*'
```

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


