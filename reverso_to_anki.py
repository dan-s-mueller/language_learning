# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:52:01 2022

@author: dan.mueller
"""

import numpy
from reverso_api import ReversoContextAPI
import csv

def anki_term_output(source_term, source_lang, target_lang, printout):
    """'Takes an input term, generates most frequent usage as output, top 3 target uses.

    Args:
        source_term: term to process
        source_lang: source language
        target_lang: target language

    Returns:
        The highlighted word usage example

    """
    # Get the term to look up
    # api = ReversoContextAPI('schonend','','de','en')
    api = ReversoContextAPI(source_term,'',source_lang,target_lang)
    
    # Findt the most frequently used translation and save it
    arr_source_word=[]
    arr_translation=[]
    arr_frequency=[]
    arr_part_of_speech=[]
    definition=[]
    if printout:
        print()
        print("Translation (top by frequency):")
    for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
        if printout:
            print(source_word, "==", translation)
            print("Frequency (how many word usage examples contain this word):", frequency)
            print("Part of speech:", part_of_speech if part_of_speech else "unknown")
            print()
        arr_source_word.append(source_word)
        arr_translation.append(translation)
        arr_frequency.append(frequency)
        arr_part_of_speech.append(part_of_speech)
    
    # Choose the top 3 most frequent definitions and pass those along.
    if len(arr_frequency)>=3:
        i_frequent=numpy.argsort(arr_frequency).tolist()[-3:]
    else:
        i_frequent =numpy.argsort(arr_frequency).tolist()
    definition.append([arr_source_word[i] for i in i_frequent])
    definition.append([arr_translation[i] for i in i_frequent])
    definition.append([arr_frequency[i] for i in i_frequent])
    definition.append([arr_part_of_speech[i] for i in i_frequent])
    
    # Find the first three context examples and output them
    i_examples=0
    arr_source=[]
    arr_target=[]
    if printout:
        print()
        print("Word Usage Examples:")
    for source, target in api.get_examples():
        i_examples=i_examples+1
        arr_source.append(source.text)
        arr_target.append(target.text)
        if printout:
            print(source.text, "==", target.text)
        if i_examples==3:
            break
    context=[list(a) for a in zip(arr_source,arr_target)]
    return definition, context

path=r'C:/Users/dan.mueller/Downloads/'
file_name='anki_transfer.csv'
printout=True
lines_out=[]
# opening the CSV file
with open(path+file_name, mode ='r',encoding='UTF-8') as file:
    csvFile = csv.reader(file)
    # for lines in csvFile:
    # 		print(lines)
    for lines in csvFile:
        source_term=lines[0]
        target_term=lines[1]
        tag=lines[2]
        if ('Der ' in source_term[:4]) or ('Die ' in source_term[:4]) or ('Das ' in source_term[:4]):
            definition,context=anki_term_output(source_term[4:],"de","en",printout)
        else:
            definition,context=anki_term_output(source_term,"de","en",printout)
        # Output is: source_term, target_term, tag, output_target_term, output_source_context, output_target_context
        lines_out.append([source_term,target_term,tag,', '.join(definition[1]),context[0][0],context[0][1]])

# write the output to a new file
with open(path+file_name[:-4]+'_out.csv', mode ='w', newline='', encoding='UTF-8') as file:
    writer=csv.writer(file)
    for line in lines_out:
        writer.writerow(line)