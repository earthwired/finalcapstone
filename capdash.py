# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload]
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If 'ALL' sites are selected, use the entire dataframe
        site_data = spacex_df
        title = 'Success Count for All Sites'
    else:
        # Filter the dataframe based on the selected launch site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Success Count for {selected_site}'
    
    # Calculate success counts
    success_counts = site_data['class'].value_counts()
    
    # Create a pie chart
    fig2 = px.pie(names=['Success', 'Failure'], values=success_counts, title=title)
    
    return fig2

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If 'ALL' sites are selected, use the entire dataframe
        site_data = spacex_df
    else:
        # Filter the dataframe based on the selected launch site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter data based on the selected payload range
    site_data = site_data[(site_data['Payload Mass (kg)'] >= payload_range[0]) & 
                         (site_data['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create a scatter plot
    fig = px.scatter(site_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title=f'Scatter Plot of Payload vs. Launch Outcome for {selected_site}')
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()