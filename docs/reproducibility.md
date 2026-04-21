# Reproducibility

The analysis was done in Python notebooks using shared risk metric functions. Together, these files implement the VaR/CVaR framework used to address the project tasks: extend VaR analysis to CVaR, analyze extreme tail losses, and compare the two measures.

## Main Files

- `risk_metrics.py`: contains Historical VaR, Historical CVaR, Parametric VaR, and Parametric CVaR functions.
- `trio1_analysis.ipynb`: daily analysis for NIFTY 50, HUL, and Adani Enterprises.
- `trio2_weekly_analysis.ipynb`: weekly analysis for HDFC Bank, HUL, and TCS.

## Data and Code

The GitHub repository is the source for the project code, notebooks, and final datasets used by the analyses:

[Aryan-IIT/CoVaR_analysis](https://github.com/Aryan-IIT/CoVaR_analysis)

The notebooks clean the data, compute log returns, call `risk_metrics.py`, and generate the tables and plots used in this website to support the project statement.
