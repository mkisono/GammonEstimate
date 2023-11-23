import streamlit as st
import pandas as pd
from backgammon import streamlit_backgammon

@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data.pkl')

def update_value():
    st.session_state.index += 1

df = load_data()

if 'index' not in st.session_state:
    st.session_state['index'] = 20

row = df.iloc[st.session_state['index']]
if row['ActiveP'] == -1:
    # reverse the board and flip values of position
    row['Position'] = [-i for i in row['Position'][::-1]]

entry = {
    'position': row['Position'],
    'cube': int(row['CubeB'] * row['ActiveP'])
}
streamlit_backgammon(entry=entry, key='board')
st.button('Next', on_click=update_value)
st.dataframe(row, width=1000)
