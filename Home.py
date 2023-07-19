import streamlit as st
from page_supplementaries import get_sidebar, get_footer

get_sidebar()

st.markdown("""
    ### About project:
    We develop new approaches to learning new words and training grammar
    issues based on specially integrated repetition techniques.
    The trainings don't take much time, about 10  minutes a day.

""")

st.markdown("""
    ### Motivation:
    Most language teaching portals offer methods that are considerably
    less effective as:

    - they require one to stay deeply concentrated, which appears mentally
    and physically exhausting.
    - their cost for remembering material is high in terms of time spent
    per day.
    - it is hard to find the portals, which remind one to rerun a training
    based on forgetting curve.

""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        **As busy people**, we know the cost of your time. Thus, we are
        thrilled to share the opportunity to learn languages more
        comfortably and effectively.
    """)

with col2:
    st.markdown("""
        **As researchers**, we are interested in the development of new tools
        pushing the boundaries of the existing methods in language learning.
    """)

st.markdown("""
    
    ### Benefits:
    - You will learn the linguistic material without any tension and dull
    memorization.
    - The techniques are time saving and easy to use.
    - While doing the tasks you will certainly master the vocabulary or
    grammar rules being trained.
""")

get_footer()
