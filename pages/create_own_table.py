import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
from gforms import Form
from gforms.elements import Value
from page_supplementaries import (
    get_sidebar, get_footer, get_data_button, get_basic_module,
    remove_from_session_state
)

url_gform = 'https://docs.google.com/forms/d/e/1FAIpQLSexayhUlCTwNQBCeX9h30rnMabVdtx9NgUun-_nfrEIB2567A/viewform'
url_gtable = 'https://docs.google.com/spreadsheets/d/1kN5QM-p6gS7LMIfmLb4VSD_YJTF2HGdzge6R5TNAOiw/edit?usp=sharing'
results_sent = False

# comments about the following code
# https://discuss.streamlit.io/t/text-input-behavior-for-updating-a-session-state-value-is-not-intuitive-for-my-use-case/38814/2

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

################
    
class CustomExerciseFiller:

    def __init__(self) -> None:

        self.user_name = st.session_state['user_name']
        
        self.set_name = st.session_state['exercise_name']
        
        self.target_lang = st.session_state['current_source_translation_table'].columns[0]
        self.fluent_lang = st.session_state['current_source_translation_table'].columns[1]

        target_words = list(st.session_state['current_source_translation_table'].iloc[:,0].values)
        fluent_words = list(st.session_state['current_source_translation_table'].iloc[:,1].values)

        num_words = len(target_words)

        for i in range(10):
            target_w_value = target_words[i] if i < num_words else 'none'
            setattr(self, f"target_l_text_{i+1}", target_w_value)
            
            fluent_w_value = fluent_words[i] if i < num_words else 'none'
            setattr(self, f"fluent_l_text_{i+1}", fluent_w_value)

    def callback(self, element, page_index, element_index):
        # fill an element based on its position
        if page_index == 0 and element_index == 0:
            result = self.user_name
        
        elif page_index == 0 and element_index == 1:
            result = self.set_name
        
        elif page_index == 0 and element_index == 2:
            result = self.target_lang
        
        elif page_index == 0 and element_index == 3:
            result = self.fluent_lang
        
        elif page_index == 0 and (3 < element_index < 14):
            result = getattr(self, f"target_l_text_{element_index-3}")
        
        elif page_index == 0 and (13 < element_index < 25):
            result = getattr(self, f"fluent_l_text_{element_index-13}")
        
        else:
            result = Value.DEFAULT

        return result

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

def get_usernames() -> list:
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        usernames = conn.read(spreadsheet=url_gtable, usecols=[1])
        unique_usernames = pd.unique(usernames[usernames.columns[0]])
        unique_usernames = list(unique_usernames)
    except:
        unique_usernames = []
    return unique_usernames

def retreive_records(df: pd.DataFrame, key: str, sort_options: dict) -> pd.DataFrame:
    if len(sort_options[key]) > 0:
        condn_mask = df[key] == sort_options[key][0]
        for i in range(1, len(sort_options[key])):
            condn_mask |= (df[key] == sort_options[key][i])
        df = df[condn_mask]
    return df

def get_unique_vals(df: pd.DataFrame, key: str) -> np.ndarray:
    vals = pd.unique(df[key])
    return vals[vals != 'none']

