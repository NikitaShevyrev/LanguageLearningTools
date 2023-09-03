import streamlit as st
from page_supplementaries import get_sidebar, get_footer
import time
import datetime as dt
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from gforms import Form
from gforms.elements import Value

url_gform = 'https://docs.google.com/forms/d/e/1FAIpQLSep762IUaVGBDbuO_JqC4xO0AU63HU14n22Ime0N49LYKHnng/viewform'
url_gtable = 'https://docs.google.com/spreadsheets/d/1BnTx2pRWDICfhw77z8IlOzk1R7uKhEd8nw9H1Buq-dU/edit?usp=sharing'
results_sent = False

class Filler:

    def __init__(self, total_seconds: int) -> None:
        
        self.user_name = st.session_state['user_name']
        
        self.total_seconds = total_seconds
        
        self.section = st.session_state['section']
        
        self.target_lang, self.fluent_lang = st.session_state['current_source_translation_table'].columns
        
        self.video_name = st.session_state['name'] if self.section == 'Watch & Learn' else 'none'
        
        self.proficiency = st.session_state['proficiency'] if self.section in ['Become Grammar Pro', 'Master Parts of Speech'] else 'none'
        
        self.unit = st.session_state['unit'] if self.section in ['Become Grammar Pro', 'Master Parts of Speech'] else 'none'
        
        self.exercise = st.session_state['name'] if self.section in ['Become Grammar Pro', 'Master Parts of Speech'] else 'none'

    def callback(self, element, page_index, element_index):
        # fill an element based on its position
        if page_index == 0 and element_index == 0:
            result = self.user_name
        
        elif page_index == 0 and element_index == 1:
            result = str(self.total_seconds)
        
        elif page_index == 0 and element_index == 2:
            result = self.section
        
        elif page_index == 0 and element_index == 3:
            result = self.target_lang
        
        elif page_index == 0 and element_index == 4:
            result = self.fluent_lang
        
        elif page_index == 0 and element_index == 5:
            result = self.video_name
        
        elif page_index == 0 and element_index == 6:
            result = self.proficiency
        
        elif page_index == 0 and element_index == 7:
            result = self.unit
        
        elif page_index == 0 and element_index == 8:
            result = self.exercise
        
        else:
            result = Value.DEFAULT

        return result

def check_uniqueness(username: str) -> bool:
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    try:
        usernames = conn.read(spreadsheet=url_gtable, usecols=[1])
        unique_usernames = pd.unique(usernames[usernames.columns[0]])
    except:
        unique_usernames = []
    return username in unique_usernames

get_sidebar()

st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if (
    ('current_shuffled_table' not in st.session_state.keys())
    or ('current_source_translation_table' not in st.session_state.keys())
):
    st.markdown("""
        Please, generate shuffled table before visiting this page.
        To do so, visit one of the next pages and follow the workflow
        presented there.

        ### Pages to visit:
        - Watch & Learn
        - Become Grammar Pro
        - Master Parts of Speech
        - Create Own Table
    """)

else:
    pass
    with st.form("User configuration"):
        st.markdown(
            """
            Please, provide your user name. After doing the exercise
            you'll be able to check your results in Results section
            and even compare them with other users' ones.
            
            **Note:** 
            1. It is not obligatory to write your actual name.
            2. Using this form for the **first time** check that your user name
            is unique. The **"name exists"** space should be **False**.
            """
        )
        user_option = "Friendly Capybara" if 'user_name' not in st.session_state.keys() else st.session_state['user_name']
        user_name = st.text_input("User name:", user_option)
        st.write(f"User exists: {check_uniqueness(user_name)}")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state['user_name'] = user_name
            st.success("User name has been saved.")

    # check user name existence
    if 'user_name' in st.session_state.keys():

        tab_shuffled_table, tab_translation = st.tabs(['Shuffled Table', 'Translation Table'])

        with tab_shuffled_table:
            # shuffled_table = st.session_state['current_shuffled_table'].copy()
            # shuffled_table.columns = [f'Column {i}' for i in range(len(shuffled_table.columns))]
            # st.dataframe(shuffled_table, hide_index=True)
            st.markdown(st.session_state['current_shuffled_table'].style.hide(axis='index').hide(axis='columns').to_html(), unsafe_allow_html=True)

        with tab_translation:
            st.dataframe(st.session_state['current_source_translation_table'], hide_index=True)

        st.text(" ")

        col1, col2, col3, col4, col5 = st.columns(5)

        if 'start' not in st.session_state.keys():
            st.session_state['start'] = 0.0

        if 'stop' not in st.session_state.keys():
            st.session_state['stop'] = 0.0

        with col1:
            btn_start = st.button('Start')
            if btn_start:
                st.session_state['start'] = time.time()

        with col2:
            btn_stop = st.button('Stop')
            if btn_stop:
                st.session_state['stop'] = time.time()

        with col3:
            btn_restart = st.button('Restart')
            if btn_restart:
                st.session_state['start'] = 0.0
                st.session_state['stop'] = 0.0

        with col4:
            result = st.session_state['stop'] - st.session_state['start']        
            
            total_seconds = int(result if result > 0 else 0.0)
            hours = total_seconds // (60 * 60)
            minutes = (total_seconds - hours * 60 * 60) // 60
            seconds = total_seconds - hours * 60 * 60 - minutes * 60
            if btn_start and not btn_stop:
                st.warning("Stopwatch is on!")
            else:
                try:
                    attempt_time = dt.time(hour=hours, minute=minutes, second=seconds)
                except:
                    attempt_time = dt.time(hour=0, minute=0, second=0)
                st.markdown(f'<p class="big-font">{attempt_time}</p>', unsafe_allow_html=True)

        with col5:
            btn_submit = st.button('Submit results', disabled=result <= 0)
            if btn_submit:
                try:
                    filler = Filler(total_seconds)
                    form = Form()
                    form.load(url_gform)
                    form.fill(filler.callback)
                    form.submit()
                    results_sent = True
                except:
                    pass

if results_sent:
    success = st.success("Result has been submitted succesfully!")
    time.sleep(2)
    success.empty()

get_footer()