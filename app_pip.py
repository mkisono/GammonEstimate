import numpy as np
import pandas as pd
import streamlit as st

from backgammon import streamlit_backgammon
from src.chart import draw_chart


@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data_pip.pkl')


def draw_position(index, row):
    # render the board
    entry = {
        'position': row['Position'],
        'cube': int(row['CubeB'] * row['ActiveP']),
    }
    streamlit_backgammon(entry=entry, key=index)


def show_analysis(row):
    tab_nd, tab_td = st.tabs(['No Double', 'Double/Take'])
    with tab_nd:
        draw_chart('Doubled_Eval', 'No Double', row)
        st.write('Cubeless Equity:  ', f"{row['Doubled_Eval'][6]:.3f}")
    with tab_td:
        draw_chart('Doubled_EvalDouble', 'Double/Take', row)
        st.write('Cubeless Equity:  ', f"{row['Doubled_EvalDouble'][6]:.3f}")
    st.write('Cubuful Equities')
    equities = [
        ['No double', f"{row['Doubled_equB']: .3f}"],
        ['Double/Take', f"{row['Doubled_equDouble']: .3f}"],
        ['Double/Pass', f"{row['Doubled_equDrop']: .3f}"]
    ]
    df_equities = pd.DataFrame(equities, columns=['Action', 'Equity'])
    df_equities.set_index('Action', inplace=True)
    st.table(df_equities)


def trailer_can_take_formula(x):
    # 137ページの公式
    if x <= 62:
        # subtract 5 from x, divede by 7, and round down
        return (x - 5) // 7 + x
    # 10% round up to the nearest integer and add 1
    return int(np.ceil(x * 0.1)) + 1 + x


st.set_page_config(
    page_title='Can Trailer Take?',
    page_icon=':game_die:'
)

start = 19
end = 122

df = load_data()

with st.sidebar:
    player_pip = st.slider('Player Pip Count', start, end, 62, 1)
    # set pip range for opponent
    opponent_pip_min, opponent_pip_max = st.slider(
        'Opponent Pip Count', start, end, (player_pip, trailer_can_take_formula(player_pip)), 1)

df_pip = df[(df['player_pip_count'] == player_pip) &
            df['opponent_pip_count'].between(opponent_pip_min, opponent_pip_max)]
for index, row in df_pip.iterrows():
    draw_position(index, row)
    show_analysis(row)
