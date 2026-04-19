# CoVaR Analysis

**Group 19 | ES 418**

This project studies downside risk using Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR). In simple terms, VaR estimates a bad-loss cutoff, while CVaR estimates how bad the loss is on average after crossing that cutoff.

We compared risk across two asset groups, using both historical data and a normal-distribution based estimate. The aim was not just to calculate one number, but to understand how tail losses differ across indices, stable stocks, volatile stocks, and sector stocks.

## What We Did

- Cleaned price data and computed log returns.
- Calculated Historical VaR and Historical CVaR at the 5% tail level.
- Calculated Parametric VaR and Parametric CVaR using a Gaussian assumption.
- Compared assets using VaR, CVaR, Tail Gap, and Tail Amplification.
- Built a small MkDocs website to present the strongest visuals and insights.
- Added a lightweight interactive playground for changing the tail level for NIFTY 50 and HUL.

## Main Notebooks

### `trio1_analysis.ipynb`

This notebook uses daily returns for:

- NIFTY 50
- HUL
- Adani Enterprises

The goal was to compare a diversified market index, a relatively stable stock, and a more volatile stock. The results show how individual stock risk can look much sharper than index-level risk.

### `trio2_weekly_analysis.ipynb`

This notebook uses weekly returns for:

- HDFC Bank
- HUL
- TCS

The goal was to compare banking, FMCG, and IT stocks at a weekly frequency. Daily prices were first cleaned and then converted into weekly prices using the last available price of each week.

## Results Tables

The main table values from both notebooks are collected here for easier report writing:

[View results tables](results.md)

## Project Website

The hosted MkDocs website is available here:

[https://aryan-iit.github.io/CoVaR_analysis/](https://aryan-iit.github.io/CoVaR_analysis/)

The website summarizes the project, explains the method, shows key charts, and includes a static interactive VaR/CVaR playground.

## How to Replicate

1. Clone the repository:

```bash
git clone https://github.com/Aryan-IIT/CoVaR_analysis.git
cd CoVaR_analysis
```

2. Install the main Python libraries:

```bash
pip install pandas numpy matplotlib scipy openpyxl
```

3. Open and run the notebooks:

```bash
jupyter notebook trio1_analysis.ipynb
jupyter notebook trio2_weekly_analysis.ipynb
```

4. To rebuild the playground data:

```bash
python3 build_playground_data.py
```

5. To preview the website locally:

```bash
pip install mkdocs-material
mkdocs serve
```

## Important Files

- `risk_metrics.py`: shared VaR and CVaR functions.
- `trio1_analysis.ipynb`: daily analysis for Trio 1.
- `trio2_weekly_analysis.ipynb`: weekly analysis for Trio 2.
- `build_playground_data.py`: precomputes data for the interactive playground.
- `docs/`: MkDocs website content.

## Note

This is an academic project focused on comparing VaR and CVaR under historical and Gaussian assumptions. The results should be read as a modelling exercise, not as investment advice.
