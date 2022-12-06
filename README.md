# sbc-sol-pdfprocessing

The [SOL platform](https://sol.sbc.org.br/) is an open online library/publisher that is supported by the Brazilian Computing Society. To post a publication there, the SBC offers two ways, one is for them to process the metadata of the files for a extra charge, the other is for the conference chairs process the metadata and send them the files containing such info.

In the second scenario, there are 4 files to be filled: Artigos, Autores, Referencias and Secoes. These files are excel sheets, three of them (Artigos, Autores and Referencias) need to be filled with data of the conference's papers, while the last one (Secoes) is sent by the Sol staff with information on the previous publications to be updated.

To fill the Artigos, Autores and Referencias files the publication chair needs to go over all pdf papers and extract the desired info. On bigger conferences this job is very error prone since opening/copy/paste/closing every file could lead to errors. To help solving this issue I wrote a set of scripts to help to process the pdf files and generate .txt croped versions with the key info needed to fill the metadata files.

# Input

The pdf files of a specific track should should be in a folder together with the __autores__ text file. The pdf files should be in the format "1.pdf", "2.pdf", ..., where the number is an integer. We
use this format to help in the proceedings organization, the file number is used to generate the __refs__, __abstract__ and __resmumo__ files.

The __autores__ text file is a auxiliar file used to generate the autores_final that contains the author metadata. This file is organized as follows:

Paper index: The index of the paper this author appears on. This number is extracted while filling initial data on the Artigos.xlsx file. I is an integer that identifies the paper.
Author names: A list of author names with their affiliation within parenthesis, separated by ';'.

The paper index and Author name information is separated by a tab ('\t'). Ex:

65	Julio Melo (UFRN - Brazil);Julio Cesar Paulino (UFRN - Brazil)

To generate this auxiliar file I used available information on the conference publication platform, that provides me the paper title and the author with affiliation list. Copy pasting this information on a google sheet to generate the index and processing on the sheet to generate this format. Here I avoided using comma(',') to separate the authors because some affiliation have comma on their names.

# Usage and Output

```
pip install -r requirements.txt
python ./processfiles.py ./demo
```

After the execution, 4 files will be generated inside the _demo_ folder: abstract.txt, resumo.txt, refs.txt and autores_final.txt. 

The __refs.txt__ file contains the references, in the format <file_idx> <ref_line>, this format is used because the pdf files break the references in many lines, one have to join them accordingly. To
do so I use a procces in google sheets (just joins the selected lines on the first one with ' ', then deletes all selected lines except the first).

The __abstract.txt__ contains the abstract if it can be found. The abstract is the text between the word "Abstract" and the begining of the the "Keywords". This file contains text within these marks,
if they can be found. This file also contains the keyworsd if they can be found. The file is organized as:

```
<file_idx> - <file_num_pages>\n<file_abstract>\n<file_keywords>
```
Ex:
```
1 - 4
Abstract. This meta-paper describes the style to be used in articles and
short papers for SBC conferences. For papers in English, you should add
just an abstract while for the papers in Portuguese, we also ask for an
abstract in Portuguese (“resumo”). In both cases, abstracts should not
have more than 10 lines and must be in the first page of the paper. Af-
ter the abstract authors should also include the keywords in English.
Keywords— one, two, three, four
```

The __resumo.txt__ contains the "resumo(pt-br)" and "palavras chave(pt-br)", in the same format as the abstract.txt.

# Work in progress

As you can see there are tons of improvement to be made, not only because of the latin letters and accents, but in the text processing in overall. Even with those
issues, I used these scripts to build the proceedings of the XXI Brazilian Conference on Games and Digital Entertainment (SBGames 2022), which was a lot of work still.
