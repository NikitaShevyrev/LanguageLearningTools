import streamlit as st
from page_supplementaries import get_sidebar, get_footer, get_data_button, delete_data_from_sessionstate
from src.shuffled_table import get_shuffled_table, get_filelike_table

from deep_translator import GoogleTranslator
from typing import List
from os.path import basename
from glob import glob
from PIL import Image
import base64
from json import load

# >>>> Important functions

def get_basic_module(
    predefined_source_lang: str = "",
    predefined_source_words: List[str] = [],
    predefined_translation_lang: str = "",
    predefined_translation: List[str] = [],
    key: str = "creator"
) -> None:
    
    if not isinstance(predefined_source_words, list):
        raise TypeError(f"predefined_source_words is expected tobe list. Received: {type(predefined_source_words)}")
    
    if not isinstance(predefined_translation, list):
        raise TypeError(f"predefined_translation is expected tobe list. Received: {type(predefined_translation)}")
    
    if len(predefined_source_words) != len(predefined_source_words):
        raise Exception("Predefined lists should have the same length.")
    
    
    if len(predefined_source_words) == 0:
        disabled = False
    else:
        disabled = True

    with st.expander("Create group of words"):

        if disabled:
            num_words_to_learn = st.number_input(
                "Select number of words to learn",
                min_value = 0,
                value = len(predefined_source_words),
                step = 1,
                disabled = disabled,
                key = f"num_words_to_learn_{key}"
            )

        else:
            num_words_to_learn = st.number_input(
                "Select number of words to learn",
                min_value = 0,
                step = 1,
                key=f"num_words_to_learn_{key}"
            )

        col0a, col0b, col0c, col0d = st.columns([0.1, 0.37, 0.11, 0.42])

        col1a, col1b = st.columns(2)

        langs_dict = GoogleTranslator().get_supported_languages(as_dict = True)
        langs_dict['auto'] = 'auto'
        langs_keys = list(langs_dict.keys())


        if disabled:
            if predefined_source_lang not in langs_keys:
                raise KeyError(f"{predefined_source_lang} is not accessible in GoogleTranslator")

            if predefined_translation_lang not in langs_keys:
                raise KeyError(f"{predefined_translation_lang} is not accessible in GoogleTranslator")
        

        with col0b:
            st.subheader("Want-To-Learn Words")
        

        with col0c:
            swap_button = st.button(":left_right_arrow:", key=f"swap_{key}")
            if swap_button:
                st.session_state[f'language_1_{key}'], st.session_state[f'language_2_{key}'] = (
                    st.session_state[f'language_2_{key}'], st.session_state[f'language_1_{key}']
                )
                st.session_state[f'source_words_{key}'], st.session_state[f'translation_{key}'] = (
                    st.session_state[f'translation_{key}'], st.session_state[f'source_words_{key}']
                )
        

        with col0d:
            st.subheader("Mother Tongue Translation")


        with col1a:
            try:
                lang1 = st.session_state[f'language_1_{key}']

            except:
                if disabled:
                    lang1 = predefined_source_lang
                else:
                    lang1 = 'auto'
                st.session_state[f'language_1_{key}'] = lang1
            
            source_lang = st.selectbox(
                "Select language to translate from",
                options = langs_keys,
                index = langs_keys.index(lang1),
                disabled = disabled,
                key = f"source_lang_{key}"
            )
            if source_lang != lang1:
                st.session_state[f'language_1_{key}'] = source_lang
        
        with col1b:
            try:
                lang2 = st.session_state[f'language_2_{key}']
            
            except:
                if disabled:
                    lang2 = predefined_translation_lang
                else:
                    lang2 = 'english'
                st.session_state[f'language_2_{key}'] = lang2
            
            target_lang = st.selectbox(
                "Select language to translate to",
                options = langs_keys,
                index = langs_keys.index(lang2),
                disabled = disabled,
                key = f"target_lang_{key}"
            )
            if target_lang != lang2:
                st.session_state[f'language_2_{key}'] = target_lang


        col2a, col2b = st.columns(2)
        

        with col2a:
            try:
                if disabled:
                    source_values = st.session_state[f'source_words_{key}']
                else:
                    source_words_num = len(st.session_state[f'source_words_{key}'])
                    if source_words_num >= num_words_to_learn:
                        source_values = st.session_state[f'source_words_{key}']
                    else:
                        source_values = st.session_state[f'source_words_{key}'] + ['word' for _ in range(num_words_to_learn-source_words_num)]
            
            except:
                if disabled:
                    source_values = predefined_source_words
                else:
                    source_values = ['word' for _ in range(num_words_to_learn)]
            
            source_words = [
                st.text_input("Write a word to learn", source_values[i], key=f"input{i}_{key}", disabled=disabled)
                for i in range(num_words_to_learn)
            ]
            st.session_state[f'source_words_{key}'] = source_words
        

        with col2b:
            if disabled:
                try:
                    offer_translation = st.session_state[f'translation_{key}']
                except:
                    offer_translation = predefined_translation
            
            else:
                offer_translation = [
                    GoogleTranslator(source = langs_dict[source_lang], target = langs_dict[target_lang]).translate(elem)
                    for elem in source_words
                ]

            translation = [
                st.text_input("Translation [change if wrong]", value=offer_translation[i], key=f"translate{i}_{key}", disabled=disabled)
                for i in range(num_words_to_learn)
            ]
            st.session_state[f'translation_{key}'] = translation


    # >>>> main
    if num_words_to_learn > 0:

        translation_words_DF = get_shuffled_table(source_words, translation)

        with st.expander("Show result"):
            st.markdown(translation_words_DF.style.hide(axis='index').hide(axis='columns').to_html(), unsafe_allow_html=True)

        st.markdown("---")

        if disabled:
            filename_part = key.split('.')[0]
        else:
            filename_part = "shuffled_table"

        result_filename = st.text_input("Select filename", f"my_{filename_part}", key = f"result_filename_{key}")
        if not result_filename.endswith(".png"):
            result_filename += ".png"

        file_like = get_filelike_table(translation_words_DF)

        btn = st.download_button(
            label="Download table", # image
            data=file_like,
            file_name=result_filename,
            mime="image/png"
        )
    
    # >>>>

