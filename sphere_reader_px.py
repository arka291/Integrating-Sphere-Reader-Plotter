import base64
import datetime
import io
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
import dash
import plotly.io as pio
import statsmodels.api as sm

# --------------------------------------------------Read Data Manually---------------------------------------------------

pd.set_option("display.max_rows", None, "display.max_columns", None)
dat2 = pd.read_csv('green-OLED_Sphere_file4-1_Data1D_1.csv', delimiter='\t', index_col=False)
a = dat2.to_dict('series')

dat3 = pd.read_csv('green-OLED_Sphere_measurement1-1_Data1D_1.txt', delimiter='\t', index_col=False)
b = dat3.to_dict('series')
'''
print(
a['Sphere_evaluation_file Voltage'],
a['Sphere_evaluation_file Current']	,
a['Sphere_evaluation_file Current density'],
a['Sphere_evaluation_file PD current'],
a['Sphere_evaluation_file Radiant flux'],
a['Sphere_evaluation_file Luminous flux'],
a['Sphere_evaluation_file Irradiance'],
a['Sphere_evaluation_file Luminance'],
a['Sphere_evaluation_file EQE'],
a['Sphere_evaluation_file P_eff']
)
'''




# ---------------------------------------------Luminance vs Voltage vs Current Density-----------------------------------
'''
subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig = px.line(data_frame=a, x="Sphere_evaluation_file Voltage", y="Sphere_evaluation_file Luminance",
              log_x=True, log_y=True, template='ggplot2')
fig2 = px.line(data_frame=a, x="Sphere_evaluation_file Voltage", y="Sphere_evaluation_file Current density",
               log_x=True, log_y=True, template='ggplot2')

fig2.update_traces(yaxis="y2")
subfig.add_traces(fig.data + fig2.data)
subfig.layout.xaxis.title = "Voltage"
subfig.layout.xaxis.type = "log"
subfig.layout.yaxis2.type = "log"
subfig.layout.yaxis.type = "log"
subfig.layout.yaxis.title = "Luminance"
subfig.layout.yaxis2.title = "Current Density"
subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
subfig.show()
'''



# -------------------------------------------------------EQE vs Luminance vs P_eff--------------------------------------
'''
subfig = make_subplots(specs=[[{"secondary_y": True}]])
fig = px.line(data_frame=a, x="Sphere_evaluation_file Luminance", y="Sphere_evaluation_file EQE")
fig2 = px.line(data_frame=a, x="Sphere_evaluation_file Luminance", y="Sphere_evaluation_file P_eff")
fig2.update_traces(yaxis="y2")
subfig.add_traces(fig.data + fig2.data)
subfig.layout.template= 'gridon' #'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
subfig.layout.xaxis.title = "<b>Luminance [cd/m^2]</b>,abs."
subfig.layout.xaxis.type = "log"
subfig.layout.yaxis.title = "<b>EQE[%]</b>"
subfig.layout.yaxis.type = "linear"
subfig.layout.yaxis.range= [0,10]
subfig.layout.yaxis2.title = "<b>P_eff[lm/W]</b>"
subfig.layout.yaxis2.type = "linear"
subfig.layout.yaxis2.range= [0,10]
subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
subfig.show()
'''



#--------------------------------------------------------Wavelength vs Instensity---------------------------------------
'''
g = px.scatter(data_frame=b, x="Spectrometer Wavelength", y="Spectrometer Intensity",
                 log_x=True,log_y=True,template='plotly_dark')
g.show()
'''
########################################################################################################################
