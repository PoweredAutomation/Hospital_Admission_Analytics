import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from controls import Department, Admissiontype

# app = dash.Dash(
#     __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
# )
externalCSS=['assets/styles.css','s1.css']
app = dash.Dash(
    __name__, external_stylesheets=externalCSS
)
server = app.server

well_status_options = [
    {"label": str(Department[well_status]), "value": str(well_status)}
    for well_status in Department
]

well_type_options = [
    {"label": str(Admissiontype[well_type]), "value": str(well_type)}
    for well_type in Admissiontype
]




# Load data

df_hosp=pd.read_csv(r"data\final.csv")
df_hosp=df_hosp.head(100000)



# df_hosp=df_hosp[~df_hosp.Avg_Age.isin(['01-11-2020'])]
# df_hosp=df_hosp[~df_hosp.Stay.isin(['01-11-2020'])]


# Create global chart template
# Create app layout
app.layout = html.Div(

    [

                            html.H3(
                            "Hospital Admission Anlytics Dashboard",
                            style={"font-family": "ui-sans-serif", "font-size":"40px","margin-bottom": "0px", "text-align": "center","display": "block","margin-top": "0px","margin-left": "3%"},
                            ),

                            # html.Header(
                            # "Explore hospital Patient age, Patient Count, and Available Rooms,Available Rooms. Click on the heatmap to visualize patient experience at different time points.",
                            # style={"margin-bottom": "0px", "text-align": "center","display": "block","margin-top": "0px"},
                            # ),
        # empty Div to trigger javascript file for graph resizing
        html.Div(
            id="header",
            className="row flex-display",
            style={"margin-bottom": "30px"},
        ),
        html.Div(
            [
                html.Div(
                    [

                        html.P(
                            "Filter by Age Range:",
                            className="control_label",style={"font-weight":"bold"},
                        ),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=df_hosp['Avg_Age'].min(),
                            max=df_hosp['Avg_Age'].max(),
                            value=[5, 96],
                            marks={str(year): str(year) for year in df_hosp['Avg_Age'].unique()},

                            className="dcc_control",
                        ),
                        html.P("Filter by Hospital Region:", className="control_label",style={"font-weight":"bold"}),
                        dcc.RadioItems(
                            id="region",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "North ", "value": "North"},
                                {"label": "South ", "value": "South"},
                                {"label": "West ", "value": "West"}

                            ],
                            value="all",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        html.P("Select Department:", className="control_label",style={"font-weight":"bold"}),
                        dcc.Dropdown(
                            id="theropy_update",
                            multi=True,
                            className="dcc_control",
                        ),
                        html.P("Select Type of Admission:", className="control_label",style={"font-weight":"bold"}),
                        dcc.Dropdown(
                            id="admissiontype",
                            multi=True,
                            className="dcc_control",
                        ),
                    ],

                    className="pretty_container four columns",
                    id="cross-filter-options",

                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="patinetcount"), html.P("Patient Count")],
                                    id="pcount",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="avrooms"), html.P("Available Rooms")],
                                    id="arooms",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="avgdeposit"), html.P("Average Deposit")],
                                    id="adeposit",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="avgsalary"), html.P("Average Stay")],
                                    id="aage",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6( id="averageage" ), html.P( "Average Age" )],
                                    id="aage1",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),

                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                ### Regression graph



                html.Div([
                    html.H5( "Region wise Analysis:" ),
                    dcc.Graph(id="main_graph",style={"height": "517px"})],
                    className="pretty_container six columns",
                ),
                html.Div( [
                    html.H6("Charges vs Payments:",style={ "line-height": "1.2"}),
                    dcc.Dropdown(
                        id='x-column',
                        options=[{"label": "Total Charges", "value": "charges"},
                                {"label": "Insurance Payment Received ", "value": "inspayment"},
                                {"label": "Expected collection ", "value": "NetExpectedCollection"},
                                {"label": "Admission deposit ", "value": "Admission_Deposit"}],
                        value='charges',
                    ),
                    dcc.RadioItems(
                        id='x-type',
                        options=[{'label': i, 'value': i} for i in ['Scatter', 'Line']],
                        value='Scatter',
                        labelStyle={'display': 'inline-block'}
                    ),
                    # html.P('Y Axis'),
                    dcc.Dropdown(
                        id='y-column',
                        options=[{"label": "Total Charges", "value": "charges"},
                                 {"label": "Insurance Payment Received", "value": "inspayment"},
                                 {"label": "Expected collection", "value": "NetExpectedCollection"},
                                 {"label": "Admission deposit ", "value": "Admission_Deposit"}],
                        value='inspayment',
                    ),
                    dcc.Graph( id='indicator-linear' )
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'} ),




            ] ,
        ),

    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback(
    [
        Output( "patinetcount", "children" ),
                Output("avrooms", "children"),
                Output("avgdeposit", "children"),
                Output("avgsalary", "children"),
                Output("averageage", "children")

        ,
    ],
    [Input("region", "value"),
     Input('admissiontype','value'),
    Input("year_slider", "value"),
     Input("theropy_update", "value")],


)
def update_text(region,admissiontype,year_slider,theropy_update):
    dff_text = df_hosp[(df_hosp["Avg_Age"] > (year_slider[0]))
                        & (df_hosp["Avg_Age"] < (year_slider[1]))]

    if region=='all':
        print(theropy_update)
        print(admissiontype)
        if theropy_update is not None and admissiontype is not None:
            dff_text = dff_text[dff_text["Department"].isin( theropy_update )]

            # admissiontype = [li['label'] for li in admissiontype]
            dff_text = dff_text[dff_text["Type of Admission"].isin(admissiontype)]
            return dff_text['Stay'].count(), dff_text['Available Extra Rooms in Hospital'].sum() , \
                   round(dff_text['Admission_Deposit'].mean()) , dff_text['Stay'].mode(),round(dff_text['Avg_Age'].mean())
        else:
            return  dff_text['Stay'].count(), dff_text['Available Extra Rooms in Hospital'].sum() , \
                   round(dff_text['Admission_Deposit'].mean()) , dff_text['Stay'].mode(),round(dff_text['Avg_Age'].mean())
    else:
        if theropy_update is not None and admissiontype is not None:
            dff_text = df_hosp[df_hosp["Hospital_region_code"]==region]
            # theropy_list = [li['label'] for li in theropy_update]
            # print( theropy_list )

            dff_text = dff_text[dff_text["Department"].isin( theropy_update )]
            dff_text = dff_text[dff_text["Type of Admission"].isin( admissiontype )]
            # admissiontype = [li['label'] for li in admissiontype]
            # dff_text = dff_text[dff_text["Type of Admission"].isin( admissiontype )]
            return dff_text['Stay'].count(), dff_text['Available Extra Rooms in Hospital'].sum(), \
                   round( dff_text['Admission_Deposit'].mean() ), dff_text['Stay'].mode(),round(dff_text['Avg_Age'].mean())
        else:
            return dff_text['Stay'].count(), dff_text['Available Extra Rooms in Hospital'].sum(), \
                   round( dff_text['Admission_Deposit'].mean() ), dff_text['Stay'].mode(), round(
                dff_text['Avg_Age'].mean() )


