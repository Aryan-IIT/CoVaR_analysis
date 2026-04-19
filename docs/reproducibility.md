# Reproducibility

The analysis was done in Python notebooks using shared risk metric functions.

## Main Files

- `risk_metrics.py`: contains Historical VaR, Historical CVaR, Parametric VaR, and Parametric CVaR functions.
- `trio1_analysis.ipynb`: daily analysis for NIFTY 50, HUL, and Adani Enterprises.
- `trio2_weekly_analysis.ipynb`: weekly analysis for HDFC Bank, HUL, and TCS.

## Data and Code

The GitHub repository is the source for the project code, notebooks, and final datasets used by the analyses:

[Aryan-IIT/CoVaR_analysis](https://github.com/Aryan-IIT/CoVaR_analysis)

The notebooks clean the data, compute log returns, call `risk_metrics.py`, and generate the comparison tables and plots used in this website.
