import streamlit as st
import pandas as pd
from backgammon import streamlit_backgammon

@st.cache_data()
def load_data():
    df = pd.read_pickle('data/xg_data.pkl')
    return df['Position']

def update_value():
    st.session_state.index += 1

positions = load_data()

if 'index' not in st.session_state:
    st.session_state['index'] = 0

streamlit_backgammon(position=positions[st.session_state['index']])
st.button('Next', on_click=update_value)
