import random
import pandas as pd
import streamlit as st

from backgammon import streamlit_backgammon
from src.chart import draw_estimate_chart, draw_chart


@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data.pkl')


def get_random_position(df):
    return random.randint(0, len(df))


def init_state():
    st.session_state['game_state'] = 'guess'
    st.session_state['index'] = get_random_position(df)
    st.session_state['player_win'] = 50
    st.session_state['player_g'] = 0
    st.session_state['opponent_g'] = 0


def show_answer():
    st.session_state['game_state'] = 'review'


def next_position(df):
    init_state()


df = load_data()

if 'game_state' not in st.session_state:
    init_state()

row = df.iloc[st.session_state['index']].copy()  # Make a copy of the row
if row['ActiveP'] == -1:
    # reverse the board and flip values of position
    row['Position'] = [-i for i in row['Position'][::-1]]

# render the board
entry = {
    'position': row['Position'],
    'cube': int(row['CubeB'] * row['ActiveP']),
}
streamlit_backgammon(entry=entry, key='board')

# user will input the win/gammon percentages
if st.session_state['game_state'] == 'guess':
    st.session_state['player_win'] = st.slider(
        'Player Win', 0, 100, 50, format='%d%%')
    st.session_state['player_g'] = st.slider(
        'Player Gammon', 0, 100, format='%d%%')
    st.session_state['opponent_g'] = st.slider(
        'Opponent Gammon', 0, 100, format='%d%%')

st.write('Your guess')
draw_estimate_chart(st.session_state['player_win'],
                    st.session_state['player_g'], st.session_state['opponent_g'])

if st.session_state['game_state'] == 'guess':
    st.button('Guess', on_click=show_answer, type='primary')

if st.session_state['game_state'] == 'review':
    tab_nd, tab_td = st.tabs(['No Double', 'Double/Take'])
    with tab_nd:
        draw_chart('Doubled_Eval', 'No Double', row)
        st.write('Cubeless Equity:  ', f"{row['Doubled_Eval'][6]:.3f}")
    with tab_td:
        draw_chart('Doubled_EvalDouble', 'Double/Take', row)
        st.write('Cubeless Equity:  ', f"{row['Doubled_EvalDouble'][6]:.3f}")
    st.write('Cubuful Equities')
    equities = [
        ['No double', row['Doubled_equB']],
        ['Double/Take', row['Doubled_equDouble']],
        ['Double/Pass', row['Doubled_equDrop']]
    ]
    df_equities = pd.DataFrame(equities, columns=['Action', 'Equity'])
    df_equities.set_index('Action', inplace=True)
    st.table(df_equities)
    st.button('Next', on_click=next_position, args=(df,), type='primary')

# st.dataframe(row, width=1000)
