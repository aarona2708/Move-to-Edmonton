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


# df_crimes_property = df_crimes[(df_crimes['Occurrence_Group'] == 'Property')]
# print(df_crimes_property)

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
