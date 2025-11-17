#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# Load the data
data = pd.read_csv('historical_automobile_sales.csv', low_memory=False)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "XYZAutomotives Automobile Statistics Dashboard"

# Dropdown options for statistics type
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024)]

# Layout of the dashboard
app.layout = html.Div([
    html.H1("XYZAutomotives Automobile Statistics Dashboard", style={'textAlign':'center', 'color':'#003366'}),
    
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type'
        ),
    ], style={'width':'40%', 'margin':'10px'}),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2023
        )
    ], style={'width':'20%', 'margin':'10px'}),
    
    # Division to display output graphs
    html.Div(id='output-container', className='output-container', style={'marginTop':'30px'})
])

# Callback to enable/disable year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_year_dropdown(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to update graphs based on dropdown selections
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    
    # ------------------------ Recession Period Statistics ------------------------
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Average Automobile Sales fluctuation over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation Over Recession Period")
        )
        
        # Plot 2: Average Vehicles Sold by Vehicle Type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type During Recession")
        )
        
        # Plot 3: Advertising Expenditure Share by Vehicle Type
        ad_exp = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(ad_exp, names='Vehicle_Type', values='Advertising_Expenditure',
                          title="Advertising Expenditure Share by Vehicle Type During Recession")
        )
        
        # Plot 4: Effect of Unemployment Rate on Vehicle Type and Sales
        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'], as_index=False)['Automobile_Sales'].mean()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )
        
        return [
            html.Div(className='chart-row', children=[html.Div(R_chart1, style={'flex':1}), html.Div(R_chart2, style={'flex':1})], style={'display':'flex'}),
            html.Div(className='chart-row', children=[html.Div(R_chart3, style={'flex':1}), html.Div(R_chart4, style={'flex':1})], style={'display':'flex'})
        ]
    
    # ------------------------ Yearly Statistics ------------------------
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly Automobile Sales (Line)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales")
        )
        
        # Plot 2: Total Monthly Automobile Sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )
        
        # Plot 3: Average Vehicles Sold by Vehicle Type
        avg_vehicle = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avg_vehicle, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in {input_year}')
        )
        
        # Plot 4: Total Advertisement Expenditure per Vehicle Type
        ad_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(ad_vehicle, names='Vehicle_Type', values='Advertising_Expenditure',
                          title=f'Total Advertisement Expenditure per Vehicle Type in {input_year}')
        )
        
        return [
            html.Div(className='chart-row', children=[html.Div(Y_chart1, style={'flex':1}), html.Div(Y_chart2, style={'flex':1})], style={'display':'flex'}),
            html.Div(className='chart-row', children=[html.Div(Y_chart3, style={'flex':1}), html.Div(Y_chart4, style={'flex':1})], style={'display':'flex'})
        ]
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