def get_accessible_wordpairs_section():

    pics_path = "free_materials/preview_pics"
    pics_names = [basename(name) for name in glob(pics_path + "/*.jpg")]

    with open('free_materials/files_dict.json', 'r') as f:
        files_dict = load(f)    

    tab_names = [files_dict[name]['alias'] for name in pics_names]
    
    for name, tab in zip(pics_names, st.tabs(tab_names)):

        with open('free_materials/logos/youtube.png', "rb") as file_:
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        link = files_dict[name]['url']
        with tab:

            col1, col2 = st.columns(2)
            with col1:
                image = Image.open(f"{pics_path}/{name}")
                st.image(image)

            with col2:
                st.markdown("### About video")
                st.markdown(files_dict[name]['description'])

                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(
                        f"<a href='{link}'><img src='data:image/png;base64,{data_url}' class='img-fluid' width='64'>",
                        unsafe_allow_html=True
                    )
                with col4:
                    get_data_button('english', files_dict[name]['english'], 'russian', files_dict[name]['russian'], name)
                    if st.session_state[f'data_btn_{name}']:
                        delete_data_from_sessionstate(name, pics_names)
            
            st.divider()


# >>>> ######### #########

st.title("Shuffled table tool")

# >>>> Add words

st.markdown("""
    ### Do you want to:
    - **learn** new words **faster**?
    - **remember** them **longer**?
    - **recall** them **easier**?

    Then try out **Shuffled tables** with predefined word pairs or add your own.
""")


tab_eng_rus, tab_creator = st.tabs(['Eng-Rus', 'Create own table'])

with tab_eng_rus:
    get_accessible_wordpairs_section()

with tab_creator:
    get_data_button('', [], '', [], 'creator')
    # get_basic_module()


placeholder = st.empty()

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
get_sidebar()