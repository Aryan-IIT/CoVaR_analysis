# CoVaR Analysis

This is a financial modelling project focused on downside tail-risk analysis using Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR).

## Current Analyses

- `trio1_analysis.ipynb`: daily VaR/CVaR analysis for NIFTY 50, HUL, and Adani Enterprises.
- `trio2_weekly_analysis.ipynb`: weekly VaR/CVaR analysis for HDFC Bank, HUL, and TCS.

## Risk Metrics

The core risk calculations are implemented in `risk_metrics.py`:

- Historical VaR
- Historical CVaR
- Parametric VaR
- Parametric CVaR

The notebooks load and clean the datasets, compute log returns, call the shared risk metric functions, and compare tail-risk behavior across assets.

## Data

Only the datasets needed for the final notebooks are intended to be tracked:

- `datasets/trio1/`
- `datasets/trio2_5yr/`

Exploratory or trial datasets are ignored to keep the repository clean.
