import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

#=================================================================================================================

crime_file = "./source-files/Occurrences_Last_90_Days.csv"
assessment_file = "./source-files/Property_Assessment_Data__Current_Calendar_Year_.csv"
languages_file = "./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv"

# create Pandas df and lists here
df_crimes = pd.read_csv(crime_file)
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

df_languages = pd.read_csv(languages_file)
column_header_lan = list(df_languages.columns.values)

df_assessments = pd.read_csv(assessment_file)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
neighbourhood_list = df_assessments['Neighbourhood'].unique()

df_neighbourhood_average = df_assessments.groupby(['Neighbourhood'], as_index=False)[['Assessed Value']].mean().round(0)
min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list = []

for item in df_category.values.tolist():
    crimes_list.append(item[0])


#===================================================================================================================

def create_graph_languages(value):
    df = pd.read_csv(languages_file)
    dff = df.loc[df['Neighbourhood Name'] == value]
    headers = list(dff.columns.values)[4:14]
    values = [
        dff.iloc[0,  4], dff.iloc[0,  5], dff.iloc[0,  6], dff.iloc[0,  7],
        dff.iloc[0,  8], dff.iloc[0,  9], dff.iloc[0, 10], dff.iloc[0, 11],
        dff.iloc[0, 12], dff.iloc[0, 13],
    ]
    column_headers = headers[::-1]
    value_list = values[::-1]
    #print(f"{len(column_headers)} & {len(value_list)}")

    fig = go.Figure(
        data=[go.Bar(
            x=value_list,
            y=column_headers,
            orientation="h",)
        ],
        layout=go.Layout(margin=dict(l=5, r=5, t=35, b=5)),
    )
    config = dict({'displayModeBar': False})

    return fig

def create_average_assessment(value):
    residential = "RESIDENTIAL"
    df = pd.read_csv(assessment_file)
    dff = df.query("`Neighbourhood`==@value & `Assessment Class % 1`==100 & `Assessment Class 1`==@residential")["Assessed Value"]
    average = dff.mean()
    currency_string = "${:,.2f}".format(average)
    return currency_string

#===============================================================================================

# colours
bg_assessedValue = "#1C6387"
fg_assessedValue = "white"

#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)