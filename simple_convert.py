#-*- coding: UTF-8 -*-
import pickle
import os
from custom_setting import *
import difflib
import re
import string
import unicodedata

def remove_noise_simple(src_name):
    # name = src_name.decode('utf-8')
    return unicodedata.normalize('NFKD', src_name).encode('ascii','ignore')

def remove_noise(src):
    # src = src.decode('utf-8')

    pattern = re.compile('è\·ˉ |È\·ˉ |è\·ˉ|È\·ˉ', re.MULTILINE)
    s = pattern.sub('', src)

    pattern = re.compile('@.*|[? ]author.email:.*', re.MULTILINE)
    s = pattern.sub('', s)

    s = s.replace(r'\xi', '')
    s = s.replace(r'\phi', '')
    s = s.replace(r'\delta', '')
    s = s.replace('é', 'e')
    s = s.replace('ó', 'o')

    pattern = re.compile(r'[àáâãäåæ]|(¨¢)+', re.MULTILINE)
    s = pattern.sub('a', s)

    pattern = re.compile(r'[ÀÁÂÃÄÅÆ]', re.MULTILINE)
    s = pattern.sub('A', s)

    pattern = re.compile(r'[èéêëȩ]|¨\||¨¨|¨e|¨¦', re.MULTILINE)
    s = pattern.sub('e', s)

    pattern = re.compile(r'[ÈÉÊË]', re.MULTILINE)
    s = pattern.sub('E', s)

    pattern = re.compile(r' ı', re.MULTILINE)
    s = pattern.sub('i', s)

    pattern = re.compile(r'[ìíîïı]|¨a|¨ª', re.MULTILINE)
    s = pattern.sub('i', s)

    pattern = re.compile(r'[ÌÍÎÏ]', re.MULTILINE)
    s = pattern.sub('I', s)

    pattern = re.compile(r'[ðđ]', re.MULTILINE)
    s = pattern.sub('d', s)

    pattern = re.compile(r'[ÐĐ]', re.MULTILINE)
    s = pattern.sub('D', s)

    pattern = re.compile(r'[ñ]', re.MULTILINE)
    s = pattern.sub('n', s)

    pattern = re.compile(r'[Ñ]', re.MULTILINE)
    s = pattern.sub('N', s)

    pattern = re.compile(r'[òóôõöø]|¨°|¨®|¨o', re.MULTILINE)
    s = pattern.sub('o', s)

    pattern = re.compile(r'[ÒÓÔÕÖØ]', re.MULTILINE)
    s = pattern.sub('O', s)

    pattern = re.compile(r'[ùúûü]|¨²|¨¹|¨u', re.MULTILINE)
    s = pattern.sub('u', s)

    pattern = re.compile(r'[ÙÚÛÜ]', re.MULTILINE)
    s = pattern.sub('U', s)

    pattern = re.compile(r'[Ýýÿ]', re.MULTILINE)
    s = pattern.sub('y', s)

    pattern = re.compile(r'[Ý]', re.MULTILINE)
    s = pattern.sub('Y', s)

    pattern = re.compile(r'[Þþ]', re.MULTILINE)
    s = pattern.sub('p', s)

    pattern = re.compile(r'[çčć]', re.MULTILINE)
    s = pattern.sub('c', s)

    pattern = re.compile(r'[Ç]', re.MULTILINE)
    s = pattern.sub('C', s)

    pattern = re.compile(r'¨f', re.MULTILINE)
    s = pattern.sub('ef', s)

    pattern = re.compile(r'[łŁ]|¨l', re.MULTILINE)
    s = pattern.sub('l', s)

    pattern = re.compile(r'Ł', re.MULTILINE)
    s = pattern.sub('L', s)

    pattern = re.compile(r'ž', re.MULTILINE)
    s = pattern.sub('z', s)

    pattern = re.compile(r'Ž', re.MULTILINE)
    s = pattern.sub('Z', s)

    pattern = re.compile(r'š', re.MULTILINE)
    s = pattern.sub('s', s)

    pattern = re.compile(r'ß', re.MULTILINE)
    s = pattern.sub('b', s)

    pattern = re.compile(r' ¨\.', re.MULTILINE)
    s = pattern.sub('.', s)

    pattern = re.compile(r' º | ¨ |¨ |° |° | ¨ |¨ | ¨| \?ˉ\? |\?ˉ\? |\?ˉ\?|ˉ\? |ˉ\?| ´ |´ | ´| ˝ |˝ | ˘ | ˜ | ˆ | ‰ |‰ | » |» ', re.MULTILINE)
    s = pattern.sub('', s)

    s = s.replace(' ³ ', ' ')

    pattern = re.compile(r"[¯´ˉ’‘ˆ°¨¸³·»~«˘'""\\\\]", re.MULTILINE)
    s = pattern.sub('', s)

    pattern = re.compile(r"[  ]", re.MULTILINE)
    s = pattern.sub(' ', s)

    cleaned = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return cleaned if cleaned.strip() else "[INVALID]"

def generate_new_author_names():
    author_fn = 'data/Author_refined_simple.csv'
    paper_author_fn = 'data/PaperAuthor_refined_simple.csv'

    # Generate Author_refined_simple.csv
    if not os.path.isfile(author_fn):
        print("Generating Author_refined_simple.csv")
        done = {}
        with open("data/Author.csv", "r", encoding="utf-8") as author_file, \
             open(author_fn, 'w', encoding="utf-8") as f:
            for line in author_file:
                tokens = line.strip().split(',')
                if len(tokens) > 1:
                    if tokens[1] in done:
                        tokens[1] = done[tokens[1]]
                    else:
                        clean = remove_noise(tokens[1])
                        done[tokens[1]] = clean
                        tokens[1] = clean
                    f.write(','.join(tokens) + '\n')
                else:
                    f.write(line)

    # Generate PaperAuthor_refined_simple.csv
    if not os.path.isfile(paper_author_fn):
        print("Generating PaperAuthor_refined_simple.csv")
        done = {}
        with open("data/PaperAuthor.csv", "r", encoding="utf-8") as pa_file, open(paper_author_fn, 'w', encoding="utf-8") as f:
            for line in pa_file:
                tokens = line.strip().split(',')
                if len(tokens) > 2:
                    if tokens[2] in done:
                        tokens[2] = done[tokens[2]]
                    else:
                        clean = remove_noise(tokens[2])
                        done[tokens[2]] = clean
                        tokens[2] = clean
                    f.write(','.join(tokens) + '\n')
                else:
                    f.write(line)

generate_new_author_names()
