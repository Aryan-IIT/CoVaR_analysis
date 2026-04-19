# Trio 2 Highlights

Trio 2 compares weekly downside risk across three sector stocks:

- HDFC Bank: banking stock
- HUL: FMCG stock
- TCS: IT stock

The source data is daily, but the analysis uses weekly prices and weekly log returns.

## Weekly VaR and CVaR Comparison

![Trio 2 weekly VaR and CVaR comparison](assets/images/trio2/comparison.png)

This chart compares the weekly downside threshold and average tail severity across the three sectors. It gives the main view of which stock has the highest weekly tail-risk exposure.

## Weekly Tail Gap

![Trio 2 weekly tail gap](assets/images/trio2/tail_gap.png)

Tail gap shows the extra weekly loss beyond the VaR cutoff. It is useful because two assets can have similar VaR values but different loss severity after the cutoff.

## Weekly Tail Amplification

![Trio 2 weekly tail amplification](assets/images/trio2/tail_amplification.png)

Tail amplification compares CVaR relative to VaR. This makes the tail depth easier to compare across banking, FMCG, and IT stocks.

## Skewness and Kurtosis

![Trio 2 skewness and kurtosis](assets/images/trio2/skewness.png)

Skewness and kurtosis help explain whether the return distribution supports the tail-risk findings. High kurtosis or negative skewness can indicate more concern around extreme downside moves.
