import gunicorn
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px



radar = pd.read_csv("data/radar_chart.csv", index_col = 0)    # ta a ler bem
histogram = pd.read_csv("data/histogram_usage.csv", index_col = 0)
heatmap = pd.read_csv("data/correlation_heatmap.csv", index_col = 0)




Personality_measure = ['Neuroticism','Extraversion','Openness','Agreeableness','Conscientiouness','Impulsiveness','Sensation Seing']
Drugs = ['Alcohol','Amphet','Amyl','Benzos','Caff','Cannabis','Choc','Coke','Crack','Ecstasy','Heroin','Ketamine','Legalh','LSD','Meth','Mushrooms','Nicotine','Semer','VSA']
Participants = ['Age','Gender','Education','Country','Ethnicity']


drugs_choices = [{'label': 'Alcohol', 'value': 'Alcohol'},
           {'label': 'Amphetamine', 'value': 'Amphet'},
           {'label': 'Amyl Nitrite', 'value': 'Amyl'},
           {'label': 'Benzodiazepine', 'value': 'Benzos'},
           {'label': 'Caffeine', 'value': 'Caff'},
           {'label': 'Cannabis', 'value': 'Cannabis'},
           {'label': 'Chocolate', 'value': 'Choc'},
           {'label': 'Cocaine', 'value': 'Coke'},
           {'label': 'Crack', 'value': 'Crack'},
           {'label': 'Ecstasy', 'value': 'Ecstasy'},
           {'label': 'Heroin', 'value': 'Heroin'},
           {'label': 'Ketamine', 'value': 'Ketamine'},
           {'label': 'Legal Highs', 'value': 'Legalh'},
           {'label': 'LSD', 'value': 'LSD'},
           {'label': 'Methadone', 'value': 'Meth'},
           {'label': 'Mushrooms', 'value': 'Mushrooms'},
           {'label': 'Nicotine', 'value': 'Nicotine'},
           {'label': 'Semer', 'value': 'Semer'},
           {'label': 'Volatile Substance Abuse (VSA)', 'value': 'VSA'}]

drugs_list_1 = dcc.Dropdown(
    id= 'drug_1',

    clearable=False,
    searchable=False,
    options=drugs_choices,
    value='Caff'    ## add style = {}
)

drugs_list_2 = dcc.Dropdown(
    id= 'drug_2',
    clearable=False,
    searchable=False,
    options=drugs_choices,
    value='Meth'    ## add style = {}
)

drugs_list_3 = dcc.Dropdown(
    id= 'drug_3',
    clearable=False,
    searchable=False,
    options=drugs_choices,
    value='Coke'    ## add style = {}
)


trace_1 = go.Bar(x=histogram.columns, y=histogram.iloc[0].tolist(), name='Never Used',marker= dict(color='#61b8e2'))
trace_2 = go.Bar(x=histogram.columns, y=histogram.iloc[1].tolist(), name='More Than A Year',marker=dict(color='#a9cbda'))
trace_3 = go.Bar(x=histogram.columns, y=histogram.iloc[2].tolist(), name='Less Than A Year',marker=dict(color='#3680c1'))
layout=go.Layout(xaxis=dict(tickangle=-45),
                 barmode='stack',
                 width= 1400 ,
                 height= 250,
                 margin = dict(l=100,r=30,b=0, t=20),
                 plot_bgcolor= 'rgb(250, 250, 250)',
                 paper_bgcolor='rgb(250, 250, 250)',
                 font=dict(color='#757575', size=13, family='Helvetica'))
slider_1 = go.Figure(data = [trace_1,trace_2,trace_3],layout=layout)


