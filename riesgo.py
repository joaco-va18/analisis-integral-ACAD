import numpy as np
from datos import returns_log
from datos import price
from datos import rf_d
acad = returns_log["ACAD"].dropna()
price_acad = price["ACAD"]
total_r = np.exp(acad.sum()) - 1
years = (acad.index[-1] - acad.index[0]).days / 365.25
cagr = np.exp(acad.sum() / years) - 1
d_vol = acad.std()
y_vol = d_vol * np.sqrt(252)
maximum = np.maximum.accumulate(price_acad)
dd = ((price_acad - maximum) / maximum)
max_dd = dd.min()
worst = acad.min()
worst_d = acad.idxmin()
best = acad.max()
best_d = acad.idxmax()
sharpe = ((acad.mean() - rf_d.mean())) / d_vol * np.sqrt(252)
if __name__ == "__main__":
    print("Overall return:", round(total_r * 100, 4), "%")
    print("CAGR:", round(cagr * 100, 4), "%")
    print("Daily volatility:", round(d_vol * 100, 4), "%")
    print("Annualized volatility:", round(y_vol * 100, 4), "%")
    print("Max drawdown:", round(max_dd * 100, 2), "%")
    print("Trough date:", dd.idxmin())
    print("Current drawdown:", round(dd.iloc[-1] * 100, 4), "%")
    print("Worst daily return:", round((np.exp(worst) - 1) * 100, 4), "% on", worst_d)
    print("Best daily return:", round((np.exp(best) - 1) * 100, 4), "% on", best_d)
    print("Sharpe:", round(sharpe, 4))