import yfinance as yf
import numpy as np
import pandas as pd
def calc_returns_log(precios):
    returns_log = np.log(precios / precios.shift(1))
    return returns_log
datos = yf.download(["ACAD", "SPY", "IWM", "IWD", "IWF", "^IRX"], start="2016-10-05", end="2026-10-05")
price = datos["Close"][["ACAD", "SPY", "IWM", "IWD", "IWF", "^IRX"]]
returns_log = calc_returns_log(price)
rf_d = ((price["^IRX"] / 100 / 252).ffill())
model_data = pd.DataFrame({
    "ACAD_exc": returns_log["ACAD"] - rf_d,
    "Rm":  returns_log["SPY"]  - rf_d,
    "SMB":      returns_log["IWM"]  - returns_log["SPY"],
    "HML":      returns_log["IWD"]  - returns_log["IWF"],
}).dropna()
if __name__ == "__main__":
    print("Days downloaded:", len(model_data))
    print("Days downloaded:", len(price))