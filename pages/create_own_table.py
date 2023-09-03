import streamlit as st
from page_supplementaries import (
    get_sidebar, get_footer, get_data_button, get_basic_module
)

get_sidebar()

st.markdown("""
    Howdy!
    
    So, you are here. You have the words of phrases to learn.
    You are full of desire to learn them and this is the right
    place to do it by creating the Shuffled Table.            
            
    **What is the workflow?**
    1. Unfold the *Create group of words* section and 
    choose the language you want to learn.
    2. Choose a language that is fluent for you.
    3. Now select the number of words/phrases to learn.
    In general, it is recommended to set it around 10 to keep
    the Shuffled Table readable and doable when exercising.
    4. After choosing the number below you'll find the gaps
    to insert the words/phrases that you want to practice with.
    - The right column will automatically offer the translation
    for the chosen language. In case it is incorrect,
    you can change it.
    - Press the double-sided arrow to swap languages, if needed
    5. Unfold the *Create group of words* section to see
    the pairs of source-translation language words.
    6. Unfold the *Show result* section to see
    ***the Shuffled Table uniquely designed for you***.
    It's highly unlikely that anyone will manage to get the same.
    7. Choose the name for the pairs and the shuffled tables
    and download them by pressing the *Download* buttons.
    8. You're awesome. Now you are ready to learn new
    words and phrases. Visit the *About* section to see how
    to use the generated materials.
    
""")

get_data_button('', [], '', [], 'creator', "Create Own Table")

try:
    lang1 = st.session_state['lang1']
    lang1_words = st.session_state['lang1_words']
    lang2 = st.session_state['lang2']
    lang2_words = st.session_state['lang2_words']
    name = st.session_state['name']
except:
    lang1 = ''
    lang1_words = []
    lang2 = ''
    lang2_words = []
    name = 'creator'

get_basic_module(lang1, lang1_words, lang2, lang2_words, name)

get_footer()
