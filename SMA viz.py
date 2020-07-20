from datetime import datetime
import backtrader as bt
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly import tools
import time 


# from strategies import *

cerebro = bt.Cerebro(optreturn=False)



class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=50   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

 #Set data parameters and add to Cerebro
data = bt.feeds.YahooFinanceData(
dataname='AAPL',
fromdate=datetime(2019, 1, 1),
todate=datetime(2020, 12, 25))
#settings for out-of-sample data
#fromdate=datetime.datetime(2018, 1, 1),
#todate=datetime.datetime(2019, 12, 25))
cerebro.adddata(data)

#Add strategy to Cerebro
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
cerebro.optstrategy(SmaCross, pfast=range(5, 20), pslow=range(50, 100))  

#Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

df = pd.DataFrame(columns=['slow', 'fast', 'pnl', 'sharpe'])
i=0


if __name__ == '__main__':
    optimized_runs = cerebro.run()

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.get_value() - 10000,2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.pfast, 
                strategy.params.pslow, PnL, sharpe['sharperatio']])

        sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
            reverse=True)
        for line in sort_by_sharpe[:5]:
            i+=1
            df.loc[i] = line
    

    data=[go.Heatmap(
                    z=df['sharpe'],
                    x=df['slow'],
                    y=df['fast']
                    )]



    fig = go.Figure(data=data)

    
    fig.update_layout(xaxis_title="slow SMA", yaxis_title="fast SMA", title="Sharpe by SMA combo")


    # fig['layout'].update( 
    #     title='heatmap'
    # )
    pyo.plot(fig, filename='sharpeHeatmap.html')

