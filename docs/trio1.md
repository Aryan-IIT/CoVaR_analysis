# Trio 1 Highlights

Trio 1 compares a diversified market benchmark, a stable defensive stock, and a volatile stock:

- NIFTY 50: diversified index
- HUL: stable / defensive stock
- Adani Enterprises: volatile stock

The aim is to see how tail risk changes when moving from broad market exposure to individual stock exposure.

## VaR and CVaR Comparison

![Trio 1 VaR and CVaR comparison](assets/images/trio1/comparison.png)

Adani Enterprises shows the strongest downside tail risk in this trio. HUL lies between the index and Adani, while NIFTY 50 is relatively contained because of diversification.

## Tail Gap

![Trio 1 tail gap](assets/images/trio1/tail_gap.png)

The tail gap shows how much worse average tail losses become after the VaR threshold is crossed. A larger gap means VaR alone misses more of the loss severity.

## Tail Amplification

![Trio 1 tail amplification](assets/images/trio1/tail_amplification.png)

Tail amplification gives the relative version of the same idea. It helps compare whether CVaR is much larger than VaR for each asset, even when the absolute risk levels differ.

## Adani Tail Shape

![Adani return distribution](assets/images/trio1/adani.png)

Adani’s return distribution makes the tail-risk result easier to see visually. The historical tail severity can differ from the Gaussian parametric estimate, which is why both methods are useful.
