import streamlit as st
import plotly.graph_objects as go

font = dict(
    size=16,
    color="rgb(49, 51, 63)"
)

config = {'displayModeBar': False, 'staticPlot': True}
height = 60


def _add_trace(fig, x_axis, y_axis, name, color):
    fig.add_trace(go.Bar(
        x=[x_axis],
        y=[y_axis],
        name=name,
        orientation='h',
        marker=dict(
            color=color
        ),
        hoverinfo='skip'
    ))


def _add_annotation(fig, x_axis, y_axis, text):
    fig.add_annotation(
        x=x_axis,
        y=y_axis,
        text=text,
        showarrow=False,
        font=font
    )


def _show_chart(fig, range):
    fig.update_xaxes(visible=False, range=range)
    fig.update_yaxes(visible=False)
    fig.update_layout(barmode='stack', height=height, margin=dict(
        l=0, r=0, b=0, t=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config=config)


def draw_chart(x_axis, y_axis, row):
    fig = go.Figure()
    # Player BG
    _add_trace(fig, row[x_axis][5], y_axis, 'player_bg', '#308FB8')
    # Player G
    _add_trace(fig, row[x_axis][4] - row[x_axis]
               [5], y_axis, 'player_g', '#5fb2d5')
    _add_annotation(fig, row[x_axis][5] + (row[x_axis][4] -
                    row[x_axis][5]) / 2, 0, f"{row[x_axis][4]*100:.2f}%")
    # Player Win
    _add_trace(fig, row[x_axis][3] - row[x_axis]
               [4], y_axis, 'player_win', '#9ccfe5')
    _add_annotation(fig, row[x_axis][4] + (row[x_axis][3] -
                    row[x_axis][4]) / 2, 0, f"{row[x_axis][3]*100:.2f}%")
    # Opponent Win
    _add_trace(fig, row[x_axis][2] - row[x_axis][1],
               y_axis, 'opponent_win', '#d7eadc')
    _add_annotation(fig, row[x_axis][3] + (row[x_axis][2] -
                    row[x_axis][1]) / 2, 0, f"{row[x_axis][2]*100:.2f}%")
    # Opponent G
    _add_trace(fig, row[x_axis][1] - row[x_axis]
               [0], y_axis, 'opponent_g', '#a4d1b0')
    _add_annotation(fig, row[x_axis][3] + (row[x_axis][2] - row[x_axis][1]) + (
        row[x_axis][1] - row[x_axis][0]) / 2, 0, f"{row[x_axis][1]*100:.2f}%")
    # Opponent BG
    _add_trace(fig, row[x_axis][0], y_axis, 'opponent_bg', '#71B784')

    _show_chart(fig, [0, 1])
    # fig.update_xaxes(visible=False, range=[0, 1])
    # fig.update_yaxes(visible=False)
    # fig.update_layout(barmode='stack', height=height, margin=dict(
    #     l=0, r=0, b=0, t=0), showlegend=False)
    # _, chart , _ = st.columns([1, 8, 1])
    # with chart:
    #     st.plotly_chart(fig, use_container_width=True, config=config)


def draw_estimate_chart(player_win, player_g, opponent_g):
    fig = go.Figure()
    # Player G
    _add_trace(fig, player_g, 0, 'player_g', '#5fb2d5')
    _add_annotation(fig, player_g / 2, 0, f"{player_g}%")
    # Player Win
    _add_trace(fig, player_win - player_g, 0, 'player_win', '#9ccfe5')
    _add_annotation(fig, player_g + (player_win - player_g) /
                    2, 0, f"{player_win}%")
    # Opponent Win
    _add_trace(fig, 100 - player_win - opponent_g,
               0, 'opponent_win', '#d7eadc')
    _add_annotation(fig, player_win + (100 - player_win -
                    opponent_g) / 2, 0, f"{100 - player_win}%")
    # Opponent G
    _add_trace(fig, opponent_g, 0, 'opponent_g', '#a4d1b0')
    _add_annotation(fig, player_win + (100 - player_win -
                    opponent_g) + opponent_g / 2, 0, f"{opponent_g}%")

    _show_chart(fig, [0, 100])

    # fig.update_xaxes(visible=False, range=[0, 100])
    # fig.update_yaxes(visible=False)
    # fig.update_layout(barmode='stack', height=height, margin=dict(
    #     l=0, r=0, b=0, t=0), showlegend=False)
    # _, chart , _ = st.columns([1, 8, 1])
    # with chart:
    #     st.plotly_chart(fig, use_container_width=True, config=config)
