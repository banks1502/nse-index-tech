from datetime import date
import plotly.graph_objs as go
from plotly import subplots
import numpy as np
import pandas as pd

######################## FOR GRAPHS  ########################
def plot_scatter(filtered_df,primary_y,sec_y = []):
    #print(filtered_df.index,filtered_df[primary_y],filtered_df[sec_y])
    graph_primary = go.Scatter(
      x=filtered_df.index, 
      y=filtered_df[primary_y],
      name=primary_y ,textposition='bottom center',
      marker= {'color':'green' if primary_y == 'ClosingIndexValue' else 'blue'},
      mode=  'lines',
      fill = 'tozeroy' if primary_y == 'ClosingIndexValue' else None,
      opacity=0.6
    )

    fig = subplots.make_subplots(
      rows=1, 
      cols=1, 
      specs=[[{"secondary_y": True}]])

    fig.add_trace(graph_primary, secondary_y=False,)			
    
    if(isinstance(sec_y, list)):
        for sec_axis in sec_y:
            graph_sec = go.Scatter(
                x=filtered_df.index, 
                y=filtered_df[sec_axis],
                name=sec_axis ,textposition='bottom center',
                marker= {'color': np.random.choice(range(256), size=3)},
                opacity=0.4
                )
            fig.add_trace(graph_sec, secondary_y=True,)	

    # Set x-axis title
    fig.update_xaxes(title_text=filtered_df.index.name)

    # Set y-axes titles
    fig.update_yaxes(title_text=primary_y, secondary_y=False,hoverformat=".2f",color ='green' if primary_y == 'ClosingIndexValue' else 'blue')
    fig.update_yaxes(title_text=' / '.join(sec_y) ,secondary_y=True,hoverformat=".2f",color="black")
    fig.update_layout(
        title_text = primary_y + " - " + " - ".join(sec_y) + " Chart" ,
        title_xanchor ='left',
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(250,250,250,1)',
        hovermode = 'x',
        legend=go.layout.Legend(
            x=1,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor='rgba(250,250,250,1)',
            bordercolor='rgba(200,200,200,1)',
            borderwidth=2
        ),
        #yaxis ={"linecolor":"green"},
        xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 12, 'label': '1Y', 'step': 'month', 'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': False}, 'type': 'date'}
    )
    return fig
    
def plot_vol(filtered_df,IndexName):
    trace1 = []
    trace2 = []
    trace1.append(
        go.Bar(x=filtered_df.index,
               y=filtered_df['Volume'],
               opacity=0.7,name='Volume ')
    )

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
        'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            hovermode = 'x',
            height=600,title="Market Volume for " + IndexName + " Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 12, 'label': '1Y', 'step': 'month', 'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': False}, 'type': 'date'},yaxis={"title":"Transactions Volume"} ,   paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')}
    return figure