@app.callback(

    Output('theropy_update','options'),
    [Input("year_slider", "value"),
     Input("region", "value")])

def update_theropy(year_slider,region):
    # dff = df_hosp[
    #     df_hosp["Department"].isin(well_statuses)
    #     & df_hosp["Type of Admission"].isin(well_types)
    #     & (df_hosp["Avg_Age"] > (year_slider[0], 1, 1))
    #     & (df_hosp["Avg_Age"] < (year_slider[1], 1, 1))
    # ]
    # #print(year_slider)
    # #print(region)
    dff=df_hosp[(df_hosp["Avg_Age"] > (year_slider[0]))
        & (df_hosp["Avg_Age"] < (year_slider[1]))]
    # #print(dff)
    # #print(dff.columns)

    if region=='all':

        testdat = dff["Department"].value_counts().rename_axis( 'cols' ).reset_index( name='cols1' )
        dept_dict = testdat['cols'].to_dict()

        well_status_selected = [
            {"label": str( dept_dict[well_status] ), "value": str( dept_dict[well_status] )}for well_status in dept_dict]


        return well_status_selected

    else:
        print(region)
        dff = dff[dff["Hospital_region_code"]==region]
        print(dff)
        testdat=dff["Department"].value_counts().rename_axis('cols').reset_index(name='cols1')
        dept_dict=testdat['cols'].to_dict()
        print(dept_dict)

        well_status_selected = [
            {"label": str( dept_dict[well_status] ), "value": str( dept_dict[well_status] )} for well_status in
            dept_dict]

        return well_status_selected

@app.callback(

    Output('admissiontype','options'),
    [Input("year_slider", "value"),
     Input("region", "value"),
     Input("theropy_update", "options")])

