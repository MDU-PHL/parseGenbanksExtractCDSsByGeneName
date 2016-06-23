# parseGenbanksExtractCDSsByGeneName.py
Takes a list of CDS gene names (whitespace separated) and extracts the genes from a list of genbank files (can do *.gbk files) and outputs a multi-fasta file for each CDS name.

## Example usage:
### In series:
    ```
    python parseGenbanksExtractCDSsByGeneName.py -g *.gbk -c accA accB_2 accD
    ```
### In parallel:
    Save your gene list to txt file, one gene name per line in file, then use:
    ```
    nice parallel -j 72 python parseGenbanksExtractCDSsByGeneName.py \
    -g *.gbk -c {} :::: core_genes_list.txt
    ```