def plot_technical(stock, dff, indicators):
    trace1 = {'x':dff['Date'],
              'open':dff['Open'],
              'low':dff['Low'],
              'high':dff['High'],
              'close':dff['Close'],
              'increasing':{'line': {'color': '#00CC94'}},
              'decreasing':{'line': {'color': '#F50030'}},
              'name': stock.split('.')[0],
              'yaxis':'y1',
              'type':'candlestick',
              'showlegend':False
              }

    if 'Volume' in indicators:
        trace2 = {'x':dff['Date'],
                  'y':dff['Volume'],
                  'name':'Volume',
                  'yaxis':'y2',
                  'type':'bar'}
    else:
        trace2 = {}

    if 'Bollinger' in indicators:
        MA = dff['Close'].rolling(window=20).mean()
        STD = dff['Close'].rolling(window=20).std()
        upper_band = MA + (STD*2)
        lower_band = MA - (STD*2)
        middle_band = MA
        trace3 = {'x':dff['Date'],
                  'y':upper_band,
                  'line':{'width':1},
                  'hoverinfo':'none',
                  'legendgroup':'Bollinger Bands',
                  'marker':{'color':'green'},
                  'name':'Bollinger Bands',
                  'mode':'lines',
                  'type':'scatter',
                  'yaxis':'y1'}
        trace4 = {'x':dff['Date'],
                  'y':lower_band,
                  'line': {'width':1},
                  'hoverinfo':'none',
                  'legendgroup':'Bollinger Bands',
                  'showlegend': False,
                  'marker':{'color':'green'},
                  'mode':'lines',
                  'type':'scatter',
                  'yaxis':'y1'}
        trace5 = {'x':dff['Date'],
                  'y':middle_band,
                  'line': {'width':1},
                  'hoverinfo':'none',
                  'legendgroup':'Bollinger Bands',
                  'showlegend': False,
                  'marker':{'color':'yellow'},
                  'mode':'lines',
                  'type':'scatter',
                  'yaxis':'y1'}
    else:
        trace3 = {}
        trace4 = {}
        trace5 = {}

    if 'Stoch' in indicators:
        L14 = dff['Low'].rolling(window=14).min()
        H14 = dff['High'].rolling(window=14).max()
        dff['%k'] = 100*((dff['Close'] - L14) / (H14 - L14))
        dff['%d'] = dff['%k'].rolling(window=3).mean()
        trace6 = {'x':dff['Date'],
                  'y':dff['%k'],
                  'line': {'width': 1},
                  'legendgroup':'Stochastic Oscilator',
                  'name':'Stochastic %k',
                  'mode':'lines',
                  'type':'scatter',
                  'yaxis':'y3'}
        trace7 = {'x':dff['Date'],
                  'y':dff['%d'],
                  'line': {'width': 1},
                  'legendgroup':'Stochastic Oscilator',
                  'name':'Stochastic %d',
                  'showlegend':False,
                  'mode':'lines',
                  'type':'scatter',
                  'yaxis':'y3'}
    else:
        trace6 = {}
        trace7 = {}

    if 'RSI' in indicators:
        delta = dff['Close'].diff()
        up_days = delta.copy()
        up_days[delta<=0] = 0.0
        down_days = abs(delta.copy())
        down_days[delta>0] = 0.0
        RS_up = up_days.rolling(window=14).mean()
        RS_down = down_days.rolling(window=14).mean()
        dff['RSI']= 100-100/(1+RS_up/RS_down)
        trace8 = {'x':dff['Date'],
                  'y':dff['RSI'],
                  'line': {'width': 1},
                  'legendgroup':'RSI',
                  'name':'RSI',
                  'mode':'lines',
                  'type':'scatter',
                  'marker':{'color':'black'},
                  'yaxis':'y3'}
    else:
        trace8 = {}

    dat = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]
    layout = go.Layout(
        title='Chart for ' + stock.split('.')[0],
        xaxis={'rangeslider':{'visible':False},
               'title':"Date",
               'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                  {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                  {'count': 12, 'label': '1Y', 'step': 'month', 'stepmode': 'backward'},
                                                  {'step': 'all'}]),
                                }},
        hovermode = 'x',
        legend={'x':1,
                'y':1,
                'bgcolor':'#E2E2E2',
                'bordercolor':'#FFFFFF',
                'borderwidth':2,
                'font':{'family':'sans-serif',
                        'size':8,
                        'color':'#000'}},
        yaxis={'title': 'Stock price',
               'domain': [0.6, 1],
               'side': 'left',
               #'overlaying': 'y2',
               'showticklabels': True},
        yaxis2={'side': 'left',
                'domain': [0.3, 0.55],
                'showticklabels': True,
                'showgrid': False},
        yaxis3={'side':'right',
                'domain':[0, 0.3],
                'showticklabels':True}
    )

    return go.Figure(data=dat, layout=layout)

