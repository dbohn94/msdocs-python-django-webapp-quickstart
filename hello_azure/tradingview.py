import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart
import webview

if __name__ == '__main__':
    
    chart = Chart()
    gui='edgechromium'

    msft = yf.Ticker("MSFT")
    df = msft.history(period="1y")

    # prepare indicator values
    sma = df.ta.sma(length=20).to_frame()
    sma = sma.reset_index()
    sma = sma.rename(columns={"Date": "time", "SMA_20": "value"})
    sma = sma.dropna()

    # this library expects lowercase columns for date, open, high, low, close, volume
    df = df.reset_index()
    df.columns = df.columns.str.lower()
    chart.set(df)
    print(df)
    # add sma line
    line = chart.create_line()    
    line.set(sma)

    chart.watermark('MSFT')
      
    #chart.show(block=True)  # use_qt=True is required for the chart to display in the webview window
