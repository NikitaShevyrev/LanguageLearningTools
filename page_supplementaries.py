import streamlit as st
from st_pages import Page, show_pages, add_page_title, Section

from typing import List
from PIL import Image
import base64
from deep_translator import GoogleTranslator
import pandas as pd

from src.shuffled_table import get_shuffled_table, get_filelike_table
from config import config as CFG

langs_dict = GoogleTranslator().get_supported_languages(as_dict = True)
langs_dict['auto'] = 'auto'
langs_dict['entity_to_translate'] = 'entity_to_translate'
langs_keys = list(langs_dict.keys())
langs_keys_no_auto = [lang for lang in langs_keys if lang != 'auto' and lang != 'entity_to_translate']

def get_sidebar() -> None:

    add_page_title()

    show_pages(
        [
            Page("Home.py", "Home"),
            Section("Shuffled Tables"),
            # Pages after a section will be indented
            # Page("pages/shuffled_tables.py", "Shuffled Table Tool"),
            Page("pages/about.py", "About"),
            Page("pages/watch_and_learn.py", "Watch & Learn"),
            Page("pages/become_grammar_pro.py", "Become Grammar Pro"),
            Page("pages/master_parts_of_speech.py", "Master Parts of Speech"),
            Page("pages/create_own_table.py", "Create Own Table"),
            # Unless you explicitly say in_section=False
            # Page("Not in a section", in_section=False)
        ]
    )

    with st.sidebar:
        st.markdown(
            """
            ```
            Supervised by:
            Tatyana Arsentyeva
            
            Code and design by:
            Nikita Shevyrev 
            n.shevyrev@gmail.com
            """
        )

def get_footer() -> None:

    st.markdown("-----")

    st.markdown("""
    #### Having ideas for further tools improvements, don't hesitate to contact us.\n
    🚀 Telegram: [ArsentyevaSchool](https://t.me/arsentyevaschool) \n
    📧 Email: n.shevyrev@gmail.com
    """)

def get_data_button(
    lang1: str, lang1_words: List[str], lang2: str, lang2_words: List[str], name: str
) -> None:

    data_btn = st.button("Let's shuffle", key=f"data_btn_{name}")
    if data_btn:        
        st.session_state['lang1'] = lang1
        st.session_state['lang1_words'] = lang1_words
        st.session_state['lang2'] = lang2
        st.session_state['lang2_words'] = lang2_words
        st.session_state['name'] = name

        try:
            del st.session_state[f'language_1_{name}'], st.session_state[f'language_2_{name}']
            del st.session_state[f'source_words_{name}'], st.session_state[f'translation_{name}']
        except:
            pass

def delete_data_from_sessionstate(name: str, all_names: List[str]) -> None:

    names_to_del = list(all_names)
    names_to_del.remove(name)
    for del_key in names_to_del:
        if f'language_1_{del_key}' in st.session_state.keys():
            del st.session_state[f'language_1_{del_key}'], st.session_state[f'language_2_{del_key}']
            del st.session_state[f'source_words_{del_key}'], st.session_state[f'translation_{del_key}']

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
                st.text_input("Translation [change if wrong]", value=offer_translation[i], key=f"translate{i}_{key}") # , disabled=disabled
                for i in range(num_words_to_learn)
            ]
            st.session_state[f'translation_{key}'] = translation


    # >>>> main
    if num_words_to_learn > 0:

        translation_words_DF = get_shuffled_table(source_words, translation)

        with st.expander("Show result"):
            st.markdown(translation_words_DF.style.hide(axis='index').hide(axis='columns').to_html(), unsafe_allow_html=True)

        st.markdown("---")

        col3a, col3b = st.columns(2)

        with col3a:
            shfl_tbl_filename = st.text_input("Select filename", f"my_shuffled_table", key = f"shfl_tbl_filename_{key}")
            if not shfl_tbl_filename.endswith(".png"):
                shfl_tbl_filename += ".png"
            
            file_like_shfl_tbl = get_filelike_table(translation_words_DF)

            btn2 = st.download_button(
                label="Download shuffled table", # image
                data=file_like_shfl_tbl,
                file_name=shfl_tbl_filename,
                mime="image/png"
            )

        with col3b:
            src_trns_filename = st.text_input("Select filename", f"my_source_translation_pairs_table", key = f"src_trns_filename_{key}")
            if not src_trns_filename.endswith(".png"):
                src_trns_filename += ".png"

            source_translation_DF = pd.DataFrame(
                data=[[src, trns] for src, trns in zip(source_words, translation)],
                columns=[source_lang, target_lang]
            )

            file_like_src_trns = get_filelike_table(source_translation_DF, False)

            btn1 = st.download_button(
                label=f"Download {langs_dict[source_lang].capitalize()}-{langs_dict[target_lang].capitalize()} pairs table", # image
                data=file_like_src_trns,
                file_name=src_trns_filename,
                mime="image/png"
            )
    
    # >>>>

