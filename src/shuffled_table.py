import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from pandas.plotting import table
from typing import List

def get_shuffled_table(source_words: List[str], translation: List[str]) -> pd.DataFrame:

    target_lang_words = np.array(source_words)
    translation_words = np.array(translation)

    Words_num = target_lang_words.size
    Rows_num = Words_num * 2
    Columns_num = 5
    Eng_word_per_column = 1
    numbers_num_per_table = 1
    numbers_digits_num = 7

    # Generate random num sequence
    num_sequence = np.tile(np.arange(Words_num), 2)

    table_mask = np.zeros((Rows_num, Columns_num), dtype=int)
    table_mask[:,0] = num_sequence
    for i in range(1,Columns_num):
        table_mask[:,i] = np.random.permutation(num_sequence)

    # use given words to fill the mask
    target_lang_words_table = target_lang_words[table_mask]

    translation_words_table = translation_words[table_mask]

    # change given number of word into its target language form
    condn_mask = np.full((Rows_num, Columns_num), False, dtype=bool)
    condn_mask[:Eng_word_per_column,:] = True
    for i in range(Columns_num):
        condn_mask[:,i] = np.random.permutation(condn_mask[:,i])

    translation_words_table = np.where(condn_mask, target_lang_words_table, translation_words_table)

    # replace random words (non target lang) in the table with numbers
    counter = 0
    while numbers_num_per_table > counter:
        x = np.random.randint(Rows_num)
        y = np.random.randint(Columns_num)
        if condn_mask[x,y] == True:
            pass
        else:
            translation_words_table[x,y] = np.random.randint((10 ** numbers_digits_num-1))
            counter += 1

    translation_words_DF = pd.DataFrame(translation_words_table)

    return translation_words_DF

def get_filelike_table(translation_words_DF: pd.DataFrame):
    
    translation_words_DF.columns = [''] * translation_words_DF.shape[1]
    translation_words_DF.index = [''] * translation_words_DF.shape[0]

    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, translation_words_DF, loc='center')  # where df is your data frame

    file_like = io.BytesIO()
    plt.savefig(file_like, bbox_inches='tight', dpi=200)
    file_like.seek(0)

    return file_like