with st.container(border=True):

    st.write("Tables Preparation Configuration")

    creator_mode = st.radio("Select creator mode:", ['Create new exercise', 'Load existing exercise'], horizontal=True)

    radio_disable = True if creator_mode == 'Load existing exercise' else False
    radio_index = 1 if creator_mode == 'Load existing exercise' else 0
    user_mode = st.radio("User search mode:", ['New User', 'Existing User'], index=radio_index, disabled=radio_disable, horizontal=True)

    # load existing names
    usernames = get_usernames()

    # get user_name
    if user_mode == 'New User':
        username = st.text_input('Write unique username', "Type Here")
        disable_save = (username in usernames) or (username == "Type Here")

        if username in usernames:
            st.warning("Username is not unique. Please, provide different one.")
        
    else:
        options = ['Undefined']
        options.extend(usernames)
        username = st.selectbox("Select username", options=options)
        disable_save = username == 'Undefined'
    
    if creator_mode == 'Create new exercise':
        new_exercise_name = st.text_input('Give name to a new exercise', "Exercise name")
        disable_save = True if new_exercise_name == "Exercise name" else disable_save
    
    disable_save = True if creator_mode == 'Load existing exercise' else disable_save
    disable_load = True

    if creator_mode == 'Load existing exercise' and username != 'Undefined':

        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            df = conn.read(spreadsheet=url_gtable, usecols=list(range(25)))

            df['Отметка времени'] = pd.to_datetime(df['Отметка времени'], format='%d.%m.%Y %H:%M:%S')

            df.rename(columns={'Отметка времени': "Timestamp"}, inplace=True)

            columns = [
                col for col in df.columns
                if col != 'User Name'
                and not col.startswith('Target L Text')
                and not col.startswith('Fluent L Text')
                and col != 'Name Of The Set'
            ]

            # choose filtering by column
            sort_by = st.multiselect("Select additional column(-s) for sorting by:", columns)

            sort_options = {}
            # add filtering
            sort_options['User Name'] = [username]#[[username]]
            df = retreive_records(df, 'User Name', sort_options)
            
            if 'Timestamp' in sort_by:
                min_val = df['Timestamp'].min()
                max_val = df['Timestamp'].max()
                accepted_time_interval = (min_val, max_val)
                (min_date_choice, max_date_choice) = st.date_input(
                    "Select time interval to find records:", value=accepted_time_interval, min_value=min_val, max_value=max_val
                )
                min_date_choice = pd.Timestamp(min_date_choice)
                max_date_choice = pd.Timestamp(year=max_date_choice.year, month=max_date_choice.month, day=max_date_choice.day, hour=23, minute=59, second=59)
                df = df[(pd.Timestamp(min_date_choice) <= df['Timestamp']) & (df['Timestamp'] <= pd.Timestamp(max_date_choice))]
            
            if 'Target Language' in sort_by:
                sort_options['Target Language'] = [[st.selectbox("Select target language to find records:", get_unique_vals(df, 'Target Language'))]]
                df = retreive_records(df, 'Target Language', sort_options)
            
            if 'Fluent Language' in sort_by:
                sort_options['Fluent Language'] = [[st.selectbox("Select fluent language to find records:", get_unique_vals(df, 'Fluent Language'))]]
                df = retreive_records(df, 'Fluent Language', sort_options)
            
            # sort_options['Name Of The Set'] = [[st.selectbox("Select name of the set to find the record:", get_unique_vals(df, 'Name Of The Set'))]]
            sort_options['Name Of The Set'] = [st.selectbox("Select name of the set to find the record:", get_unique_vals(df, 'Name Of The Set'))]
            df = retreive_records(df, 'Name Of The Set', sort_options)
            
            st.dataframe(df, hide_index=True)

            if df.shape[0] != 1:
                st.warning(f"The above table should have only **ONE SET** to allow load. Currently there are: {df.shape[0]}")
            else:
                disable_load = False
            
            if st.session_state.get('user_load'):
                target_cols = [
                    col for col in df.columns
                    if col.startswith('Target L Text')
                    and df[col].values[0] != 'none'
                ]

                fluent_cols = [
                    col for col in df.columns
                    if col.startswith('Fluent L Text')
                    and df[col].values[0] != 'none'
                ]
                
                if len(target_cols) != len(fluent_cols):
                    raise Exception("Wrong form filling.")
                
                pairs_num = len(target_cols)

                # Remove emptify table automatically

                st.session_state['lang1'] = ''
                st.session_state['lang1_words'] = []
                st.session_state['lang2'] = ''
                st.session_state['lang2_words'] = []
                st.session_state['name'] = 'creator'
                st.session_state['section'] = "Own Table"
                st.session_state['proficiency'] = "none"
                st.session_state['unit'] = "none"
                st.session_state[f"num_words_to_learn_creator"] = 0

                remove_from_session_state(f'language_1_creator')
                remove_from_session_state(f'language_2_creator')
                remove_from_session_state(f'source_words_creator')
                remove_from_session_state(f'translation_creator')
                remove_from_session_state('current_source_translation_table')
                
                source_input_keys = [elem for elem in st.session_state.keys() if elem.startswith('input')]
                for source_input_key in source_input_keys:
                    remove_from_session_state(source_input_key)
                
                translation_keys = [elem for elem in st.session_state.keys() if elem.startswith('translate')]
                for translation_key in translation_keys:
                    remove_from_session_state(translation_key)
                
                # Load new data

                st.session_state['lang1'] = df['Target Language'].values[0]
                st.session_state['lang1_words'] = list(df[target_cols].values[0])
                st.session_state['lang2'] = df['Fluent Language'].values[0]
                st.session_state['lang2_words'] = list(df[fluent_cols].values[0])
                st.session_state['name'] = sort_options['Name Of The Set'][0]#'own_table'
                st.session_state[f'num_words_to_learn_{name}'] = pairs_num
        
        except:
            st.warning('Something went wrong')
    
    col_empty, col_load, col_save = st.columns(3)

    with col_empty:
        get_data_button('', [], '', [], 'creator', "Own Table", button_name = "Emptify Table")
    
    with col_load:
        load_btn = st.button("Load Exercise", disabled=disable_load, key='user_load')
    
    with col_save:
        if 'current_source_translation_table' in st.session_state.keys():
            last_words_num = len(st.session_state['current_source_translation_table'].iloc[:,0].values)
            if last_words_num > 0 and st.session_state.get("num_words_to_learn_creator") == 0:
                name = st.session_state['name'] if 'name' in st.session_state.keys() else 'creator'
                st.session_state[f'num_words_to_learn_{name}'] = last_words_num

        if st.session_state.get("num_words_to_learn_creator") == 0:
            disable_save = True
        
        elif st.session_state.get("num_words_to_learn_creator") is None:
            disable_save = True
        
        save_btn = st.button("Save Exercise", disabled=disable_save, key='user_save')

        if save_btn:
            st.session_state['user_name'] = username
            st.session_state['exercise_name'] = new_exercise_name
            try:
                filler = CustomExerciseFiller()
                form = Form()
                form.load(url_gform)
                form.fill(filler.callback)
                form.submit()
                
                success = st.success("Result has been submitted succesfully!")
                time.sleep(2)
                success.empty()
            except:
                save_failure = st.warning("Something went wrong! Please, contact developers.")
                time.sleep(2)
                save_failure.empty()

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
