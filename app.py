import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
clicked_value = -1
app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border'   : 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


def get_skills(job_title):
    df2 = pd.read_csv('./data/2.csv')
    data = df2.loc[:, [job_title, 'Skills']].sort_values(by=job_title, ascending=False)
    fig = px.bar(data,
                 y=job_title,
                 x="Skills")
    return fig


def get_avg_job_title():
    df1 = pd.read_csv('./data/1.csv')
    FIG_avg_job_title = px.bar(df1,
                               y="Avg Salary(K)",
                               x="Job Title",
                               orientation='v')
    FIG_avg_job_title.update_xaxes(tickangle=-30)
    FIG_avg_job_title.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    print()
    print([FIG_avg_job_title['data'][0]['marker']['color']] * len(FIG_avg_job_title['data'][0]['x']))
    return FIG_avg_job_title


# fig.update_layout(clickmode='event+select')
#
# fig.update_traces(marker_size=20)

app.layout = html.Div([
    html.Div([
        html.H2("Data Science Job Market Analysis"),
        html.H3("ASDS-2022"),
        html.H4("Rima Shahbazyan")],

        style={'margin'    : 'auto',
               'padding'   : '10px',
               'text-align': 'center'}
    ),
    dcc.Graph(
        id='my-graph', style={'width': '180vh', 'height': '90vh'},
    ),
    html.Div([], id='click-data', className='div',
             style={'margin'    : 'auto',
                    'padding'   : '10px',
                    'text-align': 'center'}),
    dcc.Graph(
        id='skill-graph', style={'width': '180vh', 'height': '90vh'}, figure=get_skills("All")
    ),


],
    style={'margin' : 'auto',
           'padding': '10px'})


@app.callback(
    Output('click-data', 'children'),
    Input('my-graph', 'clickData'))
def display_click_data(clickData):
    if clickData is None or clickData['points'][0]['pointNumber'] == clicked_value:
        return None
    else:
        job_title = clickData['points'][0]['x']

        return html.H4(f'Filtered by {job_title}')

@app.callback(Output('my-graph', 'figure'),
              [Input('my-graph', 'clickData')])
def update_image(clickData):
    df1 = pd.read_csv('./data/1.csv')
    FIG_avg_job_title = px.bar(df1,
                               y="Avg Salary(K)",
                               x="Job Title",
                               orientation='v')
    FIG_avg_job_title.update_xaxes(tickangle=-30)
    FIG_avg_job_title.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    color = [FIG_avg_job_title['data'][0]['marker']['color']] * len(FIG_avg_job_title['data'][0]['x'])
    FIG_avg_job_title['data'][0]['marker']['color'] = color
    print(color)
    global clicked_value
    if clickData is not None:
        if clickData['points'][0]['pointNumber'] == clicked_value:
            clicked_value = -1
            color[clickData['points'][0]['pointNumber']] = '#636efa'
        else:
            clicked_value = clickData['points'][0]['pointNumber']
            color[clickData['points'][0]['pointNumber']] = 'red'
        FIG_avg_job_title['data'][0]['marker']['color'] = color
    return FIG_avg_job_title


@app.callback(Output('skill-graph', 'figure'),
              [Input('my-graph', 'clickData')])
def update_image(clickData):
    if clickData is None:
        job_title = 'All'

    elif clickData['points'][0]['pointNumber'] == clicked_value:
        job_title = 'All'

    else:
        job_title = clickData['points'][0]['x']

    return get_skills(job_title)


if __name__ == '__main__':
    app.run_server(debug=False)
