#
# Stock Screener in Python: https://www.youtube.com/watch?v=RQw1TUqhRco
#

import pandas as pd
import datetime as dt

import yfinance as yf
from yahoo_fin import stock_info as si


def calculate_return(ticker, start, end):
    try:
        df = yf.download(ticker, start, end)
        df["Pct_Change"] = df["Adj Close"].pct_change()
        df.to_csv(f"data/{ticker}.csv")
        return (df["Pct_Change"] + 1).cumprod().iloc[-1]
    except Exception as e:
        print(f"{e} for {ticker}")
        return


start = dt.datetime.now() - dt.timedelta(days=7)
end = dt.datetime.now()

# SP500 Index (^GSPC symbol)
sp500_return = calculate_return("^GSPC", start, end)

returns = []

# Each SP500 ticker
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_table = pd.read_html(url)
sp500_df = sp500_table[0]
tickers = sp500_df["Symbol"].tolist()

for idx, ticker in enumerate(tickers):
    if idx == 7:
        break

    ticker_return = calculate_return(ticker, start, end)
    if ticker_return:
        ticker_compared_with_sp500 = round(ticker_return / sp500_return, 2)
        returns.append(ticker_compared_with_sp500)

best_performers = pd.DataFrame(
    list(zip(tickers, returns)), columns=["Ticker", "Returns_Compared"]
)
best_performers["Score"] = best_performers["Returns_Compared"].rank(pct=True) * 100
# select top 30%
best_performers = best_performers[
    best_performers["Score"] >= best_performers["Score"].quantile(0.7)
]

final_df = pd.DataFrame(
    columns=[
        "Ticker",
        "Latest_Price",
        "Score",
        # "PE_Ratio",
        # "PEG_Ratio",
        # "SMA_150",
        # "SMA_200",
        # "Low_52_Week",
        # "High_52_Week",
    ]
)
for ticker in best_performers["Ticker"]:
    print(ticker)
    try:
        df = pd.read_csv(f"data/{ticker}.csv", index_col=0)
        # moving_averages = [150, 200]
        # for ma in moving_averages:
        #     df["SMA_" + str(ma)] = round(df["Adj Close"].rolling(window=ma).mean(), 2)

        latest_price = df["Adj Close"].iloc[-1]
        # pe_ratio = float(si.get_quote_table(ticker)["PE Ratio (TTM)"])
        # peg_ratio = float(si.get_stats_valuation(ticker)[1][4])
        # moving_average_150 = df["SMA_150"].iloc[-1]
        # moving_average_200 = df["SMA_200"].iloc[-1]
        # low_52_week = round(min(df["Low"][-(52 * 5) :]), 2)
        # high_52_week = round(max(df["High"][-(52 * 5) :]), 2)
        score = round(
            best_performers[best_performers["Ticker"] == ticker]["Score"].tolist()[0]
        )

        # condition1 = latest_price > moving_average_150 > moving_average_150
        # condition2 = latest_price >= (1.3 * low_52_week)
        # condition3 = latest_price >= (0.75 * high_52_week)
        # condition4 = pe_ratio < 40
        # condition5 = peg_ratio < 2

        # if condition1 and condition2 and condition3 and condition4 and condition5:
        row_df = pd.DataFrame(
            [
                {
                    "Ticker": ticker,
                    "Latest_Price": latest_price,
                    "Score": score,
                    # "PE_Ratio": pe_ratio,
                    # "PEG_Ratio": peg_ratio,
                    # "SMA_150": moving_average_150,
                    # "SMA_200": moving_average_200,
                    # "Low_52_Week": low_52_week,
                    # "High_52_Week": high_52_week,
                }
            ]
        )
        final_df = pd.concat([final_df, row_df], ignore_index=True)
    except Exception as e:
        print(f"{e} for {ticker}")

final_df.sort_values(by="Score", ascending=False)

pd.set_option("display.max_columns", 10)
final_df.to_csv("data/_SCREENED.csv")
