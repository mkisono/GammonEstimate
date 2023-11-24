import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from backgammon import streamlit_backgammon

@st.cache_data()
def load_data():
    return pd.read_pickle('data/xg_data.pkl')

def update_value():
    st.session_state.index += 1

def draw_chart(x_axis, y_axis):
    font = dict(
        size=16,
        color="rgb(49, 51, 63)"
    )
    fig = go.Figure()
    # Player BG
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][5]],
        name='player_bg',
        orientation='h',
        marker=dict(
            color="#308FB8"
        )
    ))
    # Player G
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][4] - row[x_axis][5]],
        name='player_g',
        orientation='h',
        marker=dict(
            color="#5fb2d5"
        )
    ))
    fig.add_annotation(
        x=row[x_axis][5] + (row[x_axis][4] - row[x_axis][5]) / 2,
        y=0,
        text=f"{row[x_axis][4]*100:.2f}%",
        showarrow=False,
        font=font
    )
    # Player Win
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][3] - row[x_axis][4]],
        name='player_win',
        orientation='h',
        marker=dict(
            color="#9ccfe5"
        )
    ))
    fig.add_annotation(
        x=row[x_axis][4] + (row[x_axis][3] - row[x_axis][4]) / 2,
        y=0,
        text=f"{row[x_axis][3]*100:.2f}%",
        showarrow=False,
        font=font
    )
    # Opponent Win
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][2] - row[x_axis][1]],
        name='opponent_win',
        orientation='h',
        marker=dict(
            color="#d7eadc"
        )
    ))
    fig.add_annotation(
        x=row[x_axis][3] + (row[x_axis][2] - row[x_axis][1]) / 2,
        y=0,
        text=f"{row[x_axis][2]*100:.2f}%",
        showarrow=False,
        font=font
    )
    # Opponent G
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][1] - row[x_axis][0]],
        name='opponent_g',
        orientation='h',
        marker=dict(
            color="#a4d1b0"
        )
    ))
    fig.add_annotation(
        x=row[x_axis][3] + (row[x_axis][2] - row[x_axis][1]) + (row[x_axis][1] - row[x_axis][0]) / 2,
        y=0,
        text=f"{row[x_axis][1]*100:.2f}%",
        showarrow=False,
        font=font
    )
    # Opponent BG
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][0]],
        name='opponent_bg',
        orientation='h',
        marker=dict(
            color="#71B784"
        )
    ))
    
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False)
    fig.update_layout(barmode='stack', height=100, margin=dict(l=0, r=0, b=0, t=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

df = load_data()

if 'index' not in st.session_state:
    st.session_state['index'] = 20

row = df.iloc[st.session_state['index']]
if row['ActiveP'] == -1:
    # reverse the board and flip values of position
    row['Position'] = [-i for i in row['Position'][::-1]]

entry = {
    'position': row['Position'],
    'cube': int(row['CubeB'] * row['ActiveP']),
}
streamlit_backgammon(entry=entry, key='board')
st.button('Next', on_click=update_value)

tab_nd, tab_td = st.tabs(['No Double', 'Double/Take'])

with tab_nd:
    draw_chart('Doubled_Eval', 'No Double')

with tab_td:
    draw_chart('Doubled_EvalDouble', 'Double/Take')

# st.dataframe(row, width=1000)
