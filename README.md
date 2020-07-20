# Backtesting_All_Moving_Averages
Given a stock ticker and time period, this program uses the Backtrader library to test all different combinations of moving averages to optimize sharpe ratio. 

Every iteration tests a different combination of fast and slow moving averages. The strategy is simple, if the fast moving average crosses the slow moving average, buy. If the two moving averages cross again and the investor owns shares, sell. Fast moving averages cover a range of 5 to 20 days, slow moving averages cover a range of 50 to 100 days. The results are plotted in a heatmap. 


