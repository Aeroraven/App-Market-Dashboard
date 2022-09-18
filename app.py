from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from data_utils import *
import dash_dangerously_set_inner_html as ht
from render import componentImport
import dash_bootstrap_components as dbc
import plotly.io as pio
import math
from plotly.subplots import make_subplots

renderHTML = ht.DangerouslySetInnerHTML

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

df_radar_ct = [4, 4, 4, 4, 4]
df_radar_std = [4, 4, 4, 4, 4]


# App Interactions
@app.callback(
    Output('example-graph-7', 'figure'),
    Input("dropdown-app", 'value')
)
def acb_update_wordcloud(app_name):
    cl = generate_word_cloud_by_app(app_name)
    fig_wordcloud = go.Figure()
    fig_wordcloud.add_trace(
        go.Image(z=cl)
    )
    fig_wordcloud.update_layout(title="Comment Wordcloud", template=pio.templates['plotly_dark'])
    return fig_wordcloud

@app.callback(
    Output('example-graph-n', 'figure'),
    Input("dropdown-app", 'value')
)
def acb_update_comment_sentiment(app_name):
    cl = get_app_reivews_polarity(app_name)
    fig_wordcloud = go.Figure()
    fig_wordcloud.add_trace(
        go.Bar(x=['Positive',"Neutral","Negative"],y=cl)
    )
    fig_wordcloud.update_layout(title="Comment Sentiment Polarity (Selected App)", template=pio.templates['plotly_dark'])
    return fig_wordcloud


@app.callback(
    Output('example-graph', 'figure'),
    Input("dropdown-category", 'value')
)
def acb_update_rating_dist(category):
    df_ratings = get_rating_stats(get_category_i(category))
    fig = px.histogram(df_ratings, x="Rating", nbins=40)
    fig.update_layout(title="Rating Distribution (Category)", template=pio.templates['plotly_dark'])
    fig.update_layout(template=pio.templates['plotly_dark'])
    return fig


@app.callback(
    Output('example-graph-8', 'figure'),
    Input("dropdown-app", 'value')
)
def acb_update_app(app_name):
    df_app_rating_id = get_app_rating_ref(app_name)
    df_app_reviews_id = get_app_reviews_ref(app_name)
    df_app_install_id = get_app_downloads_ref(app_name)
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=df_app_rating_id,
        delta={'reference': df_radar_ct[1], 'increasing': {'color': "orange"}},
        title={'text': "Rating Indicator", 'font': {'size': 16}},
        gauge={'axis': {'range': [None, 5]},
               'bar': {'color': "orange"},
               'steps': [
                   {'range': [0, 1], 'color': "#444444"},
                   {'range': [1, 2], 'color': "#555555"},
                   {'range': [2, 3], 'color': "#666666"},
                   {'range': [3, 4], 'color': "#777777"},
                   {'range': [4, 5], 'color': "#888888"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': df_radar_ct[1]}},
        domain={'row': 0, 'column': 0})
    )
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=math.log10(int(df_app_install_id)),
        delta={'reference': math.log10(DataCache.avg_download), 'increasing': {'color': "orange"}},
        title={'text': "Popularity(Download) Indicator", 'font': {'size': 16}},
        gauge={'axis': {'range': [None, 8]},
               'bar': {'color': "orange"},
               'steps': [
                   {'range': [0, 1], 'color': "#444444"},
                   {'range': [1, 2], 'color': "#555555"},
                   {'range': [2, 3], 'color': "#666666"},
                   {'range': [3, 4], 'color': "#777777"},
                   {'range': [4, 5], 'color': "#888888"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,
                             'value': math.log10(DataCache.avg_download)}},
        domain={'row': 1, 'column': 0})
    )
    fig_gauge.update_layout(template=pio.templates['plotly_dark'])
    fig_gauge.update_layout(grid={'rows': 2, 'columns': 1, 'pattern': "independent"})
    return fig_gauge


@app.callback(
    Output('example-graph-9', 'figure'),
    Input("dropdown-app", 'value')
)
def acb_update_app2(app_name):
    df_app_crating_id = get_app_cr_ref(app_name)
    df_app_reviews_id = get_app_reviews_ref(app_name)
    fig_gauge_2 = go.Figure()
    fig_gauge_2.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=math.log10(df_app_reviews_id),
        domain={'row': 0, 'column': 0},
        delta={'reference': math.log10(df_radar_ct[4] / df_radar_std[1] * DataCache.avg_reviews + 1),
               'increasing': {'color': "orange"}},
        title={'text': "Topicality(Review) Indicator", 'font': {'size': 16}},
        gauge={
            'axis': {'range': [1, 8]},
            'bar': {'color': "lightblue"},
            'steps': [
                {'range': [0, 2], 'color': "#444444"},
                {'range': [2, 4], 'color': "#555555"},
                {'range': [4, 6], 'color': "#666666"},
                {'range': [6, 8], 'color': "#777777"},
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,
                          'value': math.log10(df_radar_ct[4] / df_radar_std[1] * DataCache.avg_reviews)},

        }
    ))
    fig_gauge_2.add_trace(go.Indicator(
        mode="number",
        value=df_app_crating_id,
        number={'suffix': "+"},
        title={'text': "Content Rating", 'font': {'size': 16}},
        domain={'row': 1, 'column': 0})
    )
    fig_gauge_2.update_layout(template=pio.templates['plotly_dark'])
    fig_gauge_2.update_traces(gauge_axis_dtick="D2")
    fig_gauge_2.update_layout(grid={'rows': 2, 'columns': 1, 'pattern': "independent"})
    return fig_gauge_2


