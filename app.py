import random
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sklearn.metrics.pairwise import cosine_similarity

from backgammon import streamlit_backgammon
from slider_with_buttons import slider
from src.chart import draw_estimate_chart, draw_chart
from src.param import get_id
from src.xg import get_xgid, get_position


@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data.pkl')


def get_random_position(df):
    return random.randint(0, len(df))


def init_state(df):
    st.session_state['game_state'] = 'guess'
    st.session_state['player_win'] = 50
    st.session_state['player_g'] = 0
    st.session_state['opponent_g'] = 0
    query_params = st.query_params
    position_id = get_id(query_params, len(df))
    if position_id is not None:
        st.session_state['index'] = position_id
    else:
        st.session_state['index'] = get_random_position(df)


def show_answer():
    st.session_state['game_state'] = 'review'


def next_position(position_id):
    st.query_params['id'] = [position_id]
    init_state(df)


def random_position(df):
    next_position(str(get_random_position(df)))


def similar_position(df):
    position = get_position(st.session_state['xgid'])
    if position is None:
        row = df.iloc[st.session_state['index']]
        position = row['Position']
    cosine_similarities = cosine_similarity(
        np.array(position).reshape(1, -1), df['Position'].tolist())
    similarity = pd.DataFrame(
        cosine_similarities.transpose(), columns=['similarity'])
    top_10 = similarity.sort_values(
        'similarity', ascending=False).head(10).index
    # pick a random position from the top 10
    # exclude the current position
    next_position(str(random.choice(top_10[1:])))


def estimate_rate(names, values):
    player_g, player_win, opponent_g = slider(names, values)
    st.session_state['player_g'] = player_g
    st.session_state['player_win'] = player_win
    st.session_state['opponent_g'] = 100 - opponent_g


def draw_position(df):
    row = df.iloc[st.session_state['index']]
    entry = {
        'position': row['Position'],
        'cube': int(row['CubeB'] * row['ActiveP']),
    }
    streamlit_backgammon(entry=entry, key='board')


def show_analysis(df):
    row = df.iloc[st.session_state['index']]
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


def show_xgid(df):
    xgid = get_xgid(df.iloc[st.session_state['index']])
    st.text_input('XGID', xgid, key='xgid')


def share_button():
    url = f'https://gammonestimate.streamlit.app/?id={st.session_state["index"]}'
    components.html(
        f"""
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" 
        class="twitter-share-button" 
        data-show-count="false"
        data-url="{url}"
        data-hashtags="gammonestimate">
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    )


st.set_page_config(
    page_title='Gammon Estimate',
    page_icon=':game_die:',
    layout='wide',
)

df = load_data()

if 'game_state' not in st.session_state:
    init_state(df)

draw_position(df)

placeholder = st.empty()

# user will input the win/gammon percentages
if st.session_state['game_state'] == 'guess':
    estimate_rate(['gammon %', 'win %', 'gammon %'], [0, 50, 100])

draw_estimate_chart(st.session_state['player_win'],
                    st.session_state['player_g'],
                    st.session_state['opponent_g'],
                    placeholder)

if st.session_state['game_state'] == 'guess':
    _, _, col3 = st.columns([4, 1, 1])
    with col3:
        st.button('Guess', on_click=show_answer, type='primary')

if st.session_state['game_state'] == 'review':
    show_analysis(df)
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        show_xgid(df)
    with col2:
        st.button('Similar', on_click=similar_position,
                  args=(df,), type='secondary')
    with col3:
        st.button('Random', on_click=random_position,
                  args=(df,), type='primary')
    st.divider()
    share_button()
