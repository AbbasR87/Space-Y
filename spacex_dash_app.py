## dit is exact dezelfde code als in IBM skills network cloud IDE. Ik heb enkel de link naar de file gezet ipv als het reeds was gedownload
# hier lijken de figuren wel zeer klein terwijl bij de skilss network cloud IDE van IBM het groot en zichtbaar is
# dus ik denk dat we de "style={} moeten aanpassen"

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',
                                                options=[{'label': 'All Sites', 'value': 'All'},{'label': 'CCAFS LC-40','value':'CCAFS LC-40'},
                                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},{'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                                value='All',
                                                placeholder='Please select a Launch Site',
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,
                                marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                value=[spacex_df['Payload Mass (kg)'].min(),spacex_df['Payload Mass (kg)'].max()]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site == 'All':
        successful_launches=spacex_df[spacex_df['class']==1]
        all_sites=successful_launches.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(all_sites, values='class', 
        names='Launch Site', 
        title='Succesrate for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        select_site=filtered_df.groupby('class')['Launch Site'].count().reset_index()
        fig=px.pie(select_site,values='Launch Site',
        names='class',
        title='Succes ratio for {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
             Input(component_id='payload-slider',component_property='value')],
                )

def get_scatter(entered_site,payload_range):
    payload_df=spacex_df[(spacex_df['Payload Mass (kg)']>=payload_range[0]) & (spacex_df['Payload Mass (kg)']<= payload_range[1])]
    if entered_site=='All':
        fig=px.scatter(payload_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
        title='Launch Outcome vs. Payload mass with booster version',
        labels={'class':'Launch Outcome','Payload Mass (kg)':'Payload Mass in kg'})
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
        title='Launch Outcome vs. Payload mass with differen booster version for {}'.format(entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()