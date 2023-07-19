import streamlit as st
from page_supplementaries import get_sidebar, get_footer
from PIL import Image
from config import config as CFG

get_sidebar()

st.markdown("""
    ### Do you want to:
    - **learn** new words **faster**?
    - **remember** them **longer**?
    - **recall** them **easier**?

    Then try out **Shuffled tables** with predefined word pairs or add your own.
            
    The following section will help one with using shuffled tables
    for the studying as well as with preparing for exercising.
""")

st.markdown('---')

st.subheader("**HOWTO:** study using SHUFFLED TABLE?")

steps = list(CFG['howto']['shuffled_table']['learn'].keys())
steps_num = len(steps)

col_howto1, col_howto2 = st.columns(2)

with col_howto1:
    img1_container = st.container()

with col_howto2:
    img2_container = st.container()

step_choice = st.radio("Choose step", options=[f"Step {i+1}" for i in range(steps_num)], horizontal=True, label_visibility = 'collapsed')
idx = int(step_choice.split(' ')[1]) - 1

image = Image.open(CFG['howto']['shuffled_table']['learn'][f'step_{idx+1}']['pic_path'])
img1_container.image(image)
image2 = Image.open(CFG['howto']['shuffled_table']['learn'][f'step_{idx+1}']['description_path'])
img2_container.image(image2)

get_footer()