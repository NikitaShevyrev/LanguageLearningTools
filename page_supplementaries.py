import streamlit as st

def get_sidebar():
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

def get_footer():

    st.markdown("-----")

    st.markdown("""
    #### Having ideas for further tools improvements, don't hesitate to contact us.\n
    🚀 Telegram: [ArsentyevaSchool](https://t.me/arsentyevaschool) \n
    📧 Email: n.shevyrev@gmail.com
    """)