################### The App itself  ####################################
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
            html.Div([
                html.H1(children='Drug Usage', style={'font-size':'40px'}),
                html.Label('Visualisation to compare the impact on how different personality traits affect the frequency in drug use and how it is related to age, gender and academic education level', style={'color':'#757575'}),
                html.Br(),
                html.Br(),
            ], className='side_bar'),
            html.Div([
                html.Label(id='User rate of drugs'),
                html.H3('1. Frequency of use of the drugs',
                        style={'padding': '5px','margin':'10px'}),
                html.Br(),
                dcc.Graph(id='slider_1',
                          figure=slider_1)
            ], className='box_usage_rate'),



            html.Div([
                html.H4("Choose Drug to Analyze:"),
                html.Br(),
                drugs_list_1
            ],className='box_drug_1'),



            html.Div([
                html.H4("Choose Drug to Analyze:"),
                html.Br(),
                drugs_list_2
            ],className='box_drug_2'),



            html.Div([
                html.H3('1. Radar Chart'),
                html.Label('(Personality Features are graded from 0 to 20)',
                           style={'font-size':'12px'}),
                html.Label(id='Radar_chart'),
                dcc.Graph(id='example-graph',
                          style={'padding': '15px','margin':'5px'}),
                html.Div([
                    html.Label('The radar chart explores the different Personality Features that describe the average user of each drug. Calculations ony account for users that uses the drug at least once in the last year.',
                               style={'font-size':'15px'}),
                ], className='box_comment_radar')
            ],className='box_radar'),


            html.Div([
                html.H3('2. Age'),
                html.Label('(%)',
                           style={'font-size':'12px'}),
                dcc.Graph(id='barplot_1')
            ],className='box_age'),
            html.Div([
                html.H3('3. Gender'),
                html.Label('(%)',
                           style={'font-size':'12px'}),
                dcc.Graph(id='barplot_2')
            ],className='box_gender'),
            html.Div([
                html.H3('4. Education'),
                html.Label('(%)',
                           style={'font-size':'12px'}),
                dcc.Graph(id='barplot_3')
            ],className='box_edu'),


            html.Div([
                html.H3("Which Drug do you want to know more about?"),
                html.Br(),
                drugs_list_3
            ],className='box_drug_3'),

            html.Div([
                html.H3('1. Characteristics that best describe the Regular User'),
                html.Br(),
                html.Div([
                    html.Div([
                        html.H3('Age',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Age_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Gender',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Gender_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Education',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Education_avg' ,
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Openness',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Openness_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Extraversion',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Extraversion_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Neuroticism',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Neuroticism_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Sensation Seing',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Sensation_Seing_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),
                    html.Div([
                        html.H3('Impulsiveness',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Impulsiveness_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Conscientiouness',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Conscientiouness_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),

                    html.Div([
                        html.H3('Agreeableness',
                                style={'padding': '5px','margin':'5px'}),
                        html.H4(id='Agreeableness_avg',
                                style={'padding': '5px','margin':'5px'})
                    ], className='box_avg'),
                ], style={'display': 'flex'}),

            ], className='box_average'),

            html.Div([
                html.H3('2. Correlation Heatmap',
                        style={'padding': '5px','margin':'10px'}),
                dcc.Graph(id='heatmap_1',
                          style={'padding': '5px','margin':'10px'})
            ],className='box_heatmap'),

            html.Div([
                html.H3('For further study of the drugs included in this dashboard you can visit the links bellow',style={'padding': '5px','margin':'10px'}),
                html.A('1. Alcohol', href='https://www.drugfreeworld.org/drugfacts/alcohol.html', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('2. Amphetamine', href='https://www.medicalnewstoday.com/articles/221211', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('3. Amyl Nitrite', href='https://adf.org.au/drug-facts/amyl-nitrite/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.Br(),
                html.Br(),
                html.A('4. Benzodiazepine', href='https://www.rxlist.com/benzodiazepines/drug-class.htm', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('5. Caffeine', href='https://adf.org.au/drug-facts/caffeine/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('6. Cannabis', href='https://adf.org.au/drug-facts/cannabis/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.Br(),
                html.Br(),
                html.A('7. Chocolate', href='https://www.sciencedirect.com/science/article/abs/pii/S0002822399003077', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('8. Cocaine', href='https://nida.nih.gov/publications/drugfacts/cocaine', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('9. Crack', href='https://americanaddictioncenters.org/cocaine-treatment/differences-with-crack', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.Br(),
                html.Br(),
                html.A('10. Ecstasy', href='https://nida.nih.gov/publications/drugfacts/mdma-ecstasymolly', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('11. Heroin', href='https://nida.nih.gov/publications/drugfacts/heroin', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('12. Ketamine', href='https://www.webmd.com/depression/features/what-does-ketamine-do-your-brain', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.Br(),
                html.Br(),
                html.A('13. Leaglh', href='https://www.bbc.com/news/uk-32857256', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('14. LSD', href='https://adf.org.au/drug-facts/lsd/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('15. Methadone', href='https://www.webmd.com/mental-health/addiction/what-is-methadone#1', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.Br(),
                html.Br(),
                html.A('16. Mushrooms', href='https://myhealth.alberta.ca/Alberta/Pages/What-are-magic-mushrooms.aspx', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('17. Nicotine', href='https://adf.org.au/drug-facts/nicotine/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'}),
                html.A('18. VSA', href='https://pubmed.ncbi.nlm.nih.gov/7866398/', target='_blank',style={'padding': '10px','margin':'20px','font-size':'20px'})
            ],className='box_info'),

            html.Div([
                html.H4('Dashboard created by:'),
                html.Br(),
                html.Label('André Pereira - m20210690'),
                html.Br(),
                html.Label('André Dias - m20210668'),
                html.Br(),
                html.Label('Mariana Ramalho - m20210687'),
            ],className='footer_1'),

            html.Div([
                html.H4('Sources'),
                html.Br(),
                html.A('Drug consumption (quantified) Data Set', href='https://archive.ics.uci.edu/ml/datasets/Drug+consumption+%28quantified%29', target='_blank')
            ], className = 'footer_2'),

        ], className= 'main')
])

@app.callback(
    [Output(component_id='example-graph', component_property='figure'),
     Output(component_id='barplot_1', component_property='figure'),
     Output(component_id='barplot_2', component_property='figure'),
     Output(component_id='barplot_3', component_property='figure'),
     Output(component_id='heatmap_1', component_property='figure'),
     Output('Age_avg', 'children'),
     Output('Gender_avg', 'children'),
     Output('Education_avg', 'children'),
     Output('Openness_avg', 'children'),
     Output('Extraversion_avg', 'children'),
     Output('Neuroticism_avg', 'children'),
     Output('Sensation_Seing_avg', 'children'),
     Output('Impulsiveness_avg', 'children'),
     Output('Conscientiouness_avg', 'children'),
     Output('Agreeableness_avg', 'children')],
    [Input(component_id='drug_1', component_property='value'),
     Input(component_id='drug_2', component_property='value'),
     Input(component_id='drug_3', component_property='value')]
)


def callback_1(drug_1,drug_2,drug_3):
    df_radar_1 = radar.loc[radar[drug_1] == 'Less than a year']
    df_radar_2 = radar.loc[radar[drug_2] == 'Less than a year']
    lista_1 = []
    lista_2 = []

    for p in Personality_measure:
        lista_1.append(round(df_radar_1[p].mean(), 4))
        lista_2.append(round(df_radar_2[p].mean(), 4))


    fig = go.Figure(data=go.Scatterpolar(
        r=lista_1,
        theta=Personality_measure,
        fill='toself',
        marker_color='#61b8e2',
        opacity=1,
        name= drug_1,
        hovertext= [p + ' = ' + str(round(df_radar_1[p].mean(), 4)) for p in Personality_measure]
    ))

    fig.add_trace(go.Scatterpolar(
        r=lista_2,
        theta=Personality_measure,
        fill='toself',
        marker_color='#a9cbda',
        hovertext= [p + ' = ' + str(round(df_radar_2[p].mean(), 4)) for p in Personality_measure]
    ))

    fig.update_layout(
        polar=dict(
            hole=0.05,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type='linear',
                autotypenumbers='strict',
                showline=False,
                showticklabels=False, ticks='',
                gridcolor='black'),
        ),
        xaxis=dict(tickangle=-45),
        width=600,
        height=600,
        margin=dict(l=150, r=100, t=40, b=40),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor='rgb(250, 250, 250)',
        paper_bgcolor='rgb(250, 250, 250)',
        font=dict(color='#757575', size=15, family='Helvetica')
    )

    #age
    age_1 = round(df_radar_1['Age'].value_counts()/len(df_radar_1),3)*100
    age_2 = round(df_radar_2['Age'].value_counts()/len(df_radar_2),3)*100
    trace_a_1 = go.Bar(x=age_1.index, y=age_1.values, name=drug_1, marker= dict(color='#61b8e2'))
    trace_a_2 = go.Bar(x=age_2.index, y=age_2.values, name=drug_2, marker=dict(color='#a9cbda'))
    layout=go.Layout(xaxis=dict(tickangle=0),
                     barmode='group',
                     width= 700 ,
                     height= 190,
                     margin=dict(l=10,r=10,b=10, t=10),
                     plot_bgcolor = 'rgb(250, 250, 250)',
                     paper_bgcolor = 'rgb(250, 250, 250)',
                     font = dict(color='#757575',
                                 size= 15,
                                 family='Helvetica')
    )
    barplot_1 = go.Figure(data = [trace_a_1,trace_a_2], layout=layout)

    #gender
    gender_1 = round(df_radar_1['Gender'].value_counts()/len(df_radar_1),3)*100
    gender_2 = round(df_radar_2['Gender'].value_counts()/len(df_radar_2),3)*100
    trace_g_1 = go.Bar(x=gender_1.index, y=gender_1.values, name=drug_1, marker= dict(color='#61b8e2'))
    trace_g_2 = go.Bar(x=gender_2.index, y=gender_2.values, name=drug_2, marker=dict(color='#a9cbda'))
    layout=go.Layout(xaxis=dict(tickangle=0),
                     barmode='group',
                     width= 700 ,
                     height= 190,
                     margin=dict(l=10,r=10,b=10, t=10),
                     plot_bgcolor='rgb(250, 250, 250)',
                     paper_bgcolor='rgb(250, 250, 250)',
                     font=dict(color='#757575',
                               size= 15,
                               family='Helvetica'))
    barplot_2 = go.Figure(data = [trace_g_1,trace_g_2], layout=layout)


    # education
    edu_values = ['College',"Bachelor's","Master's / Doctorate",'Professional Certificate','Highschool']
    edu_1 = round(df_radar_1['Education'].value_counts()/len(df_radar_1),3)*100
    edu_2 = round(df_radar_2['Education'].value_counts()/len(df_radar_2),3)*100
    trace_e_1 = go.Bar(x=edu_values, y=edu_1.values, name=drug_1, marker= dict(color='#61b8e2'))
    trace_e_2 = go.Bar(x=edu_values, y=edu_2.values, name=drug_2, marker=dict(color='#a9cbda'))
    layout=go.Layout(xaxis=dict(tickangle=-15),
                     barmode='group',
                     width= 700 ,
                     height= 190,
                     margin=dict(l=10,r=10,b=10, t=10),
                     plot_bgcolor='rgb(250, 250, 250)',
                     paper_bgcolor='rgb(250, 250, 250)',
                     font=dict(color='#757575',
                               size= 15,
                               family='Helvetica')
                     )
    barplot_3 = go.Figure(data = [trace_e_1,trace_e_2], layout=layout)


    data_heat = heatmap[[drug_3,'index']].sort_values(by=[drug_3])

    heatmap_1 = go.Figure(data=go.Heatmap(
        z=data_heat.values,
        y=data_heat['index'],
        x=[drug_3],
        hoverongaps=False,
        colorscale='PuBu'
    ),layout=go.Layout(width= 700 ,
                       height= 550,
                       margin=dict(l=10,r=10,b=10, t=10),
                       plot_bgcolor='rgb(250, 250, 250)',
                       paper_bgcolor='rgb(250, 250, 250)',
                       font=dict(color='#757575',
                                 size= 15,
                                 family='Helvetica')
                     ))

    df_avg = radar.loc[radar[drug_3] == 'Less than a year']
    Age_avg = df_avg['Age'].mode()
    Gender_avg = df_avg['Gender'].mode()
    Education_avg = df_avg['Education'].mode()
    Openness_avg = round(df_avg['Openness'].mean(),1)
    Extraversion_avg = round(df_avg['Extraversion'].mean(),1)
    Neuroticism_avg = round(df_avg['Neuroticism'].mean(),1)
    Sensation_Seing_avg = round(df_avg['Sensation Seing'].mean(),1)
    Impulsiveness_avg = round(df_avg['Impulsiveness'].mean(),1)
    Conscientiouness_avg = round(df_avg['Conscientiouness'].mean(),1)
    Agreeableness_avg = round(df_avg['Agreeableness'].mean(),1)



    return fig, barplot_1, barplot_2, barplot_3, heatmap_1, Age_avg, Gender_avg, Education_avg,Openness_avg,Extraversion_avg,Neuroticism_avg, Sensation_Seing_avg, Impulsiveness_avg,Conscientiouness_avg, Agreeableness_avg,


if __name__ == '__main__':
    app.run_server(debug=True)
