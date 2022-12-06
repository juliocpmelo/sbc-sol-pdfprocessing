from glob import glob
import os
from symbol import arglist
import sys
from PyPDF2 import PdfReader, PdfMerger

#encontra um texto que inicia com alguma palavra da start_list e termina com alguma da end_list
#se end_list for None, pressupõe que é até o fim do arquivo
def findWithStartEnd(text, start_list, end_list):
    start = -1
    for r in start_list :
        p = text.find(r)
        if p != -1 :
            start = p
            break
    
    if end_list is not None :
        end = -1
        for r in end_list :
            p = text.find(r)
            if p != -1 :
                end = p
                break
        if start == -1 :
            return {'start': None, 'end': None, 'text': None}
        elif end == -1 or start > end:
            return {'start': start, 'end': None, 'text': None}
        else :
            return {'start': start, 'end': end, 'text': text[start:end]}
    
    if start == -1 :
        return {'start': None, 'text': None}
    return {'start': start, 'text': text[start:]}

def removeIfExists(file):
    try:
        os.remove(file)
    except:
        print('file ' + file + ' not found')

def processReferences(files, dest_file):
    removeIfExists(dest_file)
        
    for f in files:
        reader = PdfReader(f)
        text = reader.pages[-3].extract_text()
        text = text + '\n' + reader.pages[-2].extract_text()
        text = text + '\n' + reader.pages[-1].extract_text()
        

        ref_list = [
            'Referências',
            'References',
            'Refer ˆencias',
            'Refer ência',
            'Ref erências',
            'Refer ências',
            'Referencias'
        ]
        res = findWithStartEnd(text, ref_list, None)
        file_number = os.path.basename(f)[:-4]
        refs = ''
        if res['start'] is None :
            refs = 'no refs' + '\n'
        else :
            refs_vec = text[res['start']:].split('\n')
            #print('{} - {}', os.path.basename(f)[:-4], len(refs_vec))
            if len(refs_vec) == 1: #apenas uma linha para todas as referencias o.O?
                refs_vec = text[res['start']:].split('.') #split por . é melhor do que nada
                refs_vec = ['{}.'.format(item) for item in refs_vec]
            else:
                refs_vec = refs_vec[1:] #a primeira linha é sempre "Referencias"
            for line in refs_vec:
                if line.strip() != '' and line.strip() != '.':
                    refs = refs + line.strip() + '\n'
        if file_number == '125':
            print(reader.pages[-3].extract_text())
            print(reader.pages[-2].extract_text())
            print(reader.pages[-1].extract_text())
        with open(dest_file, encoding="utf8", errors="surrogateescape", mode='a') as dest:
            refs_v=refs.split('\n')
            for l in refs_v:
                if l.strip() != '' :
                    dest.write('{}\t{}\n'.format(file_number,l))

def concatAll(files, dest_file):
    removeIfExists(dest_file)

    def sortByNameNumber(file):
        pos1 = file.find('\\')
        pos2 = file.index(".pdf")
        return int(file[pos1+1:pos2])
    files.sort(key=sortByNameNumber)
    
    merger = PdfMerger()

    for pdf in files:
        print('appending ' + pdf)
        merger.append(pdf)

    merger.write(dest_file)
    merger.close()


    

def getAbstractAndKeyWords(text, abstract_start, abstract_end, keywords_end):
    start_list = abstract_start
    end_list = abstract_end
    
    res = findWithStartEnd(text, start_list, end_list)
    abstract = ''
    if res['start'] is None :
        abstract = 'no abstract'
    elif res['end'] is None :
        abstract = 'no end-abstract'
    else :
        abstract = res['text'] if res['text'] is not None else 'no abstract'

    #keywords search
    keywords = ''
    if res['start'] is not None :
        text = text[res['start']:] #cuts text from keywords:...
        start_list = end_list
        end_list = keywords_end
        res = findWithStartEnd(text, start_list, end_list)
        if res['start'] is None :
            keywords = 'no key-words'
        elif res['end'] is None :
            keywords = '200-chars keywords\n'
            keywords = keywords + text[res['start']:res['start']+200]
        else :
            keywords = res['text'] if res['text'] is not None else 'no key-words'
    else :
        keywords = res['text'] if res['text'] is not None else 'no key-words'
    
    return abstract.strip(), keywords.strip()
            

def processAbstractKeywords(files, dest_file):
    removeIfExists(dest_file)        
    for f in files:
        reader = PdfReader(f)
        
        text = reader.pages[0].extract_text()
        text = text + '\n' + reader.pages[1].extract_text()
    
        start_list = [
            'Abstract',
        ]
        #abstract ends when keyword starts
        end_list = [
            'Keywords',
            'Keywor ds',
            'Keyword s',
            'Index terms',
            'Index Terms'
        ]
        #keywords ends with 1. or Resumo start
        keywords_end_list = [
            'Resumo',
            'I. Introduction',
            'I. I NT',
            '1.'
        ]
        abstract, keywords = getAbstractAndKeyWords(text, start_list, end_list, keywords_end_list)
        
        file_number = os.path.basename(f)[:-4]
        if file_number == '33':
            print(reader.pages[0].extract_text())
            print(reader.pages[1].extract_text())
        
        with open(dest_file, encoding="utf8", errors="surrogateescape", mode='a') as dest:
            dest.write('{} - {}\n'.format(file_number, reader.numPages))
            dest.write('{}\n'.format(abstract))
            dest.write('{}\n'.format(keywords))

