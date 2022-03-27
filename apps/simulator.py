import base64
import datetime
import io
from app import app
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd

layout = html.H1('SRI', style={"textAlign": "center"})