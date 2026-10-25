# ACAD — Single-stock quantitative risk analysis

A full quantitative profile of **Acadia Pharmaceuticals (ACAD)** over 10 years of daily data: return and risk, return distribution, factor exposure (CAPM and Fama-French 3), and robustness of the results.

The goal is to **characterize risk, not to recommend a trade**: what kind of risk ACAD carries, how extreme it is, and which conclusions survive stricter statistical tests.

> Stage 1 of a 3-stage project: (1) one asset in depth → (2) a 5-asset portfolio with out-of-sample validation → (3) comparing 15–20 stocks, where data snooping becomes the central problem.

## Data

- **Source:** Yahoo Finance via `yfinance`. Fixed window: **2016-10-05 → 2026-10-05** (fixed `start`/`end`, so results do not change with the date the script is run).
- **Tickers:** ACAD, SPY (market), IWM − SPY (size factor proxy, SMB), IWD − IWF (value factor proxy, HML), `^IRX` (13-week T-bill, risk-free rate).
- **Returns:** daily log returns → **2,511 observations**.
- **Cleaning decisions:**
  - The risk-free rate is forward-filled on days without a quote (a rate barely moves day to day). **Prices are never filled**, since that would invent 0% returns.
  - Two samples: ACAD alone for descriptive statistics, and all series aligned only for the regressions. A single `dropna()` across all columns silently removed ACAD trading days and changed the total return from −35% to −40%.

## Key findings

| Metric | Value |
|---|---|
| Total return / CAGR | −30.8% / −3.6% per year |
| Annualized volatility | 62.2% (S&P 500 ≈ 18%) |
| Maximum drawdown | −77.2% (trough 2022-06-21) |
| Worst day | −45.4% on 2021-03-09 (FDA rejection) = **−15.4σ** |
| Best day | +63.2% on 2019-09-09 (positive phase 3 results) |
| Skewness / excess kurtosis (daily) | −1.21 / **42.8** |
| CAPM beta / R² | 0.98 [0.85, 1.11] / 0.08 |

1. **The risk is idiosyncratic and binary.** The market explains only 8% of ACAD's daily moves. The largest moves are company-specific regulatory events (FDA decisions).
2. **Fat tails are extreme and not a single outlier.** Removing the worst day lowers excess kurtosis from 42.8 to 25.3, still about 3× that of MSFT. Any model that assumes normality (normal VaR, Gaussian Monte Carlo) treats ACAD's actual risk as impossible.
3. **Beta ≈ 1 does not mean "as risky as the market".** A low correlation (0.28) combined with volatility 3.4× the market's still produces a beta near 1. Total risk is more than 3× the market's.
4. **Factor exposure:** in Fama-French 3, ACAD loads on size (**SMB = 1.11**, significant). The market beta falls from 0.98 to 0.79, and the difference splits *exactly* into indirect channels through SMB and HML (verified numerically).
5. **Robustness check:** with heteroskedasticity-robust (HC3) standard errors, Rm and SMB stay significant, but **HML loses significance** (p = 0.12). The "growth-like" reading is therefore withdrawn.
6. **Alpha:** CAPM required return ≈ 14.1% per year vs. a realized −3.6%. The gap equals the annualized alpha (≈ −17.8%), but it is **not statistically distinguishable from zero** (p = 0.35). With this level of noise, about 100 years of data would be needed to detect it.

Detailed notes, in Spanish: [`hallazgos.md`](hallazgos.md).

## Methods

Log returns · CAGR · annualized volatility · drawdown (running maximum, no look-ahead) · Sharpe ratio · skewness and kurtosis · Jarque-Bera · QQ-plots (daily vs. monthly) · OLS regression (CAPM, Fama-French 3) · HC3 robust standard errors · omitted-variable decomposition of beta.

## Structure

| File | What it does |
|---|---|
| `datos.py` | Download, cleaning, regression table (`model_data`) |
| `riesgo.py` | Total return, CAGR, volatility, drawdown, Sharpe |
| `distribucion.py` | Skewness, kurtosis, Jarque-Bera, QQ-plots, histogram |
| `factores.py` | CAPM, Fama-French 3, HC3, required return |
| `hallazgos.md` | Running log of results and open questions |

## How to run

Requires Python ≥ 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python riesgo.py
uv run python distribucion.py   # saves the QQ-plots and histogram as PNG
uv run python factores.py
```

## Limitations

- **Price data only:** no fundamentals, pipeline or valuation analysis, so no conclusion on whether ACAD is cheap or expensive.
- **Factors are ETF proxies** (IWM − SPY, IWD − IWF), not the original Kenneth French data.
- **Single stock, single period:** results describe ACAD from 2016 to 2026 and do not generalize.

## Status

- [x] Data, risk, distribution, factor models
- [ ] `estabilidad.py`: do the betas hold across subperiods?
- [ ] Written report (`informe.md`)
- [ ] Refactor into functions + tests
