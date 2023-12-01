import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from backgammon import streamlit_backgammon
from src.chart import draw_estimate_chart, draw_chart
from src.param import get_id


@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data.pkl')


def get_random_position(df):
    return random.randint(0, len(df))


def init_state(df):
    st.session_state['game_state'] = 'guess'
    query_params = st.experimental_get_query_params()
    position_id = get_id(query_params, len(df))
    if position_id is not None:
        st.session_state['index'] = position_id
    else:
        st.session_state['index'] = get_random_position(df)


def show_answer():
    st.session_state['game_state'] = 'review'


def next_position(df):
    query_params = {
        'id': [str(get_random_position(df))]
    }
    st.experimental_set_query_params(**query_params)
    init_state(df)


def estimate_rate(name, label, value):
    def update_state():
        st.session_state[name] = st.session_state[f'{name}_input']
    st.slider(label, 0, 100, value, format='%d%%',
              key=name, label_visibility='visible')
    st.number_input(
        label, 0, 100, st.session_state[name], key=f'{name}_input',
        on_change=update_state, label_visibility='hidden')


st.set_page_config(
    page_title='Gammon Estimate',
    page_icon=':game_die:'
)

df = load_data()

if 'game_state' not in st.session_state:
    init_state(df)

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
    with st.expander('Your guess', expanded=True):
        estimate_rate('player_win', 'Player Win', 50)
        estimate_rate('player_g', 'Player Gammon', 0)
        estimate_rate('opponent_g', 'Opponent Gammon', 0)

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
        ['No double', f"{row['Doubled_equB']: .3f}"],
        ['Double/Take', f"{row['Doubled_equDouble']: .3f}"],
        ['Double/Pass', f"{row['Doubled_equDrop']: .3f}"]
    ]
    df_equities = pd.DataFrame(equities, columns=['Action', 'Equity'])
    df_equities.set_index('Action', inplace=True)
    st.table(df_equities)
    st.button('Next', on_click=next_position, args=(df,), type='primary')
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
