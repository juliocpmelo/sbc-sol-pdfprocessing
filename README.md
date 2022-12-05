# sbc-sol-pdfprocessing

The [SOL platform](https://sol.sbc.org.br/) is an open online library/publisher that is supported by the Brazilian Computing Society. To post a publication there, the SBC offers two ways, one is for them to process the metadata of the files for a extra charge, the other is for the conference chairs process the metadata and send them the files containing such info.

In the second scenario, there are 4 files to be filled: Artigos, Autores, Referencias and Secoes. These files are excel sheets, three of them (Artigos, Autores and Referencias) need to be filled with data of the conference's papers, while the last one (Secoes) is sent by the Sol staff with information on the previous publications to be updated.

To fill the Artigos, Autores and Referencias files the publication chair needs to go over all pdf papers and extract the desired info. On bigger conferences this job is very error prone since opening/copy/paste/closing every file could lead to errors. To help solving this issue I wrote a set of scripts to help to process the pdf files and generate .txt croped versions with the key info needed to fill the metadata files.

# Input

The pdf files of a specific track should should be in a folder together with the autores text file.

The autores text file is a auxiliar file used to generate the autores_final that contains the author metadata. This file is organized as follows:

Paper index: The index of the paper this author appears on. This number is extracted while filling initial data on the Artigos.xlsx file. I is an integer that identifies the paper.
Author names: A list of author names with their affiliation within parenthesis, separated by ';'.

The paper index and Author name information is separated by a tab ('\t'). Ex:

65	Julio Melo (UFRN - Brazil);Julio Cesar Paulino (UFRN - Brazil)

To generate this auxiliar file I used available information on the conference publication platform, that provides me the paper title and the author with affiliation list. Copy pasting this information on a google sheet to generate the index and processing on the sheet to generate this format. Here I avoided using comma(',') to separate the authors because some affiliation have comma on their names.

# Usage and Output

pip install install.txt
python .\processfiles.py .\data\demo

Inside the demo folder 3 files will be generated containing the abstract.txt, resumo.txt, refs.txt, autores_final.txt. Containing the references, resumo and palavras-chave(pt-br), abstract and keywords the autores_final file contains the author meta-data.