def get_markdown(context):
    if context =='banner':
        return "Thanks for landing at Nifty Chart website. Honestly, I have NO idea how much to ask you for, but is a gift of ₹ 50 something you'd be able to consider? Click on below Rupee (₹) icon to donate"
    if context =='Contact Us':
        return '''
        **Liked the website?** We would love to hear from you. Our goal is to provide free and easy access of data for better investment decisions. Email us your comments, questions, feedback, suggestions.
        Below are the key details of this initiative  
        *  Data on the website is updated every weekend on Saturday.
        *  We provide free access to  Nifty50 index PE Ratio, PB Ratio and Dividend Yield and other sectoral Nifty indices (e.g. Auto, Bank, FMCG, Midcap, Next50, IT, Pharma, FMCG etc).
        '''
    if context =='Volume':
        return '`Volume:` A rising market should see rising volume. Buyers require increasing numbers and enthusiasm in order to keep pushing prices higher. Increasing price and decreasing volume show lack of interest, and this is a warning of a potential reversal. Simple fact is that a price drop (or rise) on little volume is not a strong signal. A price drop (or rise) on large volume is a stronger signal that something in the stock has fundamentally changed.'
    if context =='Bollinger':
        return '`Bollinger Bands®` are a highly popular technique. The closer the prices move to the upper band, the more overbought the market is, and the closer the prices move to the lower band, the market is more oversold.'
    if context == 'Stoch':
        return '`Stochastic oscillator`  traditionally says, readings over 80 are considered in the overbought range i.e time to sell, and readings under 20 are considered oversold i.e time to buy.'
    if context == 'RSI':
        return '`Relative Strength Index` interpretation and usage  are that values of 70 or above indicate that a security is becoming overbought or overvalued i.e time to sell . An RSI reading of 30 or below indicates an oversold or undervalued condition i.e time to buy.'
    if context =='Nifty 50-graph':
        return '''
            The `NIFTY 50` is a well diversified 50 stock index and it represent important sectors of the economy accounting for 13 sectors of the economy. It is used for a variety of purposes such as benchmarking fund portfolios, index based derivatives and index funds.It is computed based on free float methodology
        '''
    if context =='Nifty 50-graph1':
        return '''
            Nifty PE ratio measures the average PE ratio of the Nifty 50 companies covered by the Nifty Index. If P/E is 15, it means Nifty is 15 times its earnings.

            Nifty PE | Returns(3 yrs) | Sentiment
            ---------|----------------|----------
            Below 15 | more than 100% | Oversold
            15 - 20  | 30% - 5%       | Neutral
            Above 20 | less than 30%  | Overbought
            
            
            The market quickly bounces back from the **oversold** region because intelligent investors start buying stocks looking to snatch up bargains and they do the exact opposite when Nifty P/E is in the **overbought** region.
            Nifty is considered to be in oversold range when **"Nifty P/B"** ratio is below 2.5 and it's considered to be in overbought range when Nifty P/B is near 4. **"Dividend yield"** generally bounces between 1 and 1.5. A dividend yield above 1.5 means its a good time to buy.
            '''
    if context =='Nifty Next 50-graph':
        return 'The `NIFTY Next 50 Index` represents 50 companies from NIFTY 100 after excluding the NIFTY 50 companies.The NIFTY Next 50 Index represents about 12% of the free float market capitalization of the stocks listed on NSE as on March 31, 2016.'
    if context ==' Nifty 100-graph':
        return '`NIFTY 100` is a diversified 100 stock index representing major sectors of the economy. NIFTY 100 represents top 100 companies based on full market capitalisation from NIFTY 500. This index intends to measure the performance of large market capitalisation companies. The NIFTY 100 tracks the behavior of combined portfolio of two indices viz. NIFTY 50 and NIFTY Next 50.'
    if context =='Nifty 200-graph':
        return 'The `NIFTY 200` Index is designed to reflect the behaviour and performance of large and mid market capitalization companies . NIFTY 200 includes all companies forming part of NIFTY 100 and NIFTY Full Midcap 100 index.'
    if context == 'Nifty Midcap 50-graph':
        return '`NIFTY Midcap 50` index represent top 50 companies based on full market capitalisation from NIFTY Midcap 150 index and on which derivative contracts are available on National Stock Exchange (NSE).'
    if context =='NIFTY Midcap 100-graph':
        return 'The `NIFTY Midcap 100` Index captures the movement of the midcap segment of the market. The NIFTY Midcap 100 Index comprises 100 tradable stocks listed on the National Stock Exchange (NSE).'
    if context =='NIFTY Smallcap 100-graph':
        return 'The `NIFTY Smallcap 100` Index reflects the behaviour and performance of the small cap segment of the financial market.'
    if context =='Nifty Auto-graph':
        return 'The `NIFTY Auto` Index is designed to reflect the behaviour and performance of the Indian automobiles sector.'
    if context =='Nifty Bank-graph':
        return '`NIFTY Bank` Index is comprised of the most liquid and large capitalised Indian Banking stocks. It provides investors and market intermediaries with a benchmark that captures the capital market performance of Indian Banks.'
    if context =='Nifty Financial Services-graph':
        return 'The `Nifty Financial Services` Index is designed to reflect the behaviour and performance of the Indian financial market which includes banks, financial institutions, housing finance, insurance companies and other financial services companies.'
    if context =='Nifty FMCG-graph':
        return 'The `NIFTY FMCG` Index is designed to reflect the behavior of FMCGs Indian companies from (Fast Moving Consumer Goods) (FMCG) sector. It incudes companies that deals with those goods and products, which are non-durable, mass consumption products and available off the shelf.'
    if context =='Nifty IT-graph':
        return 'Information Technology (IT) industry has played a major role in the Indian economy. In order to have a good benchmark of the Indian IT sector.NIFTY IT provides investors and market intermediaries with an appropriate benchmark that captures the performance of the IT segment of the market in India.'
    if context =='Nifty Media-graph':
        return 'The `NIFTY Media` Index is designed to reflect the behavior and performance of the Media & Entertainment sector including printing and publishing in India.'
    if context =='Nifty Metal-graph':
        return 'The `NIFTY Metal` Index is designed to reflect the behavior and performance of the metals sector including mining in India.'
    if context =='Nifty MNC-graph':
        return 'The `NIFTY MNC` Index comprises Of companies in which the foreign shareholding is over 50% and / or the management control is vested in the foreign company.'
    if context =='Nifty Pharma-graph':
        return 'The `NIFTY Pharma` Index is designed to reflect the behavior and performance of the pharmaceutical sector in India.'
    if context =='Nifty PSU Bank-graph':
        return 'The NIFTY PSU Bank Index is designed to reflect the performance of the public sector banks.'
    if context =='Nifty Realty-graph':
        return 'The `NIFTY Realty` Index is designed to reflect the performance of real estate companies that are primarily engaged into construction of residential and commercial properties.'

    return ' '
    


