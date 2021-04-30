import pandas as pd
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
# import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# Multi-dropdown options

import plotly.io as pio
pio.renderers.default = "browser"



df=pd.read_csv(r"data\OSD01.csv")
df['closedate'] = pd.DatetimeIndex(df['closedate'])

df_monthly = df.groupby([pd.Grouper(key='closedate', freq='M')])['NC'].sum().reset_index().sort_values(
            'closedate')
print(df_monthly)
