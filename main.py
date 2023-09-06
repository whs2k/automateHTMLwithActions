import pandas as pd
import datetime
import os

import traceback
import plotly.graph_objs as go
import plotly.offline as pyo


fn_outputInput_html = 'index.html'
def init_index():
    '''

    :return: outputs a file in templates folder called index.html
    '''
    d_precise = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d = datetime.datetime.now().strftime("%Y-%m-%d")
    df =pd.read_csv('AMZN.csv')

    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)  # df.Date.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['High'],
        name="High",
        line_color='deepskyblue',
        opacity=0.8))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Low'],
        name="Low",
        line_color='dimgray',
        opacity=0.8))
    fig.update_layout(# xaxis_range=['2016-07-01','2016-12-31'],
        title_text="AMZN")


    amzn_plotDiv= pyo.plot(figure_or_data=fig,
                                 config={"displayModeBar": False},
                                 show_link=False,
                                 include_plotlyjs=False,
                                 output_type='div') \
                         .replace('height: 100%; width: 100%', 'height: 50%; width: 100%')

    df_html = df.to_html() \
       .replace('<table border="1" class="dataframe">','<table class="table table-hover table-condensed table-striped">')
    for col in df.columns.tolist():
        df_html = df_html.replace('<th>'+col+'</th>','<th data-sortable="true" data-filter-control="input">'+col+'</th>')

    bootstrap_header = r'''
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.9.1/extensions/filter-control/bootstrap-table-filter-control.js"></script>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.css" rel="stylesheet"/>
    <style>body{ margin:0 100; background:whitesmoke; }</style>
    '''

    html_string = '''
     <html>
         <head>
              ''' + bootstrap_header + '''
         </head>
         <body>
             <h1>This is a dashboard made on <small><kbd>__input_date__</kbd></small>!</h1>
             <br>
             <p><kbd>__input_date_precise__</kbd> to be precise</p>
    <h2>Section 1: Plotly Data!</h2>
             <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo1">Click Me For Data</button>
             <div id='demo1' class="collapse">
              ''' + amzn_plotDiv + '''
              <p>ADDITIONAL TEXT HERE</p>
          </div>
             <br>
    <h2>Section 2: Pandas Data!</h2>
             <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo2">Click Me For Data</button>
             <div id='demo2' class="collapse">
              ''' + df_html + '''
              <p>ADDITIONAL TEXT HERE</p>
          </div>
             <br>
             <br>
     </body>
     </html>'''
    html_string = html_string.replace('__input_date__', str(d)).replace('__input_date_precise__',str(d_precise)).encode('utf-8', errors='replace').decode('utf-8', errors='replace')

    with open(fn_outputInput_html, 'w') as f:
        f.write(html_string)

if __name__ == '__main__':
    init_index()
    