# neural_net_trader

![Version](https://badgen.net/badge/version/1.0.0/blue)
![Python](https://badgen.net/badge/python/3.8%2B/blue)
![License](https://badgen.net/badge/license/MIT/green)
![Framework](https://badgen.net/badge/framework/Tensorflow/orange)

The Neural Net Trader is an LSTM model hooked up to a backtesting simulation.

This project trains an LSTM model on stock data to predict the closing price
of the next day. Tensorflow is used to create and train the LSTM model,
yfinance is used to gather the stock data into a dataframe, pandas is used 
to manipulate the dataframe, and sklearn and numpy are used to scale and 
shape the data. It was tough to correctly shape the data into X and Y
values, especially for the backtest simulation. I hope to make this project
more dynamic in the future, where the user can input how they want the model
trained, and it will output more information about the model such as a graph
of how it performs compared to the actual values.

This project uses the libraries:
 - numpy
 - pandas
 - tensorflow
 - yfinance
 - sklearn
 - pickle
 - os
 - math

Using the project just requires running it in your IDE of choice with the
correct libraries installed. It should save a model file (.h5) to the
project directory once it is finished. You can open that file in another
program and use it to make predictions. This project uses the "AAPL" ticker
by default, but if you want to use a different one just change the tickers
attribute in yf.downoad() to whichever ticker you want to fit the model to.

MIT License

Copyright (c) [2024] [Marshall Pigford]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
