import streamlit as st
from typing import List

def get_sidebar() -> None:

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

def delete_data_from_sessionstate(name: str, all_names: List[str]) -> None:

    names_to_del = list(all_names)
    names_to_del.remove(name)
    for del_key in names_to_del:
        if f'language_1_{del_key}' in st.session_state.keys():
            del st.session_state[f'language_1_{del_key}'], st.session_state[f'language_2_{del_key}']
            del st.session_state[f'source_words_{del_key}'], st.session_state[f'translation_{del_key}']