def processResumoPalavraschave(files, dest_file):
    removeIfExists(dest_file)        
    for f in files:
        reader = PdfReader(f)
        
        text = reader.pages[0].extract_text()
        text = text + '\n' + reader.pages[1].extract_text()
    
        start_list = [
            'Resumo'
        ]
        #resumo ends when palavras chave starts
        end_list = [
            'Palavr',
            'Plavr',
            'Palav'
        ]
        #keywords ends with 1. or Resumo start
        keywords_end_list = [
            'Abstract',
            '1.',
            'Intro'
        ]
        abstract, keywords = getAbstractAndKeyWords(text, start_list, end_list, keywords_end_list)
        
        file_number = os.path.basename(f)[:-4]
        if file_number == '41':
            print(reader.pages[0].extract_text())
            print(reader.pages[1].extract_text())
            
        with open(dest_file, encoding="utf8", errors="surrogateescape", mode='a') as dest:
            dest.write('{} - {}\n'.format(file_number, reader.numPages))
            dest.write('{}\n'.format(abstract))
            dest.write('{}\n'.format(keywords))

def processAutores(autores_file, dest_file):
    removeIfExists(dest_file)
    authors_result = []
    with open(autores_file, mode='r', encoding="utf8",) as f:
        for line in f.readlines():
            start = line.find('\t')
            article_idx = line[:start]
            authors_txt = line[start+1:]
            authors = authors_txt.split(';')
            #print (line)
            for author in authors :
                #print(author)
                affiliation_start = author.find('(')
                affiliation_end = author.rfind(')')
                country_start = author.rfind('-')
                
                names = author[:affiliation_start].strip().split(' ')
                #print(names)
                first_name = names[0]
                last_name = names[-1]
                
                country = author[country_start+1:affiliation_end]
                affiliation = author[affiliation_start+1:country_start]
                
                authors_result.append({'article_idx':article_idx, 'first_name':first_name, 'last_name':last_name, 'affiliation': affiliation, 'country':country})

    #sort
    def sortByIdx(author):
        return int(author['article_idx'])
    authors_result.sort(key=sortByIdx)
    with open(dest_file, encoding="utf8", mode='w') as dest:
        for r in authors_result:
            #print('{}\t{}\t{}\t{}\t{}\t{}\n'.format(article_idx, first_name, last_name, affiliation, affiliation, country))
            dest.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(r['article_idx'], r['first_name'], r['last_name'], r['affiliation'], r['affiliation'], r['country']))

def main():
    
    directory = sys.argv[1]
    if not directory :
        print('must have a directory')
        exit(-1)
    files = []
    for root, dirs, files_ in os.walk(directory):
        for filename in files_:
            if filename.find(".pdf") >= 0 :
                fileFull = str(os.path.join(root, filename))
                files.append(fileFull)
    
    
    #sort
    def sortByNameNumber(file):
        pos1 = file.rfind(os.path.sep)
        pos2 = file.index(".pdf")
        return int(file[pos1+1:pos2])
    files.sort(key=sortByNameNumber)
    
    #rename
    #for f in files:
    #    f_number = int(os.path.basename(f)[:-4])
    #    f_number = f_number - 20
    #    os.rename(f, os.path.join(directory,'{}.pdf'.format(f_number)))
    
    processReferences(files, os.path.join(directory,'refs.txt'))
    processAbstractKeywords(files, os.path.join(directory,'abstract.txt'))
    processResumoPalavraschave(files, os.path.join(directory,'resumo.txt'))
    processAutores(os.path.join(directory,'autores'), os.path.join(directory,'autores_final'))
    #autores
    
        
    
                    
                
    #concatAll(files)
    
    '''
    authors = []
    author_idxs = []
    with open('data/computing/titles_authors_pages.txt', 'r') as f:
        lines = f.readlines()
        
        
        for line in lines:
            line = line.rstrip()
            
            pageNumber = re.search('\{\d+\}', line).group()
            pageNumber = pageNumber[1:]
            pageNumber = pageNumber[:-1]
            print('page number ' + str(pageNumber))
            idx1 = line.rfind('{')
            idx2 = line.rfind('}')
            
            print('authors = ' + line[idx1+1:idx2])
            authors_ = line[idx1+1:idx2].split(',')
            authors_ = [author.strip() for author in authors_]
            for author in authors_:
                if authors.count(author) == 0 :
                    authors.append(author)
                    author_idxs.append([int(pageNumber)])
                else:
                    idx = authors.index(author)
                    author_idxs[idx].append(int(pageNumber))
        author_sorted = sorted(authors)
        print('authors')
    with open('data/computing/program_out.txt', 'w') as f:
        for author in author_sorted:
            idx = authors.index(author)
            f.write('\\contentsline {{section}}{{{}}}{{{}}}{{}}\n'.format(author,','.join(str(e) for e in author_idxs[idx])))
            
            
            
    '''
    
                
    
    
main()