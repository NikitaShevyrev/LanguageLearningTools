import streamlit as st
from page_supplementaries import (
    get_sidebar,
    get_footer,
    langs_keys,
    langs_keys_no_auto,
    get_watch_and_learn_section,
    get_basic_module
)

from config import config as CFG

source_input_keys = [elem for elem in st.session_state.keys() if elem.startswith('input')]
for source_input_key in source_input_keys:
    if source_input_key in st.session_state.keys():
        st.session_state[source_input_key] = st.session_state[source_input_key]

name = st.session_state["name"] if 'name' in st.session_state.keys() else 'creator'
if f'num_words_to_learn_{name}' in st.session_state.keys():
    st.session_state[f'num_words_to_learn_{name}'] = st.session_state[f'num_words_to_learn_{name}']

translation_keys = [elem for elem in st.session_state.keys() if elem.startswith('translate')]
for translation_key in translation_keys:
    if translation_key in st.session_state.keys():
        st.session_state[translation_key] = st.session_state[translation_key]


get_sidebar()

st.markdown("""
    Howdy!
    
    This is the right place to not only study the language but
    also dive into the depths of foreign culture as well
    as see the beauties sometimes covered even from the eyes
    of the locals.
            
    **What is the workflow?**
    1. Choose the language you want to learn.
    2. Choose a language that is fluent for you.
    3. Go through the row of options below the languages
    and select the one which most appeals to you by the thumbnail
    and description.
    4. Press the YouTube button to start watching.
    5. Watch the video and write down all the unknown words.
    6. Press like to reward the efforts of the channel.
    7. Return to *Watch & Learn* tab and press **Let's shuffle**.
    8. Unfold the *Create group of words* section to see
    the pairs of source-translation language words.
    Are all of your written-down words shown here?
    No panic, if not. Underline underrepresented
    words and visit *Create Own Table* section later.
    For now, let's continue.
    9. Unfold the *Show result* section to see
    ***the Shuffled Table uniquely designed for you***.
    It's highly unlikely that anyone will manage to get the same.
    10. Choose the name for the pairs and the shuffled tables
    and download them by pressing the *Download* buttons.
    11. You're awesome. Now you are ready to learn new
    words and phrases. Visit the *About* section to see how
    to use the generated materials.
    
""")

col_WNL1, col_WNL2 = st.columns(2)

with col_WNL1:
    source_lang_WNL = st.selectbox(
        "Select language to learn",
        options = [key for key in CFG.keys() if key != 'howto'],
        key = f"source_lang_WNL"
    )
    if source_lang_WNL not in langs_keys:
        st.warning("Selected language is not a known one.")

with col_WNL2:
    target_lang_WNL = st.selectbox(
        "Select language to translate to",
        options = langs_keys_no_auto,
        index = langs_keys.index('turkish' if source_lang_WNL != 'turkish' else 'english'),
        key = f"target_lang_WNL"
    )

if len(CFG[source_lang_WNL]['WNL'].keys()) > 0:
    get_watch_and_learn_section(source_lang_WNL, target_lang_WNL)
else:
    st.warning("No materials avialable found")

try:
    if 'current_source_translation_table' not in st.session_state.keys():
        lang1 = st.session_state['lang1']
        lang1_words = st.session_state['lang1_words']
        lang2 = st.session_state['lang2']
        lang2_words = st.session_state['lang2_words']
    
    else:
        lang1 = st.session_state['current_source_translation_table'].columns[0]
        lang1_words = list(st.session_state['current_source_translation_table'].iloc[:,0].values)
        lang2 = st.session_state['current_source_translation_table'].columns[1]
        lang2_words = list(st.session_state['current_source_translation_table'].iloc[:,1].values)
        
    
    name = st.session_state['name']
    if f'num_words_to_learn_{name}' not in st.session_state.keys():
        st.session_state[f'num_words_to_learn_{name}'] = len(lang1_words)


except:
    lang1 = ''
    lang1_words = []
    lang2 = ''
    lang2_words = []
    name = 'creator'
    st.session_state['name'] = name

get_basic_module(lang1, lang1_words, lang2, lang2_words, name)

get_footer()