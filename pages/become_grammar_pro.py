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
    
    Here you can find exercises to study grammatical
    topics.
            
    **What is the workflow?**
    1. Choose the language you want to learn.
    2. Choose the desired level of proficiency for studying
    language and a grammar unit.
    3. Select an exercise from the row of uploaded excercises.
    4. Press **Let's shuffle** to prepare data for
    the Shuffled Table generation.
    5. Unfold the *Create group of words* section to see
    the pairs of words/phrases describing the rules of
    translation while doing the grammar exercise.
    Examples of pairs:
    - Grammatical structure - Formula
    (e.g. Present Cont. - am/is/are + V-ing)
    - Singular form noun - Plural form Noun
    - Adjective - Comparison form Adjective
    6. Unfold the *Show result* section to see
    ***the Shuffled Table uniquely designed for you***.
    It's highly unlikely that anyone will manage to get the same.
    7. Choose the name for the pairs and the shuffled tables
    and download them by pressing the *Download* buttons.
    8. You're awesome. Now you are ready to learn new
    words and phrases. Visit the *About* section to see how
    to use the generated materials.
    
""")

col_grammar1, col_grammar2 = st.columns(2)

with col_grammar1:
    source_lang_grammar = st.selectbox(
        "Select language to learn",
        options = [key for key in CFG.keys() if key != 'howto'],
        key = f"source_lang_grammar"
    )
    if source_lang_grammar not in langs_keys:
        st.warning("Selected language is not a known one.")

with col_grammar2:
    # target_lang_options_grammar = list(langs_keys_no_auto)
    # target_lang_options_grammar.remove(source_lang_grammar)
    target_lang_grammar = st.selectbox(
        "Select language to translate to",
        options = ["entity_to_translate"],
        key = f"target_lang_grammar",
        disabled=True
    )

try:
    grammar_levels = list(CFG[source_lang_grammar]['grammar'].keys())
    # grammar_levels = ['Any'] + grammar_levels
except:
    grammar_levels = ['empty']

col_grammar3, col_grammar4 = st.columns(2)

with col_grammar3:
    grammar_level = st.selectbox(
        "Select proficiency level",
        options = grammar_levels,
        key = f"level_grammar"
    )

try:
    grammar_units = list(CFG[source_lang_grammar]['grammar'][grammar_level].keys())
    # grammar_units = ['Any'] + grammar_units
except:
    grammar_units = ['empty']

with col_grammar4:
    grammar_unit = st.selectbox(
        "Select grammar unit",
        options = grammar_units,
        key = f"unit_grammar"
    )

if grammar_units[0] != 'empty':
    get_simple_section(source_lang_grammar, target_lang_grammar, ['grammar', grammar_level, grammar_unit])
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