def update_admissiontype(year_slider,region,theropy_update):

    dff=df_hosp[(df_hosp["Avg_Age"] > (year_slider[0]))
        & (df_hosp["Avg_Age"] < (year_slider[1]))]
    if region=='all':
        # #print('thropy',theropy_update['label'])
        theropy_list = [li['label'] for li in theropy_update]
        #print(theropy_list)

        dff = dff[dff["Department"].isin( theropy_list )]
        #print(dff.head())
        dff = dff["Type of Admission"].value_counts().rename_axis( 'cols' ).reset_index( name='cols1' )
        # typead = dff['cols'].to_list()
        dept_dict = dff['cols'].to_dict()
        well_type_options = [
            {"label": str( dept_dict[well_type] ), "value": str( dept_dict[well_type] )}

            for well_type in dept_dict]
        #print( well_type_options )
        return well_type_options

    else:
        #print(region)
        dff = dff[dff["Hospital_region_code"].isin([region])]
        theropy_list = [li['label'] for li in theropy_update]
        #print( theropy_list )
        dff = dff[dff["Department"].isin( theropy_list )]
        dff = dff["Type of Admission"].value_counts().rename_axis( 'cols' ).reset_index( name='cols1' )
        # typead = dff['cols'].to_list()
        dept_dict = dff['cols'].to_dict()

        well_type_options = [
            {"label": str( dept_dict[well_type] ), "value": str( dept_dict[well_type] )}

            for well_type in dept_dict]
        #print( well_type_options )
        return well_type_options


@app.callback(
    Output("count_graph", "figure"),
    [Input("region", "value"),
     Input("theropy_update", "value"),
     Input("admissiontype", "value"),
     Input("year_slider", "value")])



def update_graph(region,theropy,admissiontype,year_slider):
    dff_graph = df_hosp[(df_hosp["Avg_Age"] > (year_slider[0]))
                  & (df_hosp["Avg_Age"] < (year_slider[1]))]
    # print(dff_graph)

    if region=='all':
        if theropy is not None and admissiontype is not None:
        # if theropy is not None an:
            print(theropy)

            dff_text = dff_graph[dff_graph["Department"].isin( theropy )]
            # print(dff_text)

            # admissiontype = [li['label'] for li in admissiontype]
            dff_text = dff_text[dff_text["Type of Admission"].isin(admissiontype)]
            fig = px.histogram( dff_text, x='Age' ,nbins=20,color='Age')
            return fig
        else:
            # print( dff_graph )
            fig = px.histogram( dff_graph, x='Age', nbins=20, color='Age' )
            return fig


    else:
        # dff_graph = dff_graph[dff_graph["Hospital_region_code"] == region]
        # theropy_list = [li['label'] for li in theropy]
        # dff_graph = dff_graph[dff_graph["Department"].isin( theropy_list )]
        # admissiontype = [li['label'] for li in admissiontype]
        # dff_graph = dff_graph[dff_graph["Type of Admission"].isin( admissiontype )]
        if theropy is not None and admissiontype is not None:
            dff_text = dff_graph[dff_graph["Department"].isin( theropy )]

            # admissiontype = [li['label'] for li in admissiontype]
            dff_text = dff_text[dff_text["Type of Admission"].isin(admissiontype)]
            fig = px.histogram( dff_text, x='Age' ,nbins=20,color='Age')
            return fig
        else:
            fig = px.histogram( dff_graph, x='Age', nbins=20, color='Age' )
            return fig









@app.callback(
    Output("main_graph", "figure"),
    [Input("region","value")])

def update_sunburst(region):
    fig = px.sunburst( df_hosp, path=['Hospital_region_code', 'City_Code_Hospital', 'Department','Severity of Illness'], values='charges', color='City_Code_Hospital' )
    return fig




@app.callback(
    Output("indicator-linear", "figure"),
    [Input("x-column","value"),
     Input("y-column","value"),
     Input("x-type","value")],)

def update_linear(xcol,ycol,xtype):
    print(xcol)
    print(ycol)

    if xtype=='Scatter':
        fig = px.scatter( df_hosp,x=df_hosp[xcol],y=df_hosp[ycol],trendline='ols',color='Hospital_region_code')

        return fig
    elif xtype=='Line':

        new = df_hosp.groupby( str(xcol) )[str(ycol)].sum().reset_index( str(xcol) )
        fig = px.line( new, x=new[xcol], y=new[ycol] )


        return fig


if __name__ == "__main__":
    app.run_server(debug=True,port=2050)
