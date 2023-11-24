import streamlit as st
import plotly.graph_objects as go

font = dict(
    size=16,
    color="rgb(49, 51, 63)"
)

config = {'displayModeBar': False}

def draw_chart(x_axis, y_axis, row):
    fig = go.Figure()
    # Player BG
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][5]],
        name='player_bg',
        orientation='h',
        marker=dict(
            color="#308FB8"
        ),
        hoverinfo='skip'
    ))
    # Player G
    fig.add_trace(go.Bar(
        y=[y_axis],
        x=[row[x_axis][4] - row[x_axis][5]],
        name='player_g',
        orientation='h',
        marker=dict(
            color="#5fb2d5"
        ),
        hoverinfo='skip'
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
        ),
        hoverinfo='skip'
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
        ),
        hoverinfo='skip'
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
        ),
        hoverinfo='skip'
    ))
    fig.add_annotation(
        x=row[x_axis][3] + (row[x_axis][2] - row[x_axis][1]) +
        (row[x_axis][1] - row[x_axis][0]) / 2,
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
        ),
        hoverinfo='skip'
    ))
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False)
    fig.update_layout(barmode='stack', height=100, margin=dict(
        l=0, r=0, b=0, t=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config=config)


def draw_estimate_chart(player_win, player_g, opponent_g):
    fig = go.Figure()
    # Player G
    fig.add_trace(go.Bar(
        y=[0],
        x=[player_g],
        name='player_g',
        orientation='h',
        marker=dict(
            color="#5fb2d5"
        ),
        hoverinfo='skip'
    ))
    fig.add_annotation(
        x=player_g / 2,
        y=0,
        text=f"{player_g}%",
        showarrow=False,
        font=font
    )
    # Player Win
    fig.add_trace(go.Bar(
        y=[0],
        x=[player_win - player_g],
        name='player_win',
        orientation='h',
        marker=dict(
            color="#9ccfe5"
        ),
        hoverinfo='skip'
    ))
    fig.add_annotation(
        x=player_g + (player_win - player_g) / 2,
        y=0,
        text=f"{player_win}%",
        showarrow=False,
        font=font
    )
    # Opponent Win
    fig.add_trace(go.Bar(
        y=[0],
        x=[100 - player_win - opponent_g],
        name='opponent_win',
        orientation='h',
        marker=dict(
            color="#d7eadc"
        ),
        hoverinfo='skip'
    ))
    fig.add_annotation(
        x=player_win + (100 - player_win - opponent_g) / 2,
        y=0,
        text=f"{100 - player_win}%",
        showarrow=False,
        font=font
    )
    # Opponent G
    fig.add_trace(go.Bar(
        y=[0],
        x=[opponent_g],
        name='opponent_g',
        orientation='h',
        marker=dict(
            color="#a4d1b0"
        ),
        hoverinfo='skip'
    ))
    fig.add_annotation(
        x=player_win + (100 - player_win - opponent_g) + opponent_g / 2,
        y=0,
        text=f"{opponent_g}%",
        showarrow=False,
        font=font
    )
    fig.update_xaxes(visible=False, range=[0, 100])
    fig.update_yaxes(visible=False)
    fig.update_layout(barmode='stack', height=100, margin=dict(
        l=0, r=0, b=0, t=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config=config)
