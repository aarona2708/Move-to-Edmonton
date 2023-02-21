import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# ==================================================================================================================== #
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# ==================================================================================================================== #
# MAIN PAGE DATAFRAMES AND DATA PREPROCESSING
# ==================================================================================================================== #
# CRIMES DATAFRAME
df_crimes = pd.read_csv('./source-files/Occurrences_Last_90_Days.csv', low_memory=False)
df_crimes_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

def occurence_group_controller(crime_stats):
    new_df = df_crimes[df_crimes.Occurrence_Category == crime_stats]

    dfg = new_df.groupby('Occurrence_Group').count().reset_index()

    return dfg["Occurrence_Group"].values.tolist()

def occurence_group_type_controller(occurence_group):
    new_df = df_crimes[df_crimes.Occurrence_Group == occurence_group]

    dfg = new_df.groupby('Occurrence_Type_Group').count().reset_index()

    return dfg["Occurrence_Type_Group"].values.tolist()

def mapped_crime_list():
    ret = {"Disorder": occurence_group_controller("Disorder"),
           "Non-Violent": occurence_group_controller("Non-Violent"),
           "Violent": occurence_group_controller("Violent"),
           "Traffic": occurence_group_controller("Traffic"),
           "Weapons": occurence_group_controller("Weapons"),
           "Drugs": occurence_group_controller("Drugs"),
           "Other": occurence_group_controller("Other")}

    return ret

crimes_list = df_crimes['Occurrence_Category'].unique()
crimes_color_map = dict(zip(crimes_list, px.colors.qualitative.G10))

# ==================================================================================================================== #
# NEIGHBOURHOOD GEOJSON FOR CHOROPLETH MAP
# set 'neighbourhood' as a global value to avoid loading same data everytime
with open('./source-files/City of Edmonton - Neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)

# ==================================================================================================================== #
# COMPARISON PAGE DATAFRAMES AND SETUP
# ==================================================================================================================== #
# colours
bg_assessedValue = "#1C6387"
fg_assessedValue = "white"
crime_file = "./source-files/Occurrences_Last_90_Days.csv"
assessment_file = "./source-files/Property_Assessment_Data__Current_Calendar_Year_.csv"
languages_file = "./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv"
def create_graph_languages(value):
    df = pd.read_csv(languages_file)
    dff = df.loc[df['Neighbourhood'] == value]
    if (len(dff.index) == 0):
        return html.Div(
            html.H3(f"No records found for Neighbourhood: {value.title()}",
                    style={'margin': '5px',
                           'padding': '50px',
                           'border-radius': '10px',
                           'text-align': 'center',
                           'color': '#636EFA',
                           'background-color': '#E5ECF6'}
                    )
        )
    else:
        headers = list(dff.columns.values)[4:14]
        values = [
            dff.iloc[0,  4], dff.iloc[0,  5], dff.iloc[0,  6], dff.iloc[0,  7],
            dff.iloc[0,  8], dff.iloc[0,  9], dff.iloc[0, 10], dff.iloc[0, 11],
            dff.iloc[0, 12], dff.iloc[0, 13],
        ]
        column_headers = headers[::-1]
        value_list = values[::-1]

        state = all([val == 0 for val in values])
        #print(f"{len(column_headers)} & {len(value_list)}")

        if (state == False):
            fig = go.Figure(
                data=[go.Bar(
                    x=value_list,
                    y=column_headers,
                    orientation="h",
                )],
                layout=go.Layout(
                    title=f"Languages per household in {value.title()}",
                    margin=dict(l=5, r=5, t=35, b=5)),
            )
            return dcc.Graph(figure=fig, config=dict({'displayModeBar': False}))
        else:
            return html.Div(
                html.H3(f"No languages listed in Neighbourhood: {value.title()}",
                        style={'margin': '5px',
                               'padding': '50px',
                               'border-radius': '10px',
                               'text-align': 'center',
                               'color': '#636EFA',
                               'background-color': '#E5ECF6'}
                        )
            )
