import streamlit as st
from page_supplementaries import get_sidebar, get_footer

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table

import io

from deep_translator import GoogleTranslator

st.title("Shuffled table tool")

# >>>> Add words

with st.expander("Create group of words"):

    num_words_to_learn = st.number_input("Select number of words to learn", min_value = 0, step = 1)

    col0a, col0b, col0c, col0d = st.columns([0.1, 0.37, 0.11, 0.42])

    col1a, col1b = st.columns(2)

    langs_dict = GoogleTranslator().get_supported_languages(as_dict = True)
    langs_dict['auto'] = 'auto'
    langs_keys = list(langs_dict.keys())
    
    with col0b:
        st.subheader("Want-To-Learn Words")
    
    with col0c:
        swap_button = st.button(":left_right_arrow:")
        if swap_button:
            st.session_state['language_1'], st.session_state['language_2'] = st.session_state['language_2'], st.session_state['language_1']
            st.session_state['source_words'] = st.session_state['translation']
    
    with col0d:
        st.subheader("Mother Tongue Translation")

    with col1a:
        try:
            lang1 = st.session_state['language_1']
        except:
            lang1 = 'auto'
            st.session_state['language_1'] = lang1
        source_lang = st.selectbox("Select language to translate from", options = langs_keys, index = langs_keys.index(lang1))
        if source_lang != lang1:
            st.session_state['language_1'] = source_lang
    
    with col1b:
        try:
            lang2 = st.session_state['language_2']
        except:
            lang2 = 'english'
            st.session_state['language_2'] = lang2
        
        target_lang = st.selectbox("Select language to translate to", options = langs_keys, index = langs_keys.index(lang2))
        if target_lang != lang2:
            st.session_state['language_2'] = target_lang

    col2a, col2b = st.columns(2)

    with col2a:
        try:
            source_words_num = len(st.session_state['source_words'])
            if source_words_num >= num_words_to_learn:
                source_values = st.session_state['source_words']
            else:
                source_values = st.session_state['source_words'] + ['word' for _ in range(num_words_to_learn-source_words_num)]
        except:
            source_values = ['word' for _ in range(num_words_to_learn)]
        
        source_words = [
            st.text_input("Write a word to learn", source_values[i], key=f"input{i}") for i in range(num_words_to_learn)
        ]
        st.session_state['source_words'] = source_words
    
    with col2b:
        offer_translation = [
            GoogleTranslator(source = langs_dict[source_lang], target = langs_dict[target_lang]).translate(elem)
            for elem in source_words
        ]

        translation = [
            st.text_input("Translation [change if wrong]", value = offer_translation[i], key = f"translate{i}")
            for i in range(num_words_to_learn)
        ]
        st.session_state['translation'] = translation

# >>>> main
if num_words_to_learn > 0:

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

    with st.expander("Show result"):
        st.markdown(translation_words_DF.style.hide(axis='index').hide(axis='columns').to_html(), unsafe_allow_html=True)

    st.markdown("---")

    result_filename = st.text_input("Select filename", "my_shuffled_table")
    if not result_filename.endswith(".png"):
        result_filename += ".png"

    translation_words_DF.columns = [''] * Columns_num
    translation_words_DF.index = [''] * Rows_num

    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, translation_words_DF, loc='center')  # where df is your data frame

    file_like = io.BytesIO()
    plt.savefig(file_like, bbox_inches='tight', dpi=200)
    file_like.seek(0)

    btn = st.download_button(
        label="Download table", # image
        data=file_like,
        file_name=result_filename,
        mime="image/png"
    )

    # >>>>


get_footer()
get_sidebar()