def get_watch_and_learn_section(want_to_learn_lang: str, fluent_lang: str) -> None:

    pics_path = "free_materials/preview_pics"

    WNL_info = CFG[want_to_learn_lang]['WNL']

    pics_names = WNL_info.keys()
    tab_names = [WNL_info[name]['alias'] for name in pics_names]
    
    for name, tab in zip(pics_names, st.tabs(tab_names)):

        with open('free_materials/logos/youtube.png', "rb") as file_:
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        link = WNL_info[name]['url']
        with tab:

            col1, col2 = st.columns(2)
            with col1:
                image = Image.open(f"{pics_path}/{name + WNL_info[name]['extension']}")
                st.image(image)

            with col2:
                st.markdown("### About video")
                st.markdown(WNL_info[name]['description'])

                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(
                        f"<a href='{link}'><img src='data:image/png;base64,{data_url}' class='img-fluid' width='64'>",
                        unsafe_allow_html=True
                    )
                with col4:

                    lang1_words = WNL_info[name]['words_to_learn']

                    try:
                        shuffle_btn_state = st.session_state[f'data_btn_{name}']
                    except:
                        shuffle_btn_state = False

                    if shuffle_btn_state:
                        able_to_find = False
                        if 'recommended_translation' in WNL_info[name].keys():
                            if fluent_lang in WNL_info[name]['recommended_translation'].keys():
                                able_to_find = True
                                lang2_words = WNL_info[name]['recommended_translation'][fluent_lang]
                            
                        if not able_to_find:
                            lang2_words = [
                                GoogleTranslator(source = langs_dict[want_to_learn_lang], target = langs_dict[fluent_lang]).translate(elem)
                                for elem in lang1_words
                            ]
                    else:
                        lang2_words = ["no_translation" for i in range(len(lang1_words))]
                    
                    get_data_button(
                        lang1 = want_to_learn_lang,
                        lang1_words = lang1_words,
                        lang2 = fluent_lang,
                        lang2_words = lang2_words,
                        name = name
                    )
                    if st.session_state[f'data_btn_{name}']:
                        delete_data_from_sessionstate(name, pics_names)
            
            st.divider()

def get_simple_section(want_to_learn_lang: str, fluent_lang: str, keys: List[str]) -> None:

    section_info = CFG[want_to_learn_lang]
    for cfg_key in keys:
        section_info = section_info[cfg_key]

    tab_names = section_info.keys()
    
    for name, tab in zip(tab_names, st.tabs(tab_names)):
        
        with tab:

            lang1_words = section_info[name]['words_to_learn']

            try:
                shuffle_btn_state = st.session_state[f'data_btn_{name}']
            except:
                shuffle_btn_state = False

            if shuffle_btn_state:
                try:
                    lang2_words = section_info[name]['recommended_translation'][fluent_lang]
                except:
                    lang2_words = [
                        GoogleTranslator(source = langs_dict[want_to_learn_lang], target = langs_dict[fluent_lang]).translate(elem)
                        for elem in lang1_words
                    ]
            else:
                lang2_words = ["no_translation" for i in range(len(lang1_words))]
            
            get_data_button(
                lang1 = want_to_learn_lang,
                lang1_words = lang1_words,
                lang2 = fluent_lang,
                lang2_words = lang2_words,
                name = name
            )
            if st.session_state[f'data_btn_{name}']:
                delete_data_from_sessionstate(name, tab_names)
            
            st.divider()