@app.callback(
    Output('dropdown-app', 'options'),
    Input("dropdown-category", 'value')
)
def acb_change_category_find_apps(category):
    return get_application_list(get_category_i(category))


@app.callback(
    Output('example-graph-3', 'figure'),
    Input("dropdown-category", 'value')
)
def acb_change_category(category):
    df_rrd_ap, df_rrd_rv, df_rrd_rt, df_rrd_ins = get_review_rating_download_bubble_map(get_category_i(category))
    fig_rrd_scatter = go.Figure()
    fig_rrd_scatter.add_trace(go.Scatter(x=df_rrd_rv, y=df_rrd_rt, text=df_rrd_ap, mode='markers',
                                         marker=dict(size=df_rrd_ins)))
    fig_rrd_scatter.update_layout(xaxis_type="log")
    fig_rrd_scatter.update_layout(title="Popularity & Quality Map", template=pio.templates['plotly_dark'])
    return fig_rrd_scatter


@app.callback(
    Output('example-graph-4', 'figure'),
    Input("dropdown-category", 'value')
)
def acb_change_category_radar(category):
    global df_radar_ct, df_radar_std
    df_radar_ct, df_radar_std, label_radar = get_cate_radar(get_category_i(category))
    fig_cate_radar = go.Figure()
    fig_cate_radar.add_trace(go.Scatterpolar(
        r=df_radar_ct,
        theta=label_radar,
        fill='toself',
        name="Current Category"
    ))
    fig_cate_radar.add_trace(go.Scatterpolar(
        r=df_radar_std,
        theta=label_radar,
        fill='toself',
        name="All Apps"
    ))
    fig_cate_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    fig_cate_radar.update_layout(title="Category Indicator", template=pio.templates['plotly_dark'])
    fig_cate_radar.update_layout(showlegend=True)
    return fig_cate_radar


@app.callback(
    Output('example-graph-2', 'figure'),
    Input("dropdown-category", 'value')
)
def acb_change_category_pie(category):
    label_cr, df_cr_var, df_cr_inst, df_cr_rate = get_content_rating_stats_by_category(get_category_i(category))
    fig_content_rating = go.Figure()
    fig_content_rating.add_trace(go.Pie(
        values=df_cr_var,
        labels=label_cr)
    )
    fig_content_rating.update_layout(title="Content Rating Distribution", template=pio.templates['plotly_dark'])
    return fig_content_rating


# App Layout

app.layout = html.Div(id="dark-theme-container", children=[
    renderHTML(componentImport("style_injector")),
    renderHTML(componentImport("appbar")),
    html.Div(
        style={
            "margin-left": "5px",
            "vertical-align": "top"
        },
        children=[
            html.Div(children=[
                html.A(children="App Category"),
                dcc.Dropdown(get_categories(), id='dropdown-category', value="Game"),
                dcc.Graph(
                    id='example-graph-3',
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='example-graph-4',
                        ),
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block"
                    }
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='example-graph-2',
                        )
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block"
                    }
                ),
                dcc.Graph(
                    id='example-graph',
                ),
            ],
                style={
                    "width": "50%",
                    "display": "inline-block"
                }
            ),
            html.Div(children=[
                html.A(children="Selected App"),
                dcc.Dropdown(["Honkai Impact 3rd"], id='dropdown-app', value="Honkai Impact 3rd"),
                html.Div(children=[
                    html.Div(children=[
                        dcc.Graph(
                            id='example-graph-8',
                        ),
                    ], style={
                        "width": "50%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    }),
                    html.Div(children=[
                        dcc.Graph(
                            id='example-graph-9',
                        ),
                    ], style={
                        "width": "50%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    }),
                ]),

                dcc.Graph(
                    id='example-graph-7',
                ),
                dcc.Graph(
                    id='example-graph-n',
                ),


            ], style={
                "width": "50%",
                "display": "inline-block",
                "vertical-align": "top",
            }),

        ],

    )])

if __name__ == '__main__':
    app.run_server(debug=True)
