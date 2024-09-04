# neural_net_trader

The neural_net_trader project is a portfolio project of mine that combines my love for machine learning 
and stock trading. It is a deep lstm model that learns off of yfinance's close day price records. It uses
these records to also create the MSI and RSI values to give the model more descriptive information to train
on. 

The model created, more often than not, beats a 10% yearly average return. However, this is tested through a
backtesting simulation, also included in the program, rather than real money and real-time algorithmic trading.

This model was trained on Apple's stock data, but it is simple to change the data the model trains on by 
changing the ticker in the yf.download() function.

This model uses the libraries:
 - numpy
 - pandas
 - tensorflow
 - yfinance
 - sklearn
 - pickle
 - os
 - math
