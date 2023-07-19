import streamlit as st
from page_supplementaries import (
    get_sidebar,
    get_footer,
    langs_keys,
    langs_keys_no_auto,
    get_simple_section,
    get_basic_module
)
from config import config as CFG

get_sidebar()

st.markdown("""
    Howdy!
    
    Here you can find exercises to study parts of speech.
            
    **What is the workflow?**
    1. Choose the language you want to learn.
    2. Choose a language that is fluent for you.
    3. Choose the desired level of proficiency for studying
    language and a grammar unit.
    4. Select an exercise from the row of uploaded excercises.
    5. Press **Let's shuffle** to prepare data for
    the Shuffled Table generation.
    6. Unfold the *Create group of words* section to see
    the pairs of source-translation language words.
    7. Unfold the *Show result* section to see
    ***the Shuffled Table uniquely designed for you***.
    It's highly unlikely that anyone will manage to get the same.
    8. Choose the name for the pairs and the shuffled tables
    and download them by pressing the *Download* buttons.
    9. You're awesome. Now you are ready to learn new
    words and phrases. Visit the *About* section to see how
    to use the generated materials.
    
""")

col_speech1, col_speech2 = st.columns(2)

with col_speech1:
    source_lang_speech = st.selectbox(
        "Select language to learn",
        options = [key for key in CFG.keys() if key != 'howto'],
        key = f"source_lang_speech"
    )
    if source_lang_speech not in langs_keys:
        st.warning("Selected language is not a known one.")

with col_speech2:
    target_lang_options_speech = list(langs_keys_no_auto)
    target_lang_options_speech.remove(source_lang_speech)
    target_lang_speech = st.selectbox(
        "Select language to translate to",
        options = target_lang_options_speech,
        key = f"target_lang_speech"
    )

try:
    speech_levels = list(CFG[source_lang_speech]['speech'].keys())
    # speech_levels = ['Any'] + speech_levels
except:
    speech_levels = ['empty']

col_speech3, col_speech4 = st.columns(2)

with col_speech3:
    speech_level = st.selectbox(
        "Select proficiency level",
        options = speech_levels,
        key = f"level_speech"
    )

try:
    speech_units = list(CFG[source_lang_speech]['speech'][speech_level].keys())
    # speech_units = ['Any'] + speech_units
except:
    speech_units = ['empty']

with col_speech4:
    speech_unit = st.selectbox(
        "Select proficiency level",
        options = speech_units,
        key = f"unit_speech"
    )

if speech_units[0] != 'empty':
    get_simple_section(source_lang_speech, target_lang_speech, ['speech', speech_level, speech_unit])
else:
    st.warning("No materials avialable found")

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