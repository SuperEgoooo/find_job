# -*- coding: utf-8 -*-

# date: 2024/2/7 16:52
# filename: canada_vehicle.py
# writer: cao ke

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# 年限列表
year_list = [i for i in range(1980, 2024, 1)]
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard"),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        style={
            "width": "80%",
            "padding": "3px",
            "font-size": "20px",
            "text-align-last": "center"
        }
    )),
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={"display": "flex"}),
    ])
])


@app.callback(
    Output(component_id='select-year', component_property='value'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='select-year', component_property='value'),
        Input(component_id='dropdown-statistics', component_property='value')
    ]
)
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # 折线图
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        r_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period"
                           ))

        # 折线图
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        r_chart2 = dcc.Graph(figure=px.line(average_sales,
                                            x='Vehicle_Type',
                                            y='Automobile_Sales',
                                            title="Average Number of Vehicles Sold by Vehicle Type "
                                            ))

        # 饼图
        recession_data['Total_Expenditure'] = recession_data['Automobile_Sales'] * recession_data['Price']
        total_expenditure = recession_data.groupby('Vehicle_Type')['Total_Expenditure'].sum().reset_index()
        r_chart3 = dcc.Graph(figure=px.pie(total_expenditure,
                                           names="Vehicle_Type",
                                           values="Total_Expenditure",
                                           title="Total Expenditure Share By Vehicle Type"
                                           ))

        # 条形图
        r_chart4 = dcc.Graph(figure=px.bar(
            recession_data,
            x='unemployment_rate',
            y='Automobile_Sales',
            color="Vehicle_Type",
            title="Total Expenditure in Diffierent Unemployment Rate Share By Different Vehicle Type"
        ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=r_chart1), html.Div(children=r_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=r_chart3), html.Div(children=r_chart4)])
        ]

    # 按年筛选
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales"
            )
        )

        # 月度线图
        yas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        y_chart2 = dcc.Graph(
            figure=px.line(
                yas,
                x='Month',
                y='Automobile_Sales',
                title="Yearly Automobile Sales"
            )
        )

        # 条形图
        avr_vdata = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata,
            x='Month',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
        ))

        # 饼图
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            names="Vehicle_Type",
            values="Advertising_Expenditure",
            title='Advertising Expenditure Sold by Vehicle Type in the year {}'.format(input_year)
        ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=y_chart1), html.Div(children=y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=y_chart3), html.Div(children=y_chart4)])
        ]

    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